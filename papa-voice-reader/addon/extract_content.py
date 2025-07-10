import requests
from readability import Document
import sys
import html2text

def extract_article_content(url):
    """
    Fetches a URL, extracts the main article content, and returns it as plain text.
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}", ""

    doc = Document(response.text)
    
    title = doc.title()
    content_html = doc.summary()

    # Convert HTML to plain text
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    content_text = h.handle(content_html)
    
    return title, content_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_content.py <URL>")
        sys.exit(1)

    article_url = sys.argv[1]
    title, content = extract_article_content(article_url)

    print(f"--- Title ---\n{title}\n")
    print(f"--- Content ---\n{content}") 