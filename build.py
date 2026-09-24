#!/usr/bin/env python3
"""Regenerate the plant grid and care-modal data in index.html from plants.json.

Only the cards between <div class="grid"> and its closing tag, and the JSON
inside <script id="plant-care-data">, are rewritten; the head and masthead
stay hand-edited in the HTML.

After editing plants.json, run:  python3 build.py
"""
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent

CARE_FIELDS = [
    ("soil", "Грунт"),
    ("light", "Свет"),
    ("neighbors", "Соседство"),
    ("planting", "Посадка"),
    ("watering", "Полив"),
    ("fertilizer", "Удобрение"),
    ("other", "Уход"),
]


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(plant):
    src = plant["image"]
    w, h = Image.open(ROOT / src).size
    title = esc(plant["title"])
    note = esc(plant["note"])
    status = plant["status"]

    return f"""        <figure class="plant" data-plant="{plant['slug']}">
          <img src="{src}" alt="{title}" width="{w}" height="{h}" loading="lazy" decoding="async">
          <figcaption>
            <span class="plant__title">{title}</span>
            <span class="plant__status plant__status--{status}">{note}</span>
          </figcaption>
        </figure>"""


def care_data(data):
    out = {}
    for p in data["plants"]:
        fields = [{"label": label, "value": p["care"].get(key, "")} for key, label in CARE_FIELDS]
        out[p["slug"]] = {
            "title": p["title"],
            "status": p["note"],
            "statusKey": p["status"],
            "fields": fields,
        }
    return out


def main():
    data = json.loads((ROOT / "plants.json").read_text())
    cards = "\n".join(card(p) for p in data["plants"])

    page = ROOT / "index.html"
    html = page.read_text()

    html, n = re.subn(r'(<div class="grid">\n).*?(\n      </div>\n  </main>)',
                       lambda m: m.group(1) + cards + m.group(2), html, flags=re.S)
    if n != 1:
        raise SystemExit("grid block not found in index.html")

    care_json = json.dumps(care_data(data), ensure_ascii=False)
    html, n2 = re.subn(
        r'(<script type="application/json" id="plant-care-data">).*?(</script>)',
        lambda m: m.group(1) + care_json + m.group(2), html, flags=re.S)
    if n2 != 1:
        raise SystemExit("plant-care-data script not found in index.html")

    page.write_text(html)
    print(f"{len(data['plants'])} cards written")


if __name__ == "__main__":
    main()
