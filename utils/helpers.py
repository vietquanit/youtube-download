import re

def sanitize_filename(name):
    # Remove or replace invalid characters for Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def is_valid_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?youtube\.com/(watch\?v=|shorts/)[\w-]+(&\S*)?$"
    return re.match(pattern, url) is not None

def extract_video_id(url):
    if 'watch?v=' in url:
        return url.split('v=')[1].split('&')[0]
    elif 'shorts/' in url:
        return url.split('shorts/')[1].split('?')[0].split('&')[0]
    return None