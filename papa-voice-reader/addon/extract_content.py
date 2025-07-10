import requests
import sys
import html2text
from bs4 import BeautifulSoup

def extract_article_content(url: str) -> str:
    """Return a best-effort plain-text summary of the main content at *url*.

    This implementation intentionally avoids compiled binary dependencies such as
    *lxml* in order to remain compatible with NVDA's 32-bit Python runtime. It
    relies on *BeautifulSoup* to locate a reasonable content section (``<article>
    `` or ``<main>``) and *html2text* to convert the resulting HTML markup to
    speech-friendly plain text.
    """

    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        return f"Error fetching URL: {exc}"

    soup = BeautifulSoup(resp.text, "html.parser")

    # Try to locate the most relevant section.
    main = soup.find("article") or soup.find("main") or soup.body or soup

    # Fallback if main is None for some malformed pages.
    content_html = str(main) if main else resp.text

    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True

    plain_text = h.handle(content_html)

    title_tag = soup.title.string.strip() if soup.title and soup.title.string else ""

    # Combine title and extracted plain text into a single message so callers
    # receive a simple string rather than a tuple.
    if title_tag:
        return f"{title_tag}\n\n{plain_text}"
    return plain_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_content.py <URL>")
        sys.exit(1)

    url_arg = sys.argv[1]
    print(extract_article_content(url_arg)) 