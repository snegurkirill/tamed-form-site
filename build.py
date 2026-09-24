#!/usr/bin/env python3
"""Regenerate the plant grid in index.html from plants.json.

Only the cards between <div class="grid"> and its closing tag are rewritten;
the head and masthead stay hand-edited in the HTML.

After editing plants.json, run:  python3 build.py
"""
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
NB = " "
WIDE_RATIO = 1.4


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(plant, statuses):
    src = plant["image"]
    w, h = Image.open(ROOT / src).size
    title = esc(plant["title"])
    note = esc(plant["note"])
    wide = " plant--wide" if w / h > WIDE_RATIO else ""

    key = plant["status"]
    if key not in statuses:
        raise SystemExit(f"plant {plant['id']}: unknown status {key!r}")
    status = (f'\n            <span class="plant__status plant__status--{key}">'
              f"{statuses[key]}</span>")

    return f"""        <figure class="plant{wide}">
          <img src="{src}" alt="{title}" width="{w}" height="{h}" loading="lazy" decoding="async">
          <figcaption>
            <span class="plant__title">{title}</span>{status}
          </figcaption>
        </figure>"""


def credits_list(plants):
    items = []
    for p in plants:
        c = p["credit"]
        items.append(
            f'          <li>{esc(p["title"])} — {esc(c["author"])}, '
            f'{esc(c["license"])}, <a href="{c["source"]}" rel="noopener">Wikimedia Commons</a></li>'
        )
    return "\n".join(items)


def main():
    data = json.loads((ROOT / "plants.json").read_text())
    cards = "\n".join(card(p, data["statuses"]) for p in data["plants"])

    page = ROOT / "index.html"
    html = page.read_text()

    html, n = re.subn(r'(<div class="grid">\n).*?(\n      </div>\n  </main>)',
                       lambda m: m.group(1) + cards + m.group(2), html, flags=re.S)
    if n != 1:
        raise SystemExit("grid block not found in index.html")

    html, n2 = re.subn(r'(<ul class="credits__list">\n).*?(\n        </ul>)',
                        lambda m: m.group(1) + credits_list(data["plants"]) + m.group(2),
                        html, flags=re.S)
    if n2 != 1:
        raise SystemExit("credits list not found in index.html")

    page.write_text(html)
    print(f"{len(data['plants'])} cards written")


if __name__ == "__main__":
    main()
