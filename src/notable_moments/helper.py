from urllib.parse import urlparse
import re


def get_video_id(url: str) -> str | None:
    parse_url = urlparse(url)
    m = None
    if "watch" in parse_url.path:
        q = parse_url.query
        if "&" in q:
            m = re.search(r"v=([\w-]+)&", q, re.IGNORECASE)
        else:
            m = re.search(r"v=([\w-]+)", q, re.IGNORECASE)
    if "live" in parse_url.path:
        p = parse_url.path
        m = re.search(r"live\/([\w-]+)", p, re.IGNORECASE)
    return m if not m else m.group(1)
