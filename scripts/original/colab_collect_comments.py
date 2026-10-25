"""
Original collection script used in the course project (Google Colab, spring 2026).

Kept as it was run, with two changes only:
  * the API key is read from the environment instead of being written in the code
  * the missing imports at the top were added so the file runs on its own

Known issue (found when preparing the repository): top-level comments are requested
with textFormat=plainText, but replies (comments.list in fetch_replies) are not, so the
API returns them as HTML. That is why every comment containing &#39; or <br> in
combined_filtered.csv is a reply. scripts/collect_comments.py and
scripts/clean_comments.py fix this.

Output: tab-separated out.csv with
comment_id, type, replycount, likecount, date, time, emojis, comment
"""

import json
import os
import re
from urllib.request import urlopen

api_key = os.environ["YOUTUBE_API_KEY"]  # originally hard-coded; never commit a key
youtube_id = '6YzZWKdTJMs'


def clean_text(text):
    text = re.sub('[\s]+', ' ', text)
    return text

def extract_emojis(text):
    emojis = re.sub('[^\u263a-\U0001f645 \U00010000-\U0010ffff]', '', text)
    emojis = re.sub(' ', '', emojis)
    return emojis

def fetch_replies(api_key, parent_id):
    """ Holt ALLE Replies zu einem Kommentar via comments.list """
    replies = []
    url = f"https://www.googleapis.com/youtube/v3/comments?key={api_key}&part=snippet&parentId={parent_id}&maxResults=100"
    while True:
        try:
            response = urlopen(url)
            json_data = json.loads(response.read())

            for reply in json_data['items']:
                r = reply['snippet']
                replies.append({
                    "text": clean_text(r['textDisplay']),
                    "date": re.sub('T.*', '', r['publishedAt']),
                    "time": re.sub('.*T(\d\d:\d\d):\d\dZ', r'\1', r['publishedAt']),
                    "likecount": r['likeCount'],
                    "emojis": extract_emojis(r['textDisplay'])
                })

            if 'nextPageToken' in json_data:
                url = f"https://www.googleapis.com/youtube/v3/comments?key={api_key}&part=snippet&parentId={parent_id}&maxResults=100&pageToken={json_data['nextPageToken']}"
            else:
                break
        except Exception as e:
            print("Fehler beim Laden von Replies:", e)
            break
    return replies


# ------------------- Hauptprogramm -------------------

url = 'https://www.googleapis.com/youtube/v3/commentThreads?key='+api_key+'&textFormat=plainText&part=snippet&videoId='+youtube_id+'&maxResults=100'
raw_url = url
last_nextPageToken = '-'

string_to_file = 'comment_id\ttype\treplycount\tlikecount\tdate\ttime\temojis\tcomment\n'
comment_id = 1
print('type\treplies\tlikes\tdate\t\ttime\tid\temojis\tcomment')

while (comment_id < 10000):
    try:
        response = urlopen(url)
        json_data = json.loads(response.read())

        for item in json_data['items']:
            top = item['snippet']['topLevelComment']['snippet']
            comment_text = clean_text(top['textDisplay'])

            date = re.sub('T.*', '', top['publishedAt'])
            time = re.sub('.*T(\d\d:\d\d):\d\dZ', r'\1', top['publishedAt'])
            likecount = top['likeCount']
            replycount = item['snippet']['totalReplyCount']
            emojis = extract_emojis(comment_text)
            comment_id_str = str(comment_id)

            # ---------- Top-Level-Kommentar ----------
            print(comment_text)
            string_to_file += f"{comment_id_str}\ttop\t{replycount}\t{likecount}\t{date}\t{time}\t{emojis}\t{comment_text}\n"
            comment_id += 1

            # ---------- Replies (ALLE über comments.list) ----------
            if replycount > 0:
                all_replies = fetch_replies(api_key, item['snippet']['topLevelComment']['id'])
                for r in all_replies:
                    print("   ↳", r["text"])
                    string_to_file += f"{comment_id}\treply\t-\t{r['likecount']}\t{r['date']}\t{r['time']}\t{r['emojis']}\t{r['text']}\n"
                    comment_id += 1

        # ---------- Pagination bei den Top-Level-Kommentaren ----------
        if 'nextPageToken' in json_data:
            nextPageToken = json_data['nextPageToken']
            url = raw_url + '&pageToken='+nextPageToken
        if (nextPageToken == last_nextPageToken):
            break
        last_nextPageToken = nextPageToken

    except Exception as e:
        print("Fehler:", e)
        break

string_to_file = string_to_file.strip()
with open('/content/sample_data/out.csv', 'w') as writefile:
    writefile.write(string_to_file)
