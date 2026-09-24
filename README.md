# Гид по растениям — Палисадник

Static site, no build step. Every path is relative, so it runs at a domain
root or a subpath on any host unchanged.

Card grid of plants from the Palisadnik guide: name, photo, and whether the
plant winters in the ground. Design ported from the
[Andrey Novitskiy, site / CORE](https://github.com/snegurkirill/andrey-novitskiy-site)
catalogue system (same design-pixel unit, same two-column card grid).

## Updating the plants

Card data lives in `plants.json`. After editing it, regenerate the grid:

    python3 build.py

Status must be one of `winters`, `fifty`, `no` (see `statuses` in
`plants.json`). The head, masthead and legend in `index.html` are edited by
hand — `build.py` only rewrites the cards and the credits list.

## Deploy

GitHub Pages, serving `main` from the repo root.

## Data

`plants.json` is sourced from the "Гид по растениям" tab of the Palisadnik
Google Sheet (smeta). Photos are from Wikimedia Commons under open licenses
(CC0/CC BY/CC BY-SA/PD) — author and source link for each are listed in the
credits block at the bottom of the page, per `plants.json`'s `credit` field.
