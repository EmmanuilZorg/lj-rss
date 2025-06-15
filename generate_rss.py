from feedgen.feed import FeedGenerator
from datetime import datetime
from scraping import fetch_posts
from utils import load_existing_posts, save_posts, get_new_posts
from email.utils import format_datetime

url = 'https://example.livejournal.com/'  # TODO: заменить на реальный URL
feed_url = 'https://yourusername.github.io/feed.xml'

all_fetched = fetch_posts(url)
known = load_existing_posts()
new_posts = get_new_posts(all_fetched, known)

if new_posts:
    updated = new_posts + known
    updated = sorted(updated, key=lambda x: x['pubDate'], reverse=True)[:50]

    fg = FeedGenerator()
    fg.title("LiveJournal Feed")
    fg.link(href=feed_url, rel='self')
    fg.description("Автоматическая RSS-лента")

    for post in updated:
        fe = fg.add_entry()
        fe.title(post['title'])
        fe.link(href=post['link'])
        fe.pubDate(format_datetime(datetime.fromisoformat(post['pubDate'])))
        fe.description(post['description'])

    with open("feed.xml", "wb") as f:
        f.write(fg.rss_str(pretty=True))

    save_posts(updated)