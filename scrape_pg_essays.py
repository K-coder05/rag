"""
scrape_pg_essays.py

Collects Paul Graham's essays for the RAG sprint corpus.

Why this approach: paulgraham.com/articles.html is a plain static HTML index
(a <table> of <a> links to plain HTML essay pages) -- no JavaScript rendering
needed, and robots.txt does not block these paths. This is the cheapest part
of the corpus to collect.

Usage:
    pip install requests beautifulsoup4 markdownify
    python scrape_pg_essays.py
"""
import re
import time
import json
import pathlib
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown

BASE = "https://paulgraham.com/"
INDEX_URL = BASE + "articles.html"
OUT_DIR = pathlib.Path("corpus/pg_essays")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Identify yourself honestly -- good practice even where robots.txt allows crawling.
HEADERS = {"User-Agent": "rag-sprint-corpus-collector/1.0 (student project)"}


def get_essay_links():
    resp = requests.get(INDEX_URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    links = []
    for a in soup.select("table a[href]"):
        href = a["href"]
        if href.endswith(".html") and not href.startswith("http"):
            title = a.get_text(strip=True)
            if title:
                links.append((title, BASE + href))

    # de-dupe while preserving order (the index has a couple of repeated links)
    seen, unique = set(), []
    for title, url in links:
        if url not in seen:
            seen.add(url)
            unique.append((title, url))
    return unique


def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "head"]):
        tag.decompose()

    # PG's pages put the essay body in a <font face="verdana"> block alongside
    # several small ones (footnote markers, nav fragments). The body is always
    # by far the longest, so picking the longest reliably isolates it.
    candidates = [f for f in soup.find_all("font") if (f.get("face") or "").lower() == "verdana"]
    body = max(candidates, key=lambda f: len(f.get_text()), default=soup)

    # Strip the recurring "Want to start a startup? Get funded by Y Combinator"
    # promo banner (a nested <table>) -- identical boilerplate on ~50 essays,
    # pure noise for retrieval/embeddings.
    for table in body.find_all("table"):
        if "Want to start a startup" in table.get_text():
            table.decompose()

    md = html_to_markdown(str(body), heading_style="ATX")
    # Drop the trailing double-space <br> markers markdownify adds -- with
    # blank lines already separating paragraphs, they're just visual noise.
    lines = [line.rstrip() for line in md.split("\n")]
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    return text


def main():
    links = get_essay_links()
    print(f"Found {len(links)} essay links")

    manifest = []
    for i, (title, url) in enumerate(links, 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.raise_for_status()
            text = clean_text(resp.text)

            slug = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-").lower()[:60] or f"essay-{i}"
            fname = OUT_DIR / f"{slug}.md"
            fname.write_text(f"---\ntitle: {title}\nsource: {url}\n---\n\n{text}", encoding="utf-8")

            manifest.append({"title": title, "url": url, "file": str(fname)})
            print(f"[{i}/{len(links)}] saved: {title}")
        except Exception as e:
            print(f"  FAILED {url}: {e}")
        time.sleep(0.5)  # polite delay -- robots.txt sets no crawl-delay, but don't hammer it

    (OUT_DIR / "_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"\nDone. {len(manifest)} essays saved to {OUT_DIR}/")
    print("Spot-check a few files -- PG's markup is old-school HTML, so the odd")
    print("nav fragment or stray line can slip through get_text(). Trim as needed.")


if __name__ == "__main__":
    main()