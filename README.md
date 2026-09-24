# Растения Палисадника

Static site, no build step. Every path is relative, so it runs at a domain
root or a subpath on any host unchanged.

Card grid of plants from the Palisadnik guide: name, photo (vertical, fills
the card via `object-fit: cover`), and a wintering-status dot. Tapping a
photo opens a modal with the full care info (soil, light, neighbors,
planting, watering, fertilizer, other care) from the sheet, closed with the
text "Назад" button. Design ported from the
[Andrey Novitskiy, site / CORE](https://github.com/snegurkirill/andrey-novitskiy-site)
catalogue system (same design-pixel unit, same card grid).

## Updating the plants

Card and care data lives in `plants.json`. After editing it, regenerate the
grid and the modal's embedded JSON:

    python3 build.py

Status must be one of `winters`, `fifty`, `no` (see `statuses` in
`plants.json`). The head and masthead in `index.html` are edited by hand —
`build.py` only rewrites the cards (`<div class="grid">`) and the
`#plant-care-data` JSON script tag.

## Deploy

GitHub Pages, serving `main` from the repo root.

## Data

`plants.json` is sourced from the "Гид по растениям" tab of the Palisadnik
Google Sheet (smeta) — both the wintering status and the care columns
(Грунт/Свет/Соседство/Полив/Удобрение/...). Photos are from Wikimedia
Commons under open licenses (CC0/CC BY/CC BY-SA/PD); each `plants.json`
entry's `credit` field has the author/license/source, and the same list is
kept as an HTML comment near the end of `index.html` (off-page, since the
license terms still call for attribution even though it isn't shown
on-screen).
