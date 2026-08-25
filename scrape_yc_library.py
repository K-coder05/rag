"""
scrape_yc_library.py

Collects articles from the YC Startup Library for the RAG sprint corpus.

Two things make this harder than the PG essay scrape, and this script exists
specifically to handle them:

1. /library pages are client-rendered (Next.js). A plain `requests.get()` on
   an individual article only returns metadata (title, OG tags) -- the body
   text isn't in the initial HTML. This script uses Playwright to actually
   render each page in a headless browser before extracting text.

2. robots.txt disallows crawling the *filtered/paginated listing* views
   (`/library?...`), with a carve-out for `/library?categories=*&*`. It does
   NOT disallow individual article pages (`/library/<id>-<slug>`, no query
   string) or the sitemap. So instead of paginating the listing UI at all,
   this script reads the full article list from the public sitemap:
   https://www.ycombinator.com/library/sitemap.xml -- one request instead of
   dozens of paginated/filtered ones.

Some library entries are video/podcast episodes with little to no on-page
transcript. This script renders each page, checks the extracted word count,
and skips (and logs) anything too thin to be useful as a RAG document.

Usage:
    pip install requests playwright beautifulsoup4 markdownify
    playwright install chromium
    python scrape_yc_library.py
"""
import re
import csv
import time
import pathlib
import requests
from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify as html_to_markdown
from playwright.sync_api import sync_playwright

SITEMAP_URL = "https://www.ycombinator.com/library/sitemap.xml"
OUT_DIR = pathlib.Path("corpus/yc_library")
OUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_DOCS = 200    # cap the pull -- the sitemap has 800+ entries, you don't need them all
MIN_WORDS = 200   # below this, it's probably a video/podcast page with no real transcript

HEADERS = {"User-Agent": "rag-sprint-corpus-collector/1.0 (student project)"}
ARTICLE_RE = re.compile(r"^https://www\.ycombinator\.com/library/[A-Za-z0-9]{2}-[a-z0-9-]+$")


def get_article_urls():
    resp = requests.get(SITEMAP_URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    urls = re.findall(r"<loc>(.*?)</loc>", resp.text)
    articles = [u for u in urls if ARTICLE_RE.match(u)]
    return articles[:MAX_DOCS]


def _merge_adjacent(container, tag_name):
    # The site's markup wraps each word of some spans in its own <em>/<strong>,
    # which markdownify would otherwise render as *word* *word* *word*.
    changed = True
    while changed:
        changed = False
        for tag in container.find_all(tag_name):
            nxt = tag.next_sibling
            if isinstance(nxt, NavigableString) and nxt.strip() == "" and nxt.string:
                nxt2 = nxt.next_sibling
                if nxt2 is not None and getattr(nxt2, "name", None) == tag_name:
                    tag.append(str(nxt))
                    for child in list(nxt2.contents):
                        tag.append(child)
                    nxt.extract()
                    nxt2.decompose()
                    changed = True
                    break


def extract_article(html):
    soup = BeautifulSoup(html, "html.parser")
    # The article body renders into one or more Tailwind Typography ".prose"
    # containers (the rest of the page is nav/TOC/related-articles/footer
    # chrome); the real body is always by far the longest.
    candidates = soup.select(".prose")
    if not candidates:
        raise ValueError("no .prose container found on page")
    body = max(candidates, key=lambda el: len(el.get_text()))

    _merge_adjacent(body, "em")
    _merge_adjacent(body, "strong")
    for heading in body.find_all(re.compile(r"^h[1-6]$")):
        for bold in heading.find_all(["strong", "b"]):
            bold.unwrap()

    md = html_to_markdown(str(body), heading_style="ATX")
    lines = [line.rstrip() for line in md.split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def main():
    # Full refresh each run -- otherwise a doc that gets skipped this time
    # (e.g. now correctly identified as thin video/podcast content) leaves
    # its stale .md from a previous run sitting in the corpus untouched.
    for stale in OUT_DIR.glob("*.md"):
        stale.unlink()

    urls = get_article_urls()
    print(f"Found {len(urls)} candidate article URLs (capped at {MAX_DOCS})")

    manifest, skipped = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent=HEADERS["User-Agent"])

        for i, url in enumerate(urls, 1):
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                title = page.title().split(" : YC Startup Library")[0].strip()
                text = extract_article(page.content())
                word_count = len(text.split())

                if word_count < MIN_WORDS:
                    skipped.append({"url": url, "reason": f"only {word_count} words (likely video/podcast, no transcript)"})
                    print(f"[{i}/{len(urls)}] skip (thin content, {word_count}w): {title}")
                    continue

                slug = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-").lower()[:60] or f"doc-{i}"
                fname = OUT_DIR / f"{slug}.md"
                fname.write_text(f"---\ntitle: {title}\nsource: {url}\n---\n\n{text}", encoding="utf-8")

                manifest.append({"title": title, "url": url, "file": str(fname), "words": word_count})
                print(f"[{i}/{len(urls)}] saved: {title} ({word_count}w)")
            except Exception as e:
                skipped.append({"url": url, "reason": str(e)})
                print(f"  FAILED {url}: {e}")
            time.sleep(1.0)  # polite delay -- this is a full rendered page load, not a cheap GET

        browser.close()

    with open(OUT_DIR / "_manifest.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url", "file", "words"])
        writer.writeheader()
        writer.writerows(manifest)
    with open(OUT_DIR / "_skipped.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "reason"])
        writer.writeheader()
        writer.writerows(skipped)

    print(f"\nDone. {len(manifest)} saved, {len(skipped)} skipped.")
    print(f"See {OUT_DIR}/_manifest.csv and {OUT_DIR}/_skipped.csv")


if __name__ == "__main__":
    main()