# MindWords — a corpus-based dictionary of mental health discourse on YouTube

![Python](https://img.shields.io/badge/python-3.10%2B-3B6EA8)
![Data](https://img.shields.io/badge/source-YouTube%20Data%20API%20v3-c4302b)
![Tools](https://img.shields.io/badge/analysis-Sketch%20Engine%20%7C%20CQPweb-555)
![License](https://img.shields.io/badge/code-MIT-green) ![License](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey)

A specialised English corpus built from the comment sections of 14 YouTube videos on mental health and self-improvement, and a learner's dictionary derived from it. Course project, *Computational Linguistics 2025/26* (EMLex), by **Adelya Aibolova, Souhaila Derbal and Salah Eddine Nacer Benkhemis**.

> **Research question.** Which lexical units characterise mental-health and self-improvement discourse on YouTube, and how does a lay audience actually use them in spontaneous online writing?

## Highlights

| | |
|---|---|
| **Raw collection** | 120,826 comments from 14 videos (TEDx talks, podcasts, mental-health educators, motivational speakers, influencers) |
| **After filtering** | 79,646 English comments (53,980 top-level, 25,666 replies), ≈ 2.5 M word tokens |
| **Sketch Engine corpus** | two-video subcorpus, 623,452 tokens |
| **Dictionary** | 11 entries in 5 domains, with corpus examples, collocations and translations into Arabic, German, French and Spanish |

### Findings in brief

- **Self-directed *empathy*.** In standard English empathy is aimed at others; in the corpus it is overwhelmingly reflexive — *give yourself empathy and speak up*, *I was not showing myself empathy* — i.e. a synonym for self-compassion.
- ***Discipline* as liberation.** The Visual Word Sketch for *discipline is a …* yields *gateway, engine, freedom*, plus the bodily metaphor *discipline muscle*. In the reference corpus (English Web 2021) the same word is institutional: *academic, fiscal, strict*; *impose, enforce, instill*.
- ***Anxiety* is clinical, *healing* is spiritual.** Word Sketch Difference shows *anxiety* with varied clinical modifiers (*social, debilitating, constant*) and compounds (*anxiety disorder/attack*), whereas *healing* takes only *spiritual* and combines with *art, medicine, herb, frequency*. A counter-narrative also appears: *Anxiety is not an enemy*.
- **Creative compounding.** A CQP query `[pos="N.*"][word="anxiety"]` surfaces *separation, job, death, shame anxiety* and the coinage *trickle-down anxiety*.
- **Productive *self-*.** *self-education, self-discipline, self-worth, self-motivation, self-hate* — all keyword-level, all tied to personal responsibility.
- **Comment sections are multilingual.** Arabic, Portuguese, Dutch and Spanish tokens reached the keyword list even after filtering.

The full write-up (German) is in [`report/Forschungsbericht_MindWords_de.md`](report/Forschungsbericht_MindWords_de.md); sample entries are in [`docs/dictionary_sample_entries.md`](docs/dictionary_sample_entries.md).

## Corpus

![Comments per source file](data/derived/figures/comments_per_source.png)

The 14 videos and their files are listed in [`data/videos.csv`](data/videos.csv). Descriptive statistics per file are in [`data/derived/source_stats.csv`](data/derived/source_stats.csv).

![Headword frequencies](data/derived/figures/headwords_per_million.png)

### Data quality notes

Found while preparing this repository (details in [`data/derived/duplicates.csv`](data/derived/duplicates.csv)):

- `Huberman_Lab.csv` and `dr_paul.csv` contain the **same 3,980 comments** — the Paul Conti episode on the Huberman Lab channel was downloaded twice. The derived frequency tables drop exact duplicates (4,381 rows in total).
- About 9,000 comments still contained HTML entities and tags from the API (`&#39;`, `<br>`); the scripts now clean these.
- Headword counts are skewed by single videos: e.g. 450 of 654 *empathy/empathic* hits come from one Kati Morton video (*Are You a Narcissist?*). See [`headword_by_source.csv`](data/derived/headword_by_source.csv).

### Why the raw comments are not in this repository

The comment texts are user-generated content obtained under the YouTube API Terms of Service, which restrict redistribution. The repository therefore ships the **code to rebuild the corpus** and **aggregate data** (frequencies, per-source statistics), not the comments themselves. See [`data/README.md`](data/README.md).

## Reproducing the corpus

```bash
git clone https://github.com/Adelyaaibolova/mindwords-corpus.git
cd mindwords-corpus
pip install -r requirements.txt
cp .env.example .env          # then put your own YouTube Data API key in .env

# 1. collect comments (fill in video_id in data/videos.csv first)
python scripts/collect_comments.py --video-list data/videos.csv --out-dir data/raw/

# 2. combine, clean HTML, drop Arabic-script comments (--langdetect also drops other languages)
python scripts/filter_and_combine.py --in-dir data/raw --out data/raw/combined_filtered.csv

# 3. descriptive statistics and figures -> data/derived/
python scripts/corpus_stats.py data/raw/combined_filtered.csv --out data/derived

# 4. export for Sketch Engine / CQPweb (one <doc> per comment with metadata)
python scripts/export_sketchengine.py data/raw/combined_filtered.csv corpus.txt --dedupe
python scripts/export_sketchengine.py data/raw/combined_filtered.csv subset.txt --sources out__15_.csv jordan.csv   # any subset of files
```

The exported file can be uploaded to Sketch Engine as plain text; the `<doc>` attributes (`source`, `type`, `likes`, `year`) become text types for building subcorpora — which also makes it easy to address the imbalance noted above.

## Methods

| Tool | Used for |
|---|---|
| Sketch Engine — Keywords | candidate selection against English Web 2021 |
| Word Sketch / Visual Word Sketch | collocational profiles, metaphors (*discipline*, *self-education*, *anxiety*) |
| Word Sketch Difference | *anxiety* vs *healing* |
| Concordance (GDEX-sorted) + distribution | dictionary examples, self-directed *empathy* |
| Thesaurus | near-synonyms of *mindset* |
| CQPweb | POS query for noun + *anxiety* compounds |

## Repository structure

```
mindwords-corpus/
├── README.md
├── data/
│   ├── README.md               # what is and isn't included, column schema
│   ├── videos.csv              # the 14 source videos
│   ├── raw/                    # local only, git-ignored
│   └── derived/                # shareable statistics + figures
├── docs/
│   └── dictionary_sample_entries.md
├── report/
│   └── Forschungsbericht_MindWords_de.md
├── scripts/
│   ├── collect_comments.py     # YouTube Data API v3 -> CSV
│   ├── filter_and_combine.py   # merge, clean, language filter
│   ├── corpus_stats.py         # statistics + figures
│   ├── export_sketchengine.py  # Sketch Engine / CQPweb text export
│   └── textclean.py
├── requirements.txt
├── .env.example
├── CITATION.cff
└── LICENSE
```

## Limitations

- **Imbalance.** Only two of the 14 videos went into the Sketch Engine corpus, so individual videos dominate some patterns (visible in the distribution of *empathy*).
- **Language filtering** happened after collection and only targeted Arabic script; other languages remain in small numbers.
- **API artefacts** (numbers, timestamps) appear in some concordance lines.
- Frequencies in `data/derived/` are computed with a simple regex tokenizer over all 14 files and are not directly comparable with Sketch Engine figures for the two-video subcorpus.

## Authors

- Adelya Aibolova — [@Adelyaaibolova](https://github.com/Adelyaaibolova)
- Souhaila Derbal
- Salah Eddine Nacer Benkhemis

## License

Code: [MIT](LICENSE). Report, dictionary entries and derived data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). YouTube comment texts remain the property of their authors and are not distributed here.

If you use this work, please cite it via [`CITATION.cff`](CITATION.cff).
