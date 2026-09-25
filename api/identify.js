// Vercel serverless function: proxies a photo to the Pl@ntNet API and maps
// its result onto our 16-plant database (plants.json), so the key never
// reaches the browser. Requires the PLANTNET_API_KEY environment variable.
const fs = require('fs');
const path = require('path');

const PLANTS = JSON.parse(
  fs.readFileSync(path.join(process.cwd(), 'plants.json'), 'utf8')
).plants;

const MIN_SCORE = 0.03;

function norm(s) {
  return (s || '').toLowerCase().trim();
}

function speciesMatches(candidate, sciName, genus) {
  const c = norm(candidate);
  const words = c.split(' ').filter(Boolean);
  return words.length >= 2 ? c === sciName : c === genus;
}

function findMatch(results) {
  for (const r of results) {
    const sciName = norm(r.species && r.species.scientificNameWithoutAuthor);
    const genus = norm(r.species && r.species.genus && r.species.genus.scientificNameWithoutAuthor);
    if (!sciName) continue;
    for (const p of PLANTS) {
      if (p.scientific.some((cand) => speciesMatches(cand, sciName, genus))) {
        return { slug: p.slug, score: r.score };
      }
    }
  }
  return null;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'method_not_allowed' });
    return;
  }

  const apiKey = process.env.PLANTNET_API_KEY;
  if (!apiKey) {
    res.status(500).json({ error: 'server_not_configured' });
    return;
  }

  try {
    const { image } = req.body || {};
    if (!image) {
      res.status(400).json({ error: 'no_image' });
      return;
    }
    const base64 = image.includes(',') ? image.split(',')[1] : image;
    const buffer = Buffer.from(base64, 'base64');

    const form = new FormData();
    form.append('images', new Blob([buffer], { type: 'image/jpeg' }), 'photo.jpg');
    form.append('organs', 'flower');

    const url = `https://my-api.plantnet.org/v2/identify/all?api-key=${encodeURIComponent(apiKey)}`;
    const plantnetRes = await fetch(url, { method: 'POST', body: form });

    if (!plantnetRes.ok) {
      const detail = await plantnetRes.text();
      res.status(502).json({ error: 'plantnet_error', detail: detail.slice(0, 500) });
      return;
    }

    const data = await plantnetRes.json();
    const results = (data.results || []).slice(0, 5);
    const match = findMatch(results);

    if (match && match.score >= MIN_SCORE) {
      res.status(200).json({ matched: true, slug: match.slug, score: match.score });
    } else {
      res.status(200).json({ matched: false });
    }
  } catch (err) {
    res.status(500).json({ error: 'internal_error', detail: String((err && err.message) || err) });
  }
};
