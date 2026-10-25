"""Shared text cleaning for YouTube comment texts."""

import html
import re

TAG_RE = re.compile(r"<[^>]+>")


def clean(text) -> str:
    """Replace <br> with a space, strip other HTML tags, unescape entities (&#39; -> ')."""
    text = str(text).replace("<br>", " ")
    return html.unescape(TAG_RE.sub("", text)).strip()
