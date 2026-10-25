"""
Collect top-level comments and replies from YouTube videos via the YouTube Data API v3.

The API key is read from the environment variable YOUTUBE_API_KEY (or a .env file).
Never hard-code the key in this file.

Usage:
    export YOUTUBE_API_KEY=...            # or put it in .env
    python scripts/collect_comments.py --video-id VIDEO_ID --out data/raw/imbo.csv
    python scripts/collect_comments.py --video-list data/videos.csv --out-dir data/raw/

Output columns (same schema as combined_filtered.csv, minus source_file):
    comment_id, type, replycount, likecount, date, time, emojis, comment
"""

from __future__ import annotations

import argparse
import csv
import html
import os
import re
import sys
import time
from pathlib import Path

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:  # pragma: no cover
    sys.exit("Missing dependency: pip install -r requirements.txt")

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Rough emoji range: pictographs, symbols, dingbats, flags, variation selectors.
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E6-\U0001F1FF"
    "\U0000FE0F"
    "]+"
)
TAG_RE = re.compile(r"<[^>]+>")

FIELDS = ["comment_id", "type", "replycount", "likecount", "date", "time", "emojis", "comment"]


def clean_text(raw: str) -> str:
    """Unescape HTML entities and strip HTML tags (YouTube returns textDisplay as HTML)."""
    text = raw.replace("<br>", " ")
    text = TAG_RE.sub("", text)
    return html.unescape(text).strip()


def to_row(snippet: dict, kind: str, reply_count: int | str) -> dict:
    published = snippet["publishedAt"]  # e.g. 2026-03-23T15:03:11Z
    text = clean_text(snippet.get("textDisplay", ""))
    return {
        "type": kind,
        "replycount": reply_count,
        "likecount": snippet.get("likeCount", 0),
        "date": published[:10],
        "time": published[11:16],
        "emojis": "".join(EMOJI_RE.findall(text)),
        "comment": text,
    }


def fetch_replies(youtube, parent_id: str) -> list[dict]:
    rows, token = [], None
    while True:
        resp = youtube.comments().list(
            part="snippet", parentId=parent_id, maxResults=100, pageToken=token, textFormat="html"
        ).execute()
        rows += [to_row(item["snippet"], "reply", "-") for item in resp.get("items", [])]
        token = resp.get("nextPageToken")
        if not token:
            return rows


def fetch_video(youtube, video_id: str, max_comments: int | None = None) -> list[dict]:
    rows, token = [], None
    while True:
        try:
            resp = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=100,
                pageToken=token,
                textFormat="html",
            ).execute()
        except HttpError as err:
            print(f"[{video_id}] API error: {err}", file=sys.stderr)
            break

        for item in resp.get("items", []):
            top = item["snippet"]["topLevelComment"]["snippet"]
            n_replies = item["snippet"].get("totalReplyCount", 0)
            rows.append(to_row(top, "top", n_replies))
            if n_replies:
                inline = item.get("replies", {}).get("comments", [])
                if len(inline) >= n_replies:
                    rows += [to_row(r["snippet"], "reply", "-") for r in inline]
                else:  # the thread only embeds up to 5 replies
                    rows += fetch_replies(youtube, item["id"])

        print(f"[{video_id}] {len(rows)} comments so far", file=sys.stderr)
        token = resp.get("nextPageToken")
        if not token or (max_comments and len(rows) >= max_comments):
            break
        time.sleep(0.1)

    for i, row in enumerate(rows, start=1):
        row["comment_id"] = i
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {path}", file=sys.stderr)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--video-id", help="single YouTube video ID")
    src.add_argument("--video-list", type=Path, help="CSV with columns video_id,source_file")
    p.add_argument("--out", type=Path, help="output CSV (with --video-id)")
    p.add_argument("--out-dir", type=Path, default=Path("data/raw"), help="output folder (with --video-list)")
    p.add_argument("--max-comments", type=int, default=None)
    args = p.parse_args()

    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        sys.exit("Set YOUTUBE_API_KEY (see .env.example).")
    youtube = build("youtube", "v3", developerKey=key)

    if args.video_id:
        out = args.out or Path(f"data/raw/{args.video_id}.csv")
        write_csv(fetch_video(youtube, args.video_id, args.max_comments), out)
    else:
        with args.video_list.open(encoding="utf-8") as fh:
            for rec in csv.DictReader(fh):
                vid = rec["video_id"].strip()
                if not vid or vid.startswith("#"):
                    continue
                name = rec.get("source_file") or f"{vid}.csv"
                write_csv(fetch_video(youtube, vid, args.max_comments), args.out_dir / name)


if __name__ == "__main__":
    main()
