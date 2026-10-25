"""
Build the MindWords dictionary page (docs/index.html).

    dictionary/entries.json   the 11 entries: definitions, corpus examples, word groups,
                              usage notes, translations with source links, quotes
    dictionary/template.html  the page design (the dictionary as designed in the project)
    data/videos.csv           maps each example's source file to the video's creator

The data is written into the template, so the result is one static HTML file that
works on GitHub Pages and when opened from disk. Edit entries.json, then run:

    python scripts/build_dictionary.py
    python scripts/build_dictionary.py --verify data/raw/corpus_clean.csv   # check every example
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "dictionary" / "entries.json"
TEMPLATE = ROOT / "dictionary" / "template.html"
VIDEOS = ROOT / "data" / "videos.csv"
OUT = ROOT / "docs" / "index.html"


def js_json(obj) -> str:
    """JSON that is safe to place inside a <script> element."""
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def verify(data: dict, corpus_csv: Path) -> None:
    """Fail if an example does not occur verbatim under its source video in the corpus."""
    import pandas as pd

    df = pd.read_csv(corpus_csv, usecols=["comment", "source_file"])
    df["comment"] = df["comment"].astype(str)
    bad = []
    for e in data["entries"]:
        for x in e["examples"]:
            texts = df.loc[df["source_file"] == x["source"], "comment"]
            if not texts.str.contains(x["text"], regex=False).any():
                bad.append(f'{e["id"]}: "{x["text"][:60]}" ({x["source"]})')
    if bad:
        raise SystemExit("examples not found in the corpus:\n  " + "\n  ".join(bad))
    n = sum(len(e["examples"]) for e in data["entries"])
    print(f"all {n} examples found verbatim in {corpus_csv}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--verify", type=Path, metavar="CORPUS_CSV", help="check examples against the cleaned corpus")
    args = p.parse_args()

    data = json.loads(ENTRIES.read_text(encoding="utf-8"))
    if args.verify:
        verify(data, args.verify)
    with VIDEOS.open(encoding="utf-8") as fh:
        sources = {r["source_file"]: r["creator"] for r in csv.DictReader(fh)}

    missing = {x["source"] for e in data["entries"] for x in e["examples"]} - sources.keys()
    if missing:
        raise SystemExit(f"examples cite unknown source files: {sorted(missing)}")

    page = TEMPLATE.read_text(encoding="utf-8")
    for marker, value in (("/*__DATA__*/null", data), ("/*__SOURCES__*/null", sources)):
        if marker not in page:
            raise SystemExit(f"marker {marker} not found in template")
        page = page.replace(marker, js_json(value))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"{len(data['entries'])} entries -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
