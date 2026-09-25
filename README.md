# Растения Палисадника

Static site with one serverless function. Card grid of plants from the
Palisadnik guide: name, photo (vertical, fills the card via
`object-fit: cover`), and a wintering-status dot. Tapping a photo opens a
modal with the full care info (soil, light, neighbors, planting, watering,
fertilizer, other care), closed with the text "Назад" button. Design ported
from the [Andrey Novitskiy, site / CORE](https://github.com/snegurkirill/andrey-novitskiy-site)
catalogue system (same design-pixel unit, same card grid).

## Recognize a plant

A fixed footer button ("Распознать") opens a full-screen camera view with a
single round shutter button. The captured photo is sent to `/api/identify`,
a Vercel serverless function that forwards it to the
[Pl@ntNet API](https://my.plantnet.org) and matches the result against this
site's 16 plants by scientific name (`scientific` field in `plants.json`).
A match opens that plant's care modal, same as clicking its card; no match
shows an in-camera message with a "Попробовать ещё" button.

## Updating the plants

Card and care data lives in `plants.json`. After editing it, regenerate the
grid and the modal's embedded JSON:

    python3 build.py

Status must be one of `winters`, `fifty`, `replant`, `no` (see `statuses` in
`plants.json`). Add a `scientific` array (genus+species, or just genus for a
loose match) so the recognizer can find the plant. The head and masthead in
`index.html` are edited by hand — `build.py` only rewrites the cards
(`<div class="grid">`) and the `#plant-care-data` JSON script tag.

## Deploy

[Vercel](https://vercel.com) — static files + the `api/identify.js`
serverless function in one deploy (GitHub Pages can't run server code, which
the function needs to keep the Pl@ntNet key off the client).

1. Get a free API key at [my.plantnet.org](https://my.plantnet.org) (My
   account → API access; free tier is for non-commercial/educational use).
2. On [vercel.com](https://vercel.com), sign in with GitHub, "Add New
   Project", import `snegurkirill/tamed-form-site`.
3. In the project's Environment Variables, add `PLANTNET_API_KEY` with that
   key, then deploy.

Every push to `main` redeploys automatically. See `.env.example` for the
variable name (do not commit a real key).

## Data

`plants.json` is sourced from the "Гид по растениям" tab of the Palisadnik
Google Sheet (smeta) — both the wintering status and the care columns
(Грунт/Свет/Соседство/Полив/Удобрение/...). Photos are from Wikimedia
Commons under open licenses (CC0/CC BY/CC BY-SA/PD); each `plants.json`
entry's `credit` field has the author/license/source, and the same list is
kept as an HTML comment near the end of `index.html` (off-page, since the
license terms still call for attribution even though it isn't shown
on-screen).
