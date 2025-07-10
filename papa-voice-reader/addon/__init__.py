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
from readability import Document
import html2text
from bs4 import BeautifulSoup
import re

# NVDA-specific imports
import globalPluginHandler
import scriptHandler
import ui
import api
from textInfos.offsets import OffsetsTextInfo

class SmartContentExtractor:
    """
    Intelligent content extractor that can handle Facebook and general articles.
    """
    def __init__(self):
        self.h = html2text.HTML2Text()
        self.h.ignore_links = True
        self.h.ignore_images = True
    
    def extract_content(self, url):
        """
        Main extraction method that routes to appropriate parser based on URL.
        """
        try:
            if self._is_facebook_url(url):
                return self._extract_facebook_content(url)
            else:
                return self._extract_article_content(url)
        except Exception as e:
            return "Content Extraction Error", f"Unable to extract content: {str(e)}"
    
    def _is_facebook_url(self, url):
        """Check if URL is from Facebook."""
        return 'facebook.com' in url.lower() or 'fb.com' in url.lower()
    
    def _extract_facebook_content(self, url):
        """Extract content from Facebook URLs."""
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Facebook Loading Error", f"Could not load Facebook page: {str(e)}"

        soup = BeautifulSoup(response.text, 'html.parser')
        posts = self._extract_facebook_posts(soup)
        
        if not posts:
            # Fallback to general content if no posts found
            page_text = soup.get_text()[:1000]
            clean_text = self.h.handle(page_text)
            return "Facebook Page", clean_text
        
        if len(posts) == 1:
            return posts[0]['title'], posts[0]['content']
        else:
            # Multiple posts
            title = f"Facebook Feed - {len(posts)} posts"
            content_parts = []
            for i, post in enumerate(posts, 1):
                content_parts.append(f"Post {i}: {post['title']}\n{post['content']}")
            return title, '\n\n'.join(content_parts)
    
    def _extract_facebook_posts(self, soup):
        """Extract individual posts from Facebook page."""
        posts = []
        
        # Facebook post selectors based on research
        post_selectors = [
            '[data-testid="Keycommand_wrapper_feed_story"]',
            '[data-pagelet*="FeedUnit"]',
            '[role="article"]',
            '[data-testid*="story"]',
        ]
        
        found_posts = []
        for selector in post_selectors:
            found_posts.extend(soup.select(selector))
        
        # Process found posts
        for i, post_element in enumerate(found_posts[:5]):  # Limit to 5 posts
            try:
                if self._is_sponsored_content(post_element):
                    continue  # Skip ads
                
                title = self._extract_post_title(post_element, i)
                content = self._extract_post_content(post_element)
                
                if content and len(content.strip()) > 20:
                    posts.append({
                        "title": title,
                        "content": content[:1000]  # Limit content length
                    })
            except Exception:
                continue  # Skip problematic posts
        
        return posts
    
    def _is_sponsored_content(self, post_element):
        """Detect sponsored/ad content."""
        post_text = post_element.get_text().lower()
        
        # Hungarian and English sponsored indicators
        sponsored_keywords = ['sponsored', 'hirdetés', 'reklám', 'promoted', 'promóció']
        
        for keyword in sponsored_keywords:
            if keyword in post_text:
                return True
        
        # Check for aria-labelledby patterns that indicate ads
        sponsored_spans = post_element.find_all('span', attrs={'aria-labelledby': True})
        for span in sponsored_spans:
            labelledby_id = span.get('aria-labelledby')
            if labelledby_id:
                label_element = post_element.find(id=labelledby_id)
                if label_element and any(keyword in label_element.get_text().lower() 
                                       for keyword in sponsored_keywords):
                    return True
        
        return False
    
    def _extract_post_title(self, post_element, post_index):
        """Extract post title/author."""
        title_selectors = ['h2 a', 'h3 a', 'strong', '[role="link"]']
        
        for selector in title_selectors:
            title_element = post_element.select_one(selector)
            if title_element:
                title_text = title_element.get_text(strip=True)
                if title_text and len(title_text) < 100:
                    return f"Post by {title_text}"
        
        return f"Facebook Post {post_index + 1}"
    
    def _extract_post_content(self, post_element):
        """Extract main post content."""
        # Remove scripts and styles
        for element in post_element(["script", "style"]):
            element.decompose()
        
        # Try specific content selectors
        text_selectors = ['[data-testid*="text"]', 'p', '[role="text"]']
        content_parts = []
        
        for selector in text_selectors:
            for element in post_element.select(selector):
                text = element.get_text(strip=True)
                if text and len(text) > 10:
                    content_parts.append(text)
        
        if content_parts:
            content = ' '.join(content_parts)
            return re.sub(r'\s+', ' ', content)
        
        # Fallback: all text from post
        all_text = post_element.get_text(separator=' ', strip=True)
        return re.sub(r'\s+', ' ', all_text)[:1000] if all_text else ""
    
    def _extract_article_content(self, url):
        """Extract content from regular news articles."""
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Article Loading Error", f"Could not load article: {str(e)}"

        doc = Document(response.text)
        title = doc.title()
        content_html = doc.summary()
        content_text = self.h.handle(content_html)
        
        return title, content_text

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.extractor = SmartContentExtractor()
    
    def extract_url_from_focus(self):
        """Extract URL from currently focused element."""
        try:
            focus = api.getFocusObject()
            
            # Try to get URL from address bar (browser)
            if hasattr(focus, 'value') and focus.value:
                if 'http' in focus.value:
                    return focus.value
            
            # Try to get URL from link
            if hasattr(focus, 'role') and 'link' in str(focus.role).lower():
                try:
                    states = focus.states
                    for attr in dir(focus):
                        if 'url' in attr.lower() or 'href' in attr.lower():
                            url = getattr(focus, attr, None)
                            if url and isinstance(url, str) and 'http' in url:
                                return url
                except:
                    pass
            
            # Try to get current URL from browser
            browser_objects = []
            obj = focus
            while obj:
                browser_objects.append(obj)
                obj = obj.parent
            
            for obj in browser_objects:
                try:
                    if hasattr(obj, 'value') and obj.value and 'http' in obj.value:
                        return obj.value
                    if hasattr(obj, 'name') and obj.name and 'http' in obj.name:
                        return obj.name
                except:
                    continue
                    
            return None
            
        except Exception as e:
            return None
    
    def read_content_in_background(self, url):
        """Extract and read content in a background thread."""
        try:
            title, content = self.extractor.extract_content(url)
            
            # Schedule speaking on the main thread
            wx.CallAfter(self.speak_content, title, content)
            
        except Exception as e:
            wx.CallAfter(ui.message, f"Error reading content: {str(e)}")
    
    def speak_content(self, title, content):
        """Speak the extracted content using NVDA."""
        # Announce what we're about to read
        ui.message("Reading main content...")
        
        # Brief pause
        wx.CallLater(500, self.speak_title_and_content, title, content)
    
    def speak_title_and_content(self, title, content):
        """Speak title and content with proper pauses."""
        # Speak title first
        ui.message(f"Title: {title}")
        
        # Wait a bit, then speak content
        wx.CallLater(2000, ui.message, content)
    
    @scriptHandler.script(description="Read the main content of the current web page", 
                         gesture="kb:NVDA+j")
    def script_readArticle(self, gesture):
        """Main script function triggered by keyboard shortcut."""
        url = self.extract_url_from_focus()
        
        if url:
            ui.message("Extracting content...")
            # Start background thread for content extraction
            thread = threading.Thread(target=self.read_content_in_background, args=(url,))
            thread.daemon = True
            thread.start()
        else:
            ui.message("No URL found in the current object.")

    # Assign a gesture to the script
    __gestures = {
        "kb:nvda+j": "readArticle",
    } 