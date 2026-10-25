"""
Build the MindWords dictionary page (docs/index.html) from dictionary/entries.json.

The page is a single static HTML file, so it works on GitHub Pages and when
opened directly from disk. Edit entries.json, then rebuild:

    python scripts/build_dictionary.py
"""

from __future__ import annotations

import csv
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "dictionary" / "entries.json"
VIDEOS = ROOT / "data" / "videos.csv"
OUT = ROOT / "docs" / "index.html"

LANGS = [("ar", "Arabic", "rtl"), ("de", "German", "ltr"), ("fr", "French", "ltr"), ("es", "Spanish", "ltr")]


def band(per_million: float) -> int:
    """Frequency band 1-5 from occurrences per million tokens."""
    for limit, b in ((300, 5), (100, 4), (40, 3), (20, 2)):
        if per_million >= limit:
            return b
    return 1


BAND_LABEL = {5: "very frequent", 4: "frequent", 3: "common", 2: "less common", 1: "rare"}


def load_sources() -> dict[str, str]:
    with VIDEOS.open(encoding="utf-8") as fh:
        return {r["source_file"]: r["creator"] for r in csv.DictReader(fh)}


def render_entry(e: dict, sources: dict[str, str]) -> str:
    b = band(e["per_million"])
    dots = "".join(f'<span class="dot{" on" if i < b else ""}"></span>' for i in range(5))
    examples = "\n".join(
        f'<li><q>{escape(x["text"])}</q><cite>{escape(sources.get(x["source"], x["source"]))}</cite></li>'
        for x in e["examples"]
    )
    collocs = "".join(f"<li>{escape(c)}</li>" for c in e["collocations"])
    trans = "\n".join(
        f'<div><dt>{name}</dt><dd lang="{code}" dir="{d}">{escape(e["translations"][code])}</dd></div>'
        for code, name, d in LANGS if code in e["translations"]
    )
    quote = ""
    if e.get("quote"):
        quote = (f'<blockquote class="quote"><p>{escape(e["quote"]["text"])}</p>'
                 f'<footer>{escape(e["quote"]["by"])}</footer></blockquote>')
    search = " ".join([e["headword"], *e["collocations"], *e["translations"].values(), e["domain"]]).lower()
    return f"""
<article class="entry" id="{e['id']}" data-search="{escape(search)}" data-domain="{escape(e['domain'])}">
  <header class="entry-head">
    <h2 class="hw">{escape(e['headword'])}</h2>
    <p class="pos">{escape(e['pos'])}</p>
    <p class="freq" title="{e['per_million']} per million tokens">
      <span class="dots" aria-hidden="true">{dots}</span>
      <span>{BAND_LABEL[b]}, {e['per_million']:g} per million</span>
    </p>
  </header>
  <p class="def">{escape(e['definition'])}</p>
  <section class="block">
    <h3>From the comments</h3>
    <ul class="examples">{examples}</ul>
  </section>
  <section class="block">
    <h3>Common word groups</h3>
    <ul class="collocs">{collocs}</ul>
  </section>
  <section class="block note">
    <h3>Usage note</h3>
    <p>{escape(e['note'])}</p>
  </section>
  <section class="block">
    <h3>Translations</h3>
    <dl class="trans">{trans}</dl>
  </section>
  {quote}
</article>"""


def render(data: dict, sources: dict[str, str]) -> str:
    meta, entries = data["meta"], data["entries"]
    nav = []
    for d in data["domains"]:
        words = "".join(f'<li><a href="#{e["id"]}">{escape(e["headword"])}</a></li>'
                        for e in entries if e["domain"] == d)
        nav.append(f'<li class="nav-domain"><span>{escape(d)}</span><ul>{words}</ul></li>')
    body = "\n".join(render_entry(e, sources) for e in entries)
    authors = ", ".join(meta["authors"][:-1]) + " and " + meta["authors"][-1]
    return TEMPLATE.format(
        title=escape(meta["title"]),
        subtitle=escape(meta["subtitle"]),
        n=len(entries),
        n_domains=len(data["domains"]),
        nav="\n".join(nav),
        entries=body,
        corpus=escape(meta["corpus"]),
        authors=escape(authors),
        course=escape(meta["course"]),
        repo=escape(meta["repo"]),
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} dictionary</title>
<meta name="description" content="{subtitle}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&family=Noto+Naskh+Arabic:wght@500&display=swap" rel="stylesheet">
<style>
:root {{
  --paper: #F3F4EF;
  --sheet: #FBFBF8;
  --ink: #1C2033;
  --muted: #5A5F6E;
  --rule: #D7D9D0;
  --teal: #1F6B66;
  --teal-soft: #DCEBE8;
  --plum: #74476A;
  --plum-soft: #F0E5EC;
  --serif: "Literata", Georgia, serif;
  --sans: "Atkinson Hyperlegible", system-ui, sans-serif;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --paper: #14171E; --sheet: #1A1E27; --ink: #E5E7EC; --muted: #A2A7B4; --rule: #2C313D;
    --teal: #74C3B9; --teal-soft: #1F3533; --plum: #D7A2C6; --plum-soft: #34232F;
  }}
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; scroll-padding-top: 1.5rem; }}
@media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} }}
body {{
  margin: 0; background: var(--paper); color: var(--ink);
  font: 1.0625rem/1.6 var(--sans);
}}
a {{ color: var(--teal); }}
:focus-visible {{ outline: 3px solid var(--teal); outline-offset: 2px; border-radius: 3px; }}

.masthead {{ max-width: 72rem; margin: 0 auto; padding: 3.5rem 1.25rem 2rem; }}
.masthead h1 {{
  font: 600 clamp(3rem, 9vw, 6rem)/0.95 var(--serif); letter-spacing: -0.02em; margin: 0;
}}
.masthead .sub {{ font: italic 1.25rem/1.4 var(--serif); color: var(--muted); margin: 0.75rem 0 1.75rem; max-width: 36rem; }}
.search {{ display: flex; flex-direction: column; gap: 0.4rem; max-width: 34rem; }}
.search label {{ font-size: 0.95rem; color: var(--muted); }}
.search input {{
  font: 1.25rem var(--serif); color: var(--ink); background: var(--sheet);
  border: 2px solid var(--rule); border-radius: 10px; padding: 0.7rem 0.9rem;
}}
.search input:focus {{ border-color: var(--teal); outline: none; box-shadow: 0 0 0 3px var(--teal-soft); }}
.count {{ font-size: 0.95rem; color: var(--muted); margin: 0.6rem 0 0; }}

.layout {{ max-width: 72rem; margin: 0 auto; padding: 0 1.25rem 4rem; display: grid; grid-template-columns: 13.5rem 1fr; gap: 3rem; }}
nav.index {{ position: sticky; top: 1.5rem; align-self: start; max-height: calc(100vh - 3rem); overflow: auto; }}
nav.index ul {{ list-style: none; margin: 0; padding: 0; }}
.nav-domain {{ margin-bottom: 1.1rem; }}
.nav-domain > span {{ display: block; font-size: 0.85rem; color: var(--muted); margin-bottom: 0.2rem; }}
.nav-domain a {{ display: block; font: 1.05rem/1.7 var(--serif); color: var(--ink); text-decoration: none; padding-left: 0.6rem; border-left: 2px solid var(--rule); }}
.nav-domain a:hover {{ border-left-color: var(--teal); color: var(--teal); }}
.nav-domain a.dim {{ opacity: 0.35; }}

main {{ min-width: 0; }}
.entry {{ background: var(--sheet); border: 1px solid var(--rule); border-radius: 14px; padding: 2rem 2.25rem 2.25rem; margin-bottom: 2rem; max-width: 46rem; }}
.entry-head {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 0.4rem 1rem; border-bottom: 1px solid var(--rule); padding-bottom: 1rem; }}
.hw {{ font: 600 clamp(2.1rem, 5vw, 2.9rem)/1.05 var(--serif); margin: 0; letter-spacing: -0.01em; }}
.pos {{ font: italic 1.05rem var(--serif); color: var(--muted); margin: 0; }}
.freq {{ display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: var(--muted); margin: 0 0 0 auto; }}
.dots {{ display: inline-flex; gap: 3px; }}
.dot {{ width: 9px; height: 9px; border-radius: 50%; border: 1.5px solid var(--teal); }}
.dot.on {{ background: var(--teal); }}
.def {{ font: 1.2rem/1.55 var(--serif); margin: 1.2rem 0 0.4rem; }}

.block {{ margin-top: 1.6rem; }}
.block h3 {{ font: 700 0.95rem var(--sans); color: var(--muted); margin: 0 0 0.6rem; }}
.examples {{ list-style: none; margin: 0; padding: 0; }}
.examples li {{ border-left: 3px solid var(--teal-soft); padding: 0.15rem 0 0.15rem 0.9rem; margin-bottom: 0.75rem; }}
.examples q {{ font: italic 1.05rem/1.5 var(--serif); quotes: none; }}
.examples cite {{ display: block; font: normal 0.82rem var(--sans); color: var(--muted); margin-top: 0.15rem; }}
.collocs {{ list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 0.45rem; }}
.collocs li {{ background: var(--teal-soft); color: var(--ink); border-radius: 999px; padding: 0.2rem 0.75rem; font-size: 0.95rem; }}
.note {{ background: var(--plum-soft); border-radius: 10px; padding: 0.9rem 1.1rem; }}
.note h3 {{ color: var(--plum); }}
.note p {{ margin: 0; }}
.trans {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.6rem 1.2rem; margin: 0; }}
.trans dt {{ font-size: 0.82rem; color: var(--muted); }}
.trans dd {{ margin: 0; font: 1.05rem var(--serif); }}
.trans dd[lang="ar"] {{ font-family: "Noto Naskh Arabic", var(--serif); font-size: 1.2rem; text-align: left; line-height: 1.4; }}
.quote {{ margin: 1.8rem 0 0; padding-top: 1.2rem; border-top: 1px dashed var(--rule); }}
.quote p {{ font: italic 1.1rem/1.5 var(--serif); margin: 0; }}
.quote footer {{ font-size: 0.85rem; color: var(--muted); margin-top: 0.3rem; }}
.empty {{ font: 1.15rem var(--serif); color: var(--muted); max-width: 46rem; }}

.about {{ border-top: 1px solid var(--rule); max-width: 72rem; margin: 0 auto; padding: 2rem 1.25rem 3rem; color: var(--muted); font-size: 0.95rem; }}
.about p {{ max-width: 46rem; margin: 0 0 0.6rem; }}

@media (max-width: 52rem) {{
  .layout {{ grid-template-columns: 1fr; gap: 1.5rem; }}
  nav.index {{ position: static; max-height: none; }}
  nav.index > ul, .nav-domain ul {{ display: flex; flex-wrap: wrap; gap: 0.4rem; }}
  .nav-domain {{ display: contents; }}
  .nav-domain > span {{ display: none; }}
  .nav-domain a {{ border: 1px solid var(--rule); border-radius: 999px; padding: 0.1rem 0.7rem; font-size: 0.95rem; background: var(--sheet); }}
  .trans {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .entry {{ padding: 1.4rem 1.2rem 1.6rem; }}
  .freq {{ margin-left: 0; width: 100%; }}
}}
</style>
</head>
<body>
<header class="masthead">
  <h1>{title}</h1>
  <p class="sub">{subtitle}: what people really mean when they write about anxiety, discipline or healing under a video.</p>
  <div class="search" role="search">
    <label for="q">Look up a word, phrase or translation</label>
    <input id="q" type="search" placeholder="anxiety, mindset, Achtsamkeit…" autocomplete="off">
  </div>
  <p class="count" id="count" aria-live="polite">{n} entries in {n_domains} domains</p>
</header>

<div class="layout">
  <nav class="index" aria-label="All entries">
    <ul>
{nav}
    </ul>
  </nav>
  <main>
{entries}
    <p class="empty" id="empty" hidden></p>
  </main>
</div>

<footer class="about">
  <p>Built from {corpus}. Examples are quoted as written, including spelling and emojis; the name under each example is the video it was posted under. Frequencies count all word forms.</p>
  <p>By {authors} &middot; {course}. Data, code and report: <a href="{repo}">{repo}</a>.</p>
</footer>

<script>
(function () {{
  var input = document.getElementById("q");
  var entries = Array.prototype.slice.call(document.querySelectorAll(".entry"));
  var links = Array.prototype.slice.call(document.querySelectorAll("nav.index a"));
  var count = document.getElementById("count");
  var empty = document.getElementById("empty");
  var total = count.textContent;
  input.addEventListener("input", function () {{
    var q = input.value.trim().toLowerCase();
    var shown = 0;
    entries.forEach(function (el) {{
      var hit = !q || el.dataset.search.indexOf(q) !== -1;
      el.hidden = !hit;
      if (hit) shown++;
      links.forEach(function (a) {{
        if (a.getAttribute("href") === "#" + el.id) a.classList.toggle("dim", !hit);
      }});
    }});
    count.textContent = q ? shown + (shown === 1 ? " entry" : " entries") + " match \\u201c" + input.value.trim() + "\\u201d" : total;
    empty.hidden = shown !== 0;
    empty.textContent = shown ? "" : "No entry matches \\u201c" + input.value.trim() + "\\u201d. Try a headword from the list, or a translation such as Angst or empatía.";
  }});
}})();
</script>
</body>
</html>
"""


def main() -> None:
    data = json.loads(ENTRIES.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(data, load_sources()), encoding="utf-8")
    print(f"{len(data['entries'])} entries -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
