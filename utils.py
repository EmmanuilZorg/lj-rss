import json
import os

def load_existing_posts(path='posts.json'):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_posts(posts, path='posts.json'):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def get_new_posts(all_posts, known_posts):
    known_links = {p['link'] for p in known_posts}
    return [p for p in all_posts if p['link'] not in known_links]