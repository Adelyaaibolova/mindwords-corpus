import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import textclean as tc  # noqa: E402


def test_html_entities_and_breaks():
    assert tc.clean("I&#39;m fine<br>thanks") == "I'm fine thanks"
    assert tc.clean("so &quot;true&quot; &amp; real") == 'so "true" & real'
    assert tc.clean("double &amp;#39; escaped") == "double ' escaped"


def test_tags_keep_inner_text():
    assert tc.clean("<b>single motherhood</b> is hard") == "single motherhood is hard"


def test_timestamp_and_emoji_links_removed():
    raw = 'FFW to <a href="https://www.youtube.com/watch?v=LnJwH&amp;t=265">4:25</a> great'
    assert tc.clean(raw) == "FFW to great"
    assert tc.clean('love it <a href="UCkszU2WH9/penguin-blue"></a>') == "love it"


def test_urls_removed():
    assert tc.clean("watch https://youtu.be/abc?si=1 now") == "watch now"
    assert tc.clean("see www.example.com.") == "see"


def test_mentions_removed():
    assert tc.clean("@grimshady Thanks brother") == "Thanks brother"
    assert tc.clean("@@flawed thank ya") == "thank ya"
    assert tc.clean("​@Jackinn1t messed up phone") == "messed up phone"
    assert tc.clean("@Валентини17 thank you") == "thank you"


def test_email_like_kept():
    assert "me@mail.com" in tc.clean("write me@mail.com")


def test_video_timestamps_removed():
    assert tc.clean("3:00 Pine tree vs oak tree") == "Pine tree vs oak tree"
    assert tc.clean("0:01 - 0:30 so good") == "so good"
    assert tc.clean("Powerful lesson at 16:10.") == "Powerful lesson ."
    assert tc.clean("Narcissistic behavior 1:35:55") == "Narcissistic behavior"
    assert tc.clean("@6:35 my woman") == "my woman"
    assert tc.clean("@user 2:30 so true") == "so true"


def test_bible_verses_and_clock_times_kept():
    assert tc.clean("as it is appointed (Heb 9:27)") == "as it is appointed (Heb 9:27)"
    assert tc.clean("I wake up at 5:30 am every day") == "I wake up at 5:30 am every day"


def test_invisible_characters():
    assert tc.clean("I love this ‏‪ part‬") == "I love this part"


def test_has_letters():
    assert not tc.has_letters("❤❤ 16:00")
    assert tc.has_letters("ok")
    assert tc.has_letters("спасибо")


def test_emojis_optional():
    assert tc.clean("Nice video😍🔥") == "Nice video😍🔥"
    assert tc.normalize_whitespace(tc.remove_emojis("Nice video😍🔥 wow")) == "Nice video wow"
