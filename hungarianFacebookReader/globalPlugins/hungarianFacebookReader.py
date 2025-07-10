import sys
import os
import threading
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse
import json

# NVDA-specific imports
import globalPluginHandler
import ui
import api
from logHandler import log
import speech
import wx

# Windows-compatible HTML to text conversion
import html

class FacebookParser:
    """Windows-compatible Facebook content parser."""
    
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
    def extract_facebook_posts(self, url):
        """Extract Facebook posts from a page URL."""
        try:
            # Create request with proper headers
            request = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
            
            with urllib.request.urlopen(request, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
                
            # Simple content extraction for Facebook posts
            posts = []
            
            # Look for common Facebook post patterns
            # This is a simplified approach - Facebook's structure changes frequently
            post_patterns = [
                r'<div[^>]*data-testid="post_message"[^>]*>(.*?)</div>',
                r'<div[^>]*userContent[^>]*>(.*?)</div>',
                r'<p[^>]*>(.*?)</p>'
            ]
            
            for pattern in post_patterns:
                matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
                for match in matches:
                    # Clean HTML tags
                    clean_text = self.clean_html(match)
                    if clean_text and len(clean_text) > 10:  # Filter out very short content
                        posts.append({
                            'title': 'Facebook Post',
                            'content': clean_text[:500]  # Limit length
                        })
                        
            return posts[:5]  # Return max 5 posts
            
        except Exception as e:
            log.error(f"Error extracting Facebook posts: {e}")
            return []
    
    def clean_html(self, html_content):
        """Clean HTML tags and decode entities."""
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', html_content)
        # Decode HTML entities
        clean_text = html.unescape(clean_text)
        # Clean up whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text

class ContentExtractor:
    """Windows-compatible content extractor."""
    
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    def extract_article_content(self, url):
        """Extract article content from URL."""
        try:
            request = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
            
            with urllib.request.urlopen(request, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
            
            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else "No title"
            title = html.unescape(title).strip()
            
            # Simple content extraction - look for main content areas
            content_patterns = [
                r'<article[^>]*>(.*?)</article>',
                r'<main[^>]*>(.*?)</main>',
                r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
                r'<div[^>]*id="[^"]*content[^"]*"[^>]*>(.*?)</div>'
            ]
            
            extracted_content = ""
            for pattern in content_patterns:
                matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
                if matches:
                    extracted_content = matches[0]
                    break
            
            if not extracted_content:
                # Fallback: extract all paragraph text
                paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
                extracted_content = ' '.join(paragraphs)
            
            # Clean HTML
            clean_content = self.clean_html(extracted_content)
            
            return title, clean_content[:1000]  # Limit to 1000 chars
            
        except Exception as e:
            log.error(f"Error extracting content: {e}")
            return "Error", f"Could not extract content: {str(e)}"
    
    def clean_html(self, html_content):
        """Clean HTML tags and decode entities."""
        # Remove script and style tags
        html_content = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html_content, flags=re.DOTALL)
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', html_content)
        # Decode HTML entities
        clean_text = html.unescape(clean_text)
        # Clean up whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """Hungarian Facebook Reader Global Plugin."""
    
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.facebook_parser = FacebookParser()
        self.content_extractor = ContentExtractor()
        log.info("Hungarian Facebook Reader initialized")
    
    def is_facebook_url(self, url):
        """Check if URL is Facebook."""
        return 'facebook.com' in url.lower()
    
    def get_current_url(self):
        """Get current browser URL using multiple strategies."""
        try:
            focus_obj = api.getFocusObject()
            
            # Strategy 1: Look for URL in current object
            obj = focus_obj
            for _ in range(10):  # Search up hierarchy
                if obj:
                    # Check common URL attributes
                    for attr in ['URL', 'url', 'value', 'name']:
                        if hasattr(obj, attr):
                            url = getattr(obj, attr)
                            if url and isinstance(url, str) and 'http' in url:
                                return url
                    obj = obj.parent
                else:
                    break
            
            # Strategy 2: Get from browse mode document
            if hasattr(focus_obj, 'treeInterceptor') and focus_obj.treeInterceptor:
                ti = focus_obj.treeInterceptor
                if hasattr(ti, 'rootNVDAObject') and hasattr(ti.rootNVDAObject, 'URL'):
                    return ti.rootNVDAObject.URL
            
            return None
            
        except Exception as e:
            log.error(f"Error getting URL: {e}")
            return None
    
    def script_readFacebookContent(self, gesture):
        """Read Facebook content intelligently. Bound to NVDA+Shift+F."""
        
        def extract_and_speak():
            try:
                url = self.get_current_url()
                
                if not url:
                    wx.CallAfter(ui.message, "Nincs URL találva. Kérlek navigálj egy weboldalra először.")
                    return
                
                if not url.startswith('http'):
                    url = 'https://' + url
                
                wx.CallAfter(ui.message, "Tartalom betöltése...")
                
                if self.is_facebook_url(url):
                    posts = self.facebook_parser.extract_facebook_posts(url)
                    if posts:
                        full_text = "Facebook tartalom: "
                        for i, post in enumerate(posts, 1):
                            full_text += f"{i}. bejegyzés: {post['content']} ... "
                        wx.CallAfter(speech.speakMessage, full_text)
                    else:
                        wx.CallAfter(ui.message, "Nem sikerült kinyerni a bejegyzéseket erről a Facebook oldalról.")
                else:
                    title, content = self.content_extractor.extract_article_content(url)
                    if content and len(content) > 20:
                        message = f"Cím: {title}. Tartalom: {content}"
                        wx.CallAfter(speech.speakMessage, message)
                    else:
                        wx.CallAfter(ui.message, f"Oldal címe: {title}. Nem sikerült kinyerni a fő tartalmat.")
                    
            except Exception as e:
                log.error(f"Error in readFacebookContent: {e}")
                wx.CallAfter(ui.message, f"Hiba a tartalom olvasásakor: {str(e)}")
        
        # Run in background thread
        thread = threading.Thread(target=extract_and_speak, daemon=True)
        thread.start()
    
    def script_readCurrentElement(self, gesture):
        """Read current element content. Bound to NVDA+Shift+R."""
        
        try:
            focus_obj = api.getFocusObject()
            
            if not focus_obj:
                ui.message("Nincs aktív elem.")
                return
            
            # Get element text
            text = ""
            if hasattr(focus_obj, 'name') and focus_obj.name:
                text += focus_obj.name + ". "
            if hasattr(focus_obj, 'value') and focus_obj.value:
                text += focus_obj.value + ". "
            if hasattr(focus_obj, 'description') and focus_obj.description:
                text += focus_obj.description + ". "
            
            if text:
                speech.speakMessage(text)
            else:
                ui.message("Nincs szöveg ebben az elemben.")
                
        except Exception as e:
            log.error(f"Error in readCurrentElement: {e}")
            ui.message(f"Hiba: {str(e)}")
    
    def script_toggleHungarianMode(self, gesture):
        """Toggle Hungarian language optimizations. Bound to NVDA+Shift+H."""
        
        # This is a placeholder for Hungarian-specific optimizations
        ui.message("Magyar nyelvi optimalizációk kapcsolása - még nem implementált.")
    
    # Gesture bindings
    __gestures = {
        "kb:NVDA+shift+f": "readFacebookContent",
        "kb:NVDA+shift+r": "readCurrentElement", 
        "kb:NVDA+shift+h": "toggleHungarianMode",
    }