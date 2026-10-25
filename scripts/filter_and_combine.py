"""
Combine per-video CSVs into one file and remove non-English comments.

Steps:
  1. read every CSV in --in-dir, add a `source_file` column
  2. unescape leftover HTML entities (&#39; -> ') and <br> tags
  3. drop comments written in Arabic script (the main non-English group found
     in the raw data); optionally run `langdetect` to drop other languages too
  4. renumber comment_id and write combined_filtered.csv

Usage:
    python scripts/filter_and_combine.py --in-dir data/raw --out data/raw/combined_filtered.csv
    python scripts/filter_and_combine.py --in-dir data/raw --out ... --langdetect
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

from textclean import clean

ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")
LATIN_RE = re.compile(r"[A-Za-z]")


def mostly_arabic(text: str, threshold: float = 0.3) -> bool:
    ar = len(ARABIC_RE.findall(text))
    lat = len(LATIN_RE.findall(text))
    return ar > 0 and ar / max(ar + lat, 1) >= threshold


def is_english(text: str) -> bool:
    from langdetect import DetectorFactory, LangDetectException, detect

    DetectorFactory.seed = 0
    if len(LATIN_RE.findall(text)) < 15:  # too short to classify reliably: keep
        return True
    try:
        return detect(text) == "en"
    except LangDetectException:
        return True


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--in-dir", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--langdetect", action="store_true", help="also drop non-English Latin-script comments")
    args = p.parse_args()

    frames = []
    for path in sorted(args.in_dir.glob("*.csv")):
        if path.resolve() == args.out.resolve():
            continue
        df = pd.read_csv(path)
        df["source_file"] = path.name
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    n0 = len(df)

    df["comment"] = df["comment"].map(clean)
    df = df[df["comment"].str.len() > 0]
    df = df[~df["comment"].map(mostly_arabic)]
    n_ar = len(df)
    if args.langdetect:
        df = df[df["comment"].map(is_english)]

    df["comment_id"] = range(1, len(df) + 1)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"{n0} raw -> {n_ar} after Arabic filter -> {len(df)} written to {args.out}")


if __name__ == "__main__":
    main()
