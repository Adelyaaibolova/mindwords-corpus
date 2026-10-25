"""
Export the comment CSV to a Sketch Engine / CQPweb-ready plain-text file.

Each comment becomes one <doc> element whose attributes carry the metadata,
so in Sketch Engine you can filter or build subcorpora by video, type or year.

    <doc id="1" source="COWBOY" type="top" likes="0" year="2026">
    Man I'm afraid too get it all together ...
    </doc>

Usage:
    python scripts/export_sketchengine.py data/raw/combined_filtered.csv corpus.txt
    python scripts/export_sketchengine.py data/raw/combined_filtered.csv corpus.txt --sources out__15_.csv jordan.csv
    python scripts/export_sketchengine.py ... --dedupe
"""

from __future__ import annotations

import argparse
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

import pandas as pd

from textclean import clean


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("--sources", nargs="*", help="only include these source files (e.g. the two videos used)")
    p.add_argument("--dedupe", action="store_true", help="drop exact duplicate comments (same text, date, time)")
    args = p.parse_args()

    df = pd.read_csv(args.csv)
    if args.sources:
        df = df[df["source_file"].isin(args.sources)]
    if args.dedupe:
        df = df.drop_duplicates(subset=["comment", "date", "time"])

    with args.out.open("w", encoding="utf-8") as fh:
        for r in df.itertuples(index=False):
            attrs = {
                "id": r.comment_id,
                "source": str(r.source_file).removesuffix(".csv"),
                "type": r.type,
                "likes": r.likecount,
                "year": str(r.date)[:4],
            }
            attr_str = " ".join(f"{k}={quoteattr(str(v))}" for k, v in attrs.items())
            fh.write(f"<doc {attr_str}>\n{escape(clean(r.comment))}\n</doc>\n")

    print(f"{len(df)} documents -> {args.out}")


if __name__ == "__main__":
    main()
