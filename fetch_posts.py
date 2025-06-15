import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_posts(url):
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')

    posts = []
    dts = soup.select("dt.entry-title")
    for dt in dts:
        a = dt.select_one("a.subj-link")
        if not a:
            continue
        title = a.get_text(strip=True) or "(no title)"
        link = a['href']

        date_abbr = dt.find_next_sibling("dd").select_one("abbr.updated")
        dt_obj = datetime.fromisoformat(date_abbr['title']) if date_abbr else datetime.utcnow()
        pubDate = dt_obj.strftime('%a, %d %b %Y %H:%M:%S %z')

        content_dd = dt.find_next_sibling("dd.entry-text")
        content_div = content_dd.select_one("div.entry-content") or content_dd.select_one("div")
        description = content_div.decode_contents() if content_div else "(no content)"

        posts.append({
            "title": title,
            "link": link,
            "pubDate": pubDate,
            "description": description
        })

    return posts
