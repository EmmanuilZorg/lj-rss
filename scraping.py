import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_posts(url):
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')

    posts = []
    for entry in soup.select('.entry-wrap, .b-singlepost-body'):  # селекторы нужно уточнить под конкретный блог
        a = entry.find('a', href=True)
        if not a: continue
        title = a.get_text(strip=True)
        link = a['href']
        date_tag = entry.find('time')
        pubDate = date_tag['datetime'] if date_tag and date_tag.has_attr('datetime') else datetime.utcnow().isoformat()
        desc = entry.get_text(strip=True)[:300]
        posts.append({
            "title": title,
            "link": link,
            "pubDate": pubDate,
            "description": desc
        })
    return posts