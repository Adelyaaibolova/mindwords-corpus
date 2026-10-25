"""
Compute descriptive statistics from the cleaned corpus (output of clean_comments.py)
and write them to data/derived/. These files contain counts, not comment texts.

Outputs:
    source_stats.csv         comments, replies, tokens, date range per source file
    word_frequencies.csv     top N word forms (lower-cased) with counts and per-million
    headword_by_source.csv   frequency of the dictionary headwords in each source
    figures/comments_per_source.png
    figures/headwords_per_million.png

Usage:
    python scripts/corpus_stats.py data/raw/corpus_clean.csv --out data/derived
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

import pandas as pd

from textclean import clean

TOKEN_RE = re.compile(r"[a-z]+(?:[-'’][a-z]+)*")

HEADWORDS = {
    "anxiety": r"\banxiet(?:y|ies)\b",
    "overthinking": r"\boverthink(?:ing|s|er)?\b",
    "discipline": r"\bdisciplin(?:e|ed|es)\b",
    "mindset": r"\bmindsets?\b",
    "self-education": r"\bself[- ]educat(?:ion|ed)\b",
    "empathy": r"\bempath(?:y|ic)\b",
    "healing": r"\bheal(?:ing|ed|s)?\b",
    "self-worth": r"\bself[- ]worth\b",
    "mindfulness": r"\bmindful(?:ness)?\b",
    "self-motivation": r"\bself[- ]motivat(?:ion|ed)\b",
    "you are not alone": r"\byou(?:'re| are) not alone\b",
}


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(str(text).lower())


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("csv", type=Path)
    p.add_argument("--out", type=Path, default=Path("data/derived"))
    p.add_argument("--top", type=int, default=2000)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.csv)
    df["comment"] = df["comment"].map(clean)
    df["tokens"] = df["comment"].map(tokenize)
    df["n_tokens"] = df["tokens"].map(len)

    # per-source statistics
    stats = df.groupby("source_file").agg(
        comments=("comment", "size"),
        top_level=("type", lambda s: (s == "top").sum()),
        replies=("type", lambda s: (s == "reply").sum()),
        tokens=("n_tokens", "sum"),
        median_tokens_per_comment=("n_tokens", "median"),
        total_likes=("likecount", "sum"),
        first_comment=("date", "min"),
        last_comment=("date", "max"),
    ).sort_values("comments", ascending=False)
    total = pd.DataFrame([{
        "comments": len(df), "top_level": (df.type == "top").sum(), "replies": (df.type == "reply").sum(),
        "tokens": df.n_tokens.sum(), "median_tokens_per_comment": df.n_tokens.median(),
        "total_likes": df.likecount.sum(), "first_comment": df.date.min(), "last_comment": df.date.max(),
    }], index=["TOTAL"])
    pd.concat([stats, total]).rename_axis("source_file").to_csv(args.out / "source_stats.csv")

    # word frequencies (drop any remaining exact duplicates)
    dedup = df.drop_duplicates(subset=["comment", "date", "time"])
    counts = Counter(tok for toks in dedup["tokens"] for tok in toks)
    n = sum(counts.values())
    freq = pd.DataFrame(counts.most_common(args.top), columns=["word", "count"])
    freq.insert(0, "rank", range(1, len(freq) + 1))
    freq["per_million"] = (freq["count"] / n * 1e6).round(2)
    freq.to_csv(args.out / "word_frequencies.csv", index=False)

    # headwords per source
    rows = []
    for src, g in dedup.groupby("source_file"):
        lower = g["comment"].str.lower()
        toks = g["n_tokens"].sum()
        for hw, pat in HEADWORDS.items():
            hits = int(lower.str.count(pat).sum())
            rows.append({"headword": hw, "source_file": src, "hits": hits,
                         "per_million": round(hits / toks * 1e6, 2) if toks else 0})
    hw = pd.DataFrame(rows)
    hw.to_csv(args.out / "headword_by_source.csv", index=False)

    make_figures(stats, hw, dedup, args.out / "figures")
    print(f"{len(df)} comments, {df.n_tokens.sum():,} tokens; "
          f"{len(df) - len(dedup)} duplicates; outputs in {args.out}")


def make_figures(stats: pd.DataFrame, hw: pd.DataFrame, dedup: pd.DataFrame, fig_dir: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

    s = stats.sort_values("comments")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(s.index.str.removesuffix(".csv"), s["top_level"], color="#3B6EA8", label="top-level")
    ax.barh(s.index.str.removesuffix(".csv"), s["replies"], left=s["top_level"], color="#9DB8D9", label="replies")
    ax.set_xlabel("comments")
    ax.set_title("Comments per source file (cleaned corpus)", loc="left")
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(fig_dir / "comments_per_source.png", dpi=150)
    plt.close(fig)

    toks = dedup["n_tokens"].sum()
    overall = {h: dedup["comment"].str.lower().str.count(p).sum() / toks * 1e6 for h, p in HEADWORDS.items()}
    o = pd.Series(overall).sort_values()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(o.index, o.values, color="#3B6EA8")
    for i, v in enumerate(o.values):
        ax.text(v, i, f" {v:.1f}", va="center", fontsize=9)
    ax.set_xlabel("occurrences per million tokens (all forms)")
    ax.set_title("Dictionary headwords in the cleaned corpus (all 13 videos)", loc="left")
    fig.tight_layout()
    fig.savefig(fig_dir / "headwords_per_million.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
