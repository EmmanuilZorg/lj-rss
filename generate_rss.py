from feedgen.feed import FeedGenerator

def generate_rss(posts, feed_title, feed_link, feed_description):
    fg = FeedGenerator()
    fg.title(feed_title)
    fg.link(href=feed_link)
    fg.description(feed_description)
    fg.language('en')

    for post in posts:
        fe = fg.add_entry()
        fe.title(post["title"])
        fe.link(href=post["link"])
        fe.pubDate(post["pubDate"])
        fe.description(post["description"])

    return fg.rss_str(pretty=True)

if __name__ == "__main__":
    import sys
    import fetch_posts

    url = sys.argv[1] if len(sys.argv) > 1 else "https://dekodeko.livejournal.com/"
    posts = fetch_posts.fetch_posts(url)
    rss_xml = generate_rss(posts,
                           feed_title="LiveJournal RSS Feed",
                           feed_link=url,
                           feed_description="RSS feed generated from LiveJournal posts")

    with open("feed.xml", "wb") as f:
        f.write(rss_xml)
