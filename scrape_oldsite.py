#!/usr/bin/env python3
"""Scrape captainsflathotel.com.au into pub/oldsite.

Saves:
  pub/oldsite/<slug>.html   - raw HTML of each page
  pub/oldsite/media/<file>  - all media assets (full-size originals)
  pub/oldsite/content/<slug>.txt - extracted text content per page
"""
import html.parser
import json
import os
import re
import sys
import urllib.request
import urllib.error

BASE = "https://www.captainsflathotel.com.au"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pub", "oldsite")
MEDIA_DIR = os.path.join(OUT, "media")
CONTENT_DIR = os.path.join(OUT, "content")

PAGES = {
    "index": "/",
    "our-bar": "/our-bar",
    "events": "/events",
    "about-1-1": "/about-1-1",   # 1938 (history)
    "about-1": "/about-1",       # Accommodation
    "about-9": "/about-9",       # Contact us
    "team-4": "/team-4",         # Menu
    "general-4": "/general-4",   # Opening hours
    "general-6": "/general-6",   # Gallery
    "merchandise": "/merchandise",
}

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/126.0 Safari/537.36"}

# media id (with extension) right after /media/
MEDIA_RE = re.compile(
    r"(?:static\.wixstatic\.com|video\.wixstatic\.com)[\\/]+media[\\/]+"
    r"([A-Za-z0-9_\-~]+?\.(?:jpg|jpeg|png|gif|webp|jfif|svg|mp4|webm|mov))",
    re.IGNORECASE)
# uglified/escaped urls e.g. https:\/\/static.wixstatic.com\/media\/xxx
HOST_RE = re.compile(
    r"https?:[\\/]+((?:static|video)\.wixstatic\.com[\\/]+media[\\/]+"
    r"[A-Za-z0-9_\-~]+?\.(?:jpg|jpeg|png|gif|webp|jfif|svg|mp4|webm|mov))",
    re.IGNORECASE)


def fetch(url, dest=None):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if dest:
        with open(dest, "wb") as f:
            f.write(data)
    return data


class TextExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.parts.append("\n## ")
        elif tag in ("p", "div", "li", "br", "section", "tr"):
            self.parts.append("\n")
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v and v.startswith(("http", "mailto", "tel")):
                    self.parts.append(f" ")
        if tag == "img":
            for k, v in attrs:
                if k == "alt" and v:
                    self.parts.append(f"[img: {v}]")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

    def text(self):
        t = "".join(self.parts)
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r"\n\s*\n+", "\n\n", t)
        return t.strip()


def main():
    os.makedirs(MEDIA_DIR, exist_ok=True)
    os.makedirs(CONTENT_DIR, exist_ok=True)

    media_ids = {}   # filename -> host/path base
    for slug, path in PAGES.items():
        url = BASE + path
        dest = os.path.join(OUT, f"{slug}.html")
        print(f"page: {url}")
        try:
            fetch(url, dest)
        except Exception as e:
            print(f"  FAILED: {e}")
            continue
        with open(dest, encoding="utf-8", errors="replace") as f:
            doc = f.read()
        for m in MEDIA_RE.finditer(doc):
            media_ids.setdefault(m.group(1), "static.wixstatic.com")
        for m in HOST_RE.finditer(doc):
            frag = m.group(1).replace("\\/", "/")
            host, _, fname = frag.partition("/media/")
            media_ids.setdefault(fname, host)

        # extracted text
        p = TextExtractor()
        p.feed(doc)
        with open(os.path.join(CONTENT_DIR, f"{slug}.txt"), "w",
                  encoding="utf-8") as f:
            f.write(f"# {BASE}{path}\n\n{p.text()}\n")

    print(f"\n{len(media_ids)} unique media files found")
    ok, fail = 0, 0
    for fname, host in sorted(media_ids.items()):
        safe = fname.replace("/", "_")
        dest = os.path.join(MEDIA_DIR, safe)
        if os.path.exists(dest):
            ok += 1
            continue
        url = f"https://{host}/media/{fname}"
        try:
            fetch(url, dest)
            ok += 1
            print(f"  got {safe} ({os.path.getsize(dest)} bytes)")
        except Exception as e:
            fail += 1
            print(f"  FAIL {url}: {e}")
    print(f"\ndone: {ok} media files, {fail} failed")


if __name__ == "__main__":
    main()
