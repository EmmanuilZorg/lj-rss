import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import yaml
import sys
import urllib.parse # To handle relative URLs

# Load configuration from config.yaml
try:
    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError:
    print("Error: config.yaml not found. Please create one.")
    sys.exit(1)
except yaml.YAMLError as e:
    print(f"Error parsing config.yaml: {e}")
    sys.exit(1)

# Define standard headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0'
}

# Process each blog configured in the YAML file
for item in config.get('lj_blogs', []): # Use .get() with default to prevent error if lj_blogs is missing
    url = item.get('url')
    rss_filename = item.get('rss_filename')
    rss_title = item.get('rss_title')
    rss_description = item.get('rss_description')

    # Basic validation for required fields
    if not url or not rss_filename or not rss_title or not rss_description:
        print(f"Skipping an entry in config.yaml due to missing required fields (url, rss_filename, rss_title, rss_description).")
        continue

    print(f"Processing: {rss_title} ({url})")

    # Fetch the blog page content
    try:
        r = requests.get(url, headers=headers, timeout=10) # Added timeout
        r.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        continue # Move to the next blog on error

    # Parse the HTML content
    try:
        soup = BeautifulSoup(r.text, 'lxml')
    except Exception as e: # Catch potential parsing errors
        print(f"Error parsing HTML for {url}: {e}")
        continue

    # Initialize FeedGenerator
    fg = FeedGenerator()
    fg.id(url)
    fg.title(rss_title)
    fg.author({'name': 'LJ-RSS'}) # Consider making author configurable
    fg.link(href=url, rel='alternate')
    fg.subtitle(rss_description)
    fg.language('ru') # Assuming Russian is standard for LJ, make configurable if needed

    # Find all post containers using the new class 'j-e-root'
    posts = soup.find_all(class_='j-e-root')

    if not posts:
        print(f"Warning: No posts found for {url} with class 'j-e-root'. Check URL or class name.")

    # Process each post found
    for post in posts:
        # Find the title container using class 'j-e-title'
        title_container = post.find(class_='j-e-title')
        if not title_container:
            print(f"Warning: Skipping a post for {url} due to missing title container ('j-e-title').")
            continue

        # Find the link tag (<a>) inside the title container
        title_link = title_container.find('a')
        if not title_link or not title_link.get('href'):
             print(f"Warning: Skipping a post for {url} due to missing title link ('a') or href attribute inside title container.")
             continue

        # Extract post URL and title text
        post_url_relative = title_link['href']
        post_url = urllib.parse.urljoin(url, post_url_relative) # Make URL absolute
        post_title = title_link.text.strip()

        # Find the body element using class 'j-e-text'
        body_element = post.find(class_='j-e-text')
        # If the body is not found, set post_body to empty string
        if not body_element:
            print(f"Warning: Post '{post_title}' ({post_url}) missing body element ('j-e-text'). Body will be empty.")
            post_body = ""
        else:
            post_body = body_element.text.strip()

        # Add the post as an entry to the RSS feed
        fe = fg.add_entry()
        fe.id(post_url) # Use the absolute URL as the unique ID
        fe.title(post_title)
        fe.link(href=post_url)
        fe.description(post_body) # Consider using content() if HTML is desired

    # Save the generated RSS feed to a file
    try:
        fg.rss_file(rss_filename, pretty=True)
        print(f"Successfully generated RSS feed: {rss_filename}")
    except IOError as e:
        print(f"Error writing RSS file {rss_filename}: {e}")
