import sys
import os
import threading
import wx

# Add bundled libraries to the path
addon_dir = os.path.dirname(__file__)
lib_dir = os.path.join(addon_dir, "lib")
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

# Now we can import our bundled libraries
import requests
import html2text
from bs4 import BeautifulSoup
import re

# NVDA-specific imports
import globalPluginHandler
import scriptHandler
import ui
import api
from textInfos.offsets import OffsetsTextInfo

class SimpleContentExtractor:
    """
    Pure Python content extractor that works without compiled dependencies.
    """
    def __init__(self):
        self.h = html2text.HTML2Text()
        self.h.ignore_links = True
        self.h.ignore_images = True
        
    def extract_content(self, url):
        """
        Main extraction method that routes to appropriate parser based on URL.
        """
        if self._is_facebook_url(url):
            return self._extract_facebook_content(url)
        else:
            return self._extract_article_content(url)
    
    def _is_facebook_url(self, url):
        """Check if URL is from Facebook."""
        return 'facebook.com' in url.lower() or 'fb.com' in url.lower()
    
    def _extract_facebook_content(self, url):
        """Extract Facebook posts and content."""
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Error", f"Error fetching Facebook page: {e}"

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find Facebook posts using various selectors
        posts = []
        
        # Look for common Facebook post containers
        post_selectors = [
            '[data-testid*="story"]',
            '[role="article"]',
            'div[data-pagelet*="FeedUnit"]',
            'div[data-testid="Keycommand_wrapper_feed_story"]'
        ]
        
        for selector in post_selectors:
            elements = soup.select(selector)
            if elements:
                posts.extend(elements)
                break
        
        if not posts:
            # Fallback: look for any div with substantial text content
            posts = soup.find_all('div', string=re.compile(r'.{50,}'))
        
        # Extract text from posts
        extracted_posts = []
        for post in posts[:5]:  # Limit to first 5 posts
            text = post.get_text(strip=True)
            if len(text) > 30 and not self._is_sponsored_content(text):
                extracted_posts.append(text)
        
        if extracted_posts:
            title = "Facebook Feed - {} posts".format(len(extracted_posts))
            content = "\n\n".join([f"Post {i+1}: {post}" for i, post in enumerate(extracted_posts)])
            return title, content
        else:
            return "Facebook", "No posts found or unable to extract content."
    
    def _extract_article_content(self, url):
        """Extract main content from news articles and blogs."""
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Error", f"Error fetching URL: {e}"

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        # Try to find the main content
        title = self._extract_title(soup)
        content = self._extract_main_content(soup)
        
        if content:
            clean_content = self.h.handle(str(content))
            return title, clean_content
        else:
            return title, "Unable to extract main content from this page."
    
    def _extract_title(self, soup):
        """Extract page title."""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        # Try meta title
        meta_title = soup.find('meta', property='og:title')
        if meta_title:
            return meta_title.get('content', 'Article')
        
        # Try h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        return "Article"
    
    def _extract_main_content(self, soup):
        """Extract main article content using simple heuristics."""
        # Common content selectors
        content_selectors = [
            'article',
            '.article-content',
            '.post-content', 
            '.entry-content',
            '.content',
            'main',
            '[role="main"]'
        ]
        
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content and len(content.get_text(strip=True)) > 200:
                return content
        
        # Fallback: find the largest text block
        text_blocks = soup.find_all(['div', 'section', 'article'])
        largest_block = None
        max_text_length = 0
        
        for block in text_blocks:
            text = block.get_text(strip=True)
            if len(text) > max_text_length:
                max_text_length = len(text)
                largest_block = block
        
        return largest_block if max_text_length > 200 else None
    
    def _is_sponsored_content(self, text):
        """Check if content appears to be sponsored/advertising."""
        sponsored_keywords = [
            'sponsored', 'hirdetés', 'reklám', 'promóció', 
            'advertisement', 'ads by', 'promoted'
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in sponsored_keywords)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.extractor = SimpleContentExtractor()

    def script_readArticle(self, gesture):
        """Extract and read the main content of the current page."""
        def background_extraction():
            try:
                # Get the current URL
                focus_obj = api.getFocusObject()
                url = None
                
                # Try to get URL from browser
                if hasattr(focus_obj, 'windowControlID'):
                    url = focus_obj.windowText if focus_obj.windowText and focus_obj.windowText.startswith('http') else None
                
                if not url:
                    # Try to get from document
                    try:
                        if hasattr(focus_obj, 'makeTextInfo'):
                            info = focus_obj.makeTextInfo("all")
                            url = getattr(info.obj, 'URL', None)
                    except:
                        pass
                
                if not url:
                    wx.CallAfter(ui.message, "No URL found in the current object.")
                    return
                
                # Extract content
                title, content = self.extractor.extract_content(url)
                
                # Speak the result
                if title and content and content != "Unable to extract main content from this page.":
                    message = f"Title: {title}\n\n{content}"
                    wx.CallAfter(ui.message, message)
                else:
                    wx.CallAfter(ui.message, f"Error reading content: {content}")
                    
            except Exception as e:
                wx.CallAfter(ui.message, f"Error: {str(e)}")
        
        # Run extraction in background thread
        thread = threading.Thread(target=background_extraction)
        thread.daemon = True
        thread.start()
        
        ui.message("Reading article content...")
    
    script_readArticle.__doc__ = "Extract and read the main content of the current web page"
    
    # Assign a gesture to the script
    __gestures = {
        "kb:nvda+j": "readArticle",
    } 