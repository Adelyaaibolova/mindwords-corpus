"""
Text-level cleaning functions for YouTube comment texts.

Each function does one thing and can be used on its own; `clean()` applies the
default sequence. The pipeline script `clean_comments.py` uses these functions
and logs how many comments each step changed.

What YouTube Data API v3 comment texts typically contain (textDisplay format):
  * HTML entities and tags       I&#39;m fine<br>thanks, <b>bold</b>
  * timestamp links              <a href="...watch?v=ID&amp;t=380">6:20</a>
  * channel emoji links          <a href="UCkszU2.../penguin-blue-waving"></a>
  * reply mentions               @someuser thank you
  * invisible characters         zero-width spaces, bidi marks
"""

from __future__ import annotations

import html
import re

# --- HTML -------------------------------------------------------------------
# <a> elements that only carry a video timestamp (href with &t=NNN)
TIMESTAMP_LINK_RE = re.compile(r'<a\s+href="[^"]*[?&](?:amp;)?t=\d+[^"]*"[^>]*>.*?</a>', re.I | re.S)
# empty <a> elements: custom channel emojis
EMPTY_LINK_RE = re.compile(r'<a\s+[^>]*>\s*</a>', re.I)
BR_RE = re.compile(r"<br\s*/?>", re.I)
TAG_RE = re.compile(r"</?[a-zA-Z][^>]*>")

# --- URLs, mentions, hashtags -------------------------------------------------
URL_RE = re.compile(r"(?:https?://|www\.)\S+", re.I)
# one or more @ followed by a handle; not preceded by a word char (keeps e-mail-like strings intact)
MENTION_RE = re.compile(r"(?<![\w@])@+[\w.\-]+")

# --- timestamps -----------------------------------------------------------------
# H:MM:SS is almost always a video position
LONG_TS_RE = re.compile(r"\b\d{1,2}:\d{2}:\d{2}\b")
# MM:SS only when it is clearly a video reference: at the start of the comment
# (possibly several: "0:01 - 0:30, 1:15"), or as "at 12:30" / "@6:35" (removed with the prefix).
# Mid-sentence 3:16 is left alone, because it is often a Bible verse (Heb 9:27)
# or a clock time (3:00 am).
LEADING_TS_RE = re.compile(r"^(?:\W*\d{1,2}:\d{2}\b(?:\s*(?:-|–|to|,|and)\s*\d{1,2}:\d{2}\b)*)+[\s:.,\-–]*")
AT_TS_RE = re.compile(r"(?:\b[Aa]t\s+|@)\d{1,2}:\d{2}\b(?!\s*[AaPp]\.?[Mm]\b)")

# --- invisible / control characters --------------------------------------------
INVISIBLE_RE = re.compile("[​-‏‪-‮⁠-⁤﻿­]")
WS_RE = re.compile(r"\s+")
LETTER_RE = re.compile(r"[^\W\d_]")  # any letter, any script

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E6-\U0001F1FF"
    "\U0000FE0F\U0000200D"
    "]+"
)


def strip_html(text: str) -> str:
    """Drop timestamp and emoji links, turn <br> into spaces, keep the text of other tags, unescape entities."""
    text = TIMESTAMP_LINK_RE.sub(" ", text)
    text = EMPTY_LINK_RE.sub(" ", text)
    text = BR_RE.sub(" ", text)
    text = TAG_RE.sub("", text)
    # entities can be double-escaped (&amp;#39;)
    for _ in range(2):
        text = html.unescape(text)
    return text


def remove_invisible(text: str) -> str:
    return INVISIBLE_RE.sub("", text)


def remove_urls(text: str) -> str:
    return URL_RE.sub(" ", text)


def remove_mentions(text: str) -> str:
    return MENTION_RE.sub(" ", text)


def remove_timestamps(text: str) -> str:
    text = LONG_TS_RE.sub(" ", text)
    text = AT_TS_RE.sub(" ", text)
    stripped = text.lstrip()
    without_leading = LEADING_TS_RE.sub("", stripped)
    return without_leading if without_leading != stripped else text


def remove_emojis(text: str) -> str:
    return EMOJI_RE.sub(" ", text)


def normalize_whitespace(text: str) -> str:
    return WS_RE.sub(" ", text).strip()


GREETING_RE = re.compile(r"^(?:hello|hi|hey|dear|thank you|thanks)\s+[^,.!]{1,40}[,.!]\s*", re.I)
NON_ALPHA_RE = re.compile(r"[^a-z ]")


def template_key(text: str, length: int = 80) -> str:
    """Normalised form used to spot template replies and spam: greeting/name removed,
    lower-cased, letters only, first `length` characters ("Hello Ritha, Thank you for ..."
    and "Hello Eduardo, Thank you for ..." get the same key)."""
    text = GREETING_RE.sub("", text).lower()
    return WS_RE.sub(" ", NON_ALPHA_RE.sub("", text)).strip()[:length]


def has_letters(text: str) -> bool:
    return bool(LETTER_RE.search(text))


# Order matters: HTML first (it contains the URLs and timestamp links),
# invisible characters before mentions (they often sit right before "@"),
# timestamps before mentions ("@6:35" is a timestamp, not a user handle).
DEFAULT_STEPS = (
    strip_html,
    remove_invisible,
    remove_urls,
    remove_timestamps,
    remove_mentions,
    remove_timestamps,  # again: "@user 2:30 so true" only starts with 2:30 once the handle is gone
    normalize_whitespace,
)


def clean(text, steps=DEFAULT_STEPS) -> str:
    text = "" if text is None else str(text)
    for step in steps:
        text = step(text)
    return text
