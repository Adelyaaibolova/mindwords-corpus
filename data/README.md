# Data

## Included

| Path | Content |
|---|---|
| `videos.csv` | the 14 source videos, mapped to the file names used in the project. `video_id` is left empty — fill it in to re-collect with `scripts/collect_comments.py --video-list`. Rows marked *(to verify)* / *(to fill in)* need checking. |
| `derived/source_stats.csv` | comments, top-level vs replies, tokens, likes and date range per source file |
| `derived/word_frequencies.csv` | top 2,000 word forms (lower-cased, deduplicated corpus) with counts and per-million |
| `derived/headword_by_source.csv` | frequency of the 11 dictionary headwords per source file |
| `derived/cleaning_log.csv` | what each cleaning step changed or removed |
| `derived/repeated_texts.csv` | template replies and spam removed as repeats: normalised first 80 characters and number of occurrences per video |
| `derived/figures/` | charts used in the main README |

All derived files are regenerated with:

```bash
python scripts/corpus_stats.py data/raw/corpus_clean.csv --out data/derived
```

## Not included: `raw/`

`raw/` holds the per-video CSVs, `combined_filtered.csv` and `corpus_clean.csv` on your own machine and is git-ignored. Comment texts are user-generated content collected through the YouTube Data API; its Terms of Service restrict storing and redistributing that data, so the texts are not published. Rebuild them with the scripts (see the main README).

### Schema of `combined_filtered.csv`

| Column | Description |
|---|---|
| `comment_id` | running number |
| `type` | `top` (top-level comment) or `reply` |
| `replycount` | number of replies for top-level comments, `-` for replies |
| `likecount` | likes at collection time |
| `date`, `time` | publication date (YYYY-MM-DD) and time (HH:MM, UTC) |
| `emojis` | emojis extracted from the comment |
| `comment` | comment text |
| `source_file` | per-video file the comment came from |

Snapshot used in the project: 79,646 rows, comments dated 2014-12-23 to 2026-03-25, collected in March 2026.
