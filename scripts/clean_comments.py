"""
Clean the combined comment file before loading it into Sketch Engine / CQPweb.

Text-level steps (see textclean.py), applied to every comment:
  1. html          drop timestamp/emoji links, <br> -> space, strip tags, unescape &#39; etc.
  2. invisible     zero-width spaces, bidi marks, soft hyphens
  3. urls          http(s)://... and www....
  4. timestamps    video positions: H:MM:SS, leading MM:SS, "at 12:30", "@6:35"
                   (mid-sentence 3:16 is kept: Bible verses, clock times)
  5. mentions      reply handles (@username) - noise for the corpus and personal data
  6. whitespace    collapse runs of spaces/newlines
  (optional) emojis   --strip-emojis; they are already kept in the `emojis` column

Row-level steps:
  7. no_letters         drop comments left without a single letter (emoji-only, "16:00")
  8. duplicate_source   drop a source file whose comments repeat another file's (>= 90 %)
  9. duplicate_comment  drop exact duplicates within one source (same text, date, time)
 10. repeated_text      the same text (ignoring greeting/name) posted >= 5 times in one video:
                        creator template replies ("Hello X, thank you for watching my TEDx talk...")
                        and spam bots (book/investment ads). The first occurrence is kept.
                        Only texts of 6+ words (20+ Latin letters) are considered. --repeat-threshold 0 disables it.
 11. min_words          optional --min-words N

Writes the cleaned CSV and a step-by-step log (CSV) of how many comments each
step changed or removed.

Usage:
    python scripts/clean_comments.py data/raw/combined_filtered.csv data/raw/corpus_clean.csv
    python scripts/clean_comments.py IN OUT --strip-emojis --min-words 3 --keep-original
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

import textclean as tc

TEXT_STEPS = [
    ("html", tc.strip_html),
    ("invisible", tc.remove_invisible),
    ("urls", tc.remove_urls),
    ("timestamps", tc.remove_timestamps),
    ("mentions", tc.remove_mentions),
    ("timestamps_after_mentions", tc.remove_timestamps),
    ("whitespace", tc.normalize_whitespace),
]


def find_duplicate_sources(df: pd.DataFrame, threshold: float = 0.9) -> dict[str, str]:
    """Return {source_to_drop: source_it_duplicates} for files that share >= threshold of comments."""
    keys = {s: set(zip(g["comment"], g["date"], g["time"])) for s, g in df.groupby("source_file", sort=True)}
    drop: dict[str, str] = {}
    names = sorted(keys, key=str.lower)  # keep the first name alphabetically, drop later copies
    for i, a in enumerate(names):
        if a in drop:
            continue
        for b in names[i + 1:]:
            if b in drop:
                continue
            shared = len(keys[a] & keys[b])
            if shared and shared / min(len(keys[a]), len(keys[b])) >= threshold:
                drop[b] = a
    return drop


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--log", type=Path, help="step log CSV (default: <output>_log.csv)")
    p.add_argument("--strip-emojis", action="store_true", help="also remove emojis from the text")
    p.add_argument("--min-words", type=int, default=0, help="drop comments with fewer words")
    p.add_argument("--keep-original", action="store_true", help="keep the raw text in `comment_raw`")
    p.add_argument("--dup-threshold", type=float, default=0.9)
    p.add_argument("--repeat-threshold", type=int, default=5,
                   help="drop texts repeated this many times per source (0 = off)")
    p.add_argument("--repeats-out", type=Path, help="CSV listing the repeated texts that were removed")
    args = p.parse_args()

    df = pd.read_csv(args.input, dtype={"replycount": str})
    df["comment"] = df["comment"].fillna("").astype(str)
    if args.keep_original:
        df["comment_raw"] = df["comment"]
    log = [{"step": "input", "kind": "rows", "affected": len(df), "rows_left": len(df)}]

    steps = TEXT_STEPS + ([("emojis", tc.remove_emojis), ("whitespace_2", tc.normalize_whitespace)]
                          if args.strip_emojis else [])
    for name, fn in steps:
        new = df["comment"].map(fn)
        changed = int((new != df["comment"]).sum())
        df["comment"] = new
        if not name.startswith("whitespace_2"):
            log.append({"step": name, "kind": "text changed", "affected": changed, "rows_left": len(df)})

    def drop(mask: pd.Series, name: str, note: str = "") -> None:
        nonlocal df
        n = int(mask.sum())
        df = df[~mask]
        log.append({"step": name, "kind": "rows dropped", "affected": n, "rows_left": len(df), "note": note})

    drop(~df["comment"].map(tc.has_letters), "no_letters")

    dup_sources = find_duplicate_sources(df, args.dup_threshold)
    drop(df["source_file"].isin(dup_sources),
         "duplicate_source", "; ".join(f"{k} = {v}" for k, v in dup_sources.items()))

    drop(df.duplicated(subset=["source_file", "comment", "date", "time"]), "duplicate_comment")

    if args.repeat_threshold:
        key = df["comment"].map(tc.template_key)
        eligible = (df["comment"].str.split().str.len() >= 6) & (key.str.len() >= 20)
        counts = key.groupby([df["source_file"], key]).transform("size")
        repeated = eligible & (counts >= args.repeat_threshold)
        first = ~df.assign(_k=key).duplicated(subset=["source_file", "_k"])
        if args.repeats_out:
            summary = (df[repeated].assign(template=key[repeated])
                       .groupby(["source_file", "template"]).size()
                       .rename("occurrences").sort_values(ascending=False).reset_index())
            summary.to_csv(args.repeats_out, index=False)
        drop(repeated & ~first, "repeated_text", f">= {args.repeat_threshold} times, first kept")

    if args.min_words:
        drop(df["comment"].str.split().str.len() < args.min_words, f"min_words_{args.min_words}")

    df = df.copy()
    df["comment_id"] = range(1, len(df) + 1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)

    log_path = args.log or args.output.with_name(args.output.stem + "_log.csv")
    log_df = pd.DataFrame(log)
    log_df.to_csv(log_path, index=False)

    print(log_df.fillna("").to_string(index=False))
    print(f"\n{len(df)} comments -> {args.output}\nlog -> {log_path}")


if __name__ == "__main__":
    main()
