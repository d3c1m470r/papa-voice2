import threading
import wx

# NVDA-specific imports
import globalPluginHandler
import ui
import api

class RobustContentReader:
    """
    Robust content reader using only Python standard library.
    """
    
    def get_page_content(self, url):
        """
        Get page content using urllib from standard library.
        """
        try:
            import urllib.request
            import urllib.parse
            import html
            import re
            
            # Set up request with proper headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            req = urllib.request.Request(url, headers=headers)
            
            # Get the webpage
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
                
                # Try to decode
                try:
                    html_content = content.decode('utf-8')
                except UnicodeDecodeError:
                    html_content = content.decode('latin-1', errors='ignore')
            
            # Basic title extraction
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
            title = title_match.group(1) if title_match else "Web Page"
            title = html.unescape(title).strip()
            
            # Remove scripts and styles
            html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            
            # Extract text content - look for common content containers
            content_patterns = [
                r'<article[^>]*>(.*?)</article>',
                r'<main[^>]*>(.*?)</main>',
                r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
                r'<div[^>]*class="[^"]*post[^"]*"[^>]*>(.*?)</div>',
            ]
            
            extracted_content = ""
            for pattern in content_patterns:
                matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
                if matches:
                    extracted_content = matches[0]
                    break
            
            # If no specific content found, extract paragraphs
            if not extracted_content:
                paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL | re.IGNORECASE)
                extracted_content = ' '.join(paragraphs[:5])  # First 5 paragraphs
            
            # Clean up HTML tags and entities
            clean_content = re.sub(r'<[^>]+>', ' ', extracted_content)
            clean_content = html.unescape(clean_content)
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            
            # Check if we have meaningful content
            if len(clean_content) > 50:
                return title, clean_content[:2000]  # Limit to 2000 chars
            else:
                return title, "Could not extract meaningful content from this page."
                
        except Exception as e:
            return "Error", f"Failed to load page: {str(e)}"

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.reader = RobustContentReader()

    def script_readWebContent(self, gesture):
        """Read web page content intelligently."""
        
        def extract_and_speak():
            try:
                # Get current focus object
                focus_obj = api.getFocusObject()
                url = None
                
                # Multiple strategies to get URL
                attempts = [
                    lambda: getattr(focus_obj, 'URL', None),
                    lambda: getattr(focus_obj, 'value', None) if hasattr(focus_obj, 'value') and focus_obj.value and 'http' in focus_obj.value else None,
                    lambda: getattr(focus_obj, 'name', None) if hasattr(focus_obj, 'name') and focus_obj.name and 'http' in focus_obj.name else None,
                ]
                
                # Try to get URL from focus object hierarchy
                obj = focus_obj
                for _ in range(15):  # Search up to 15 levels
                    if obj:
                        for attempt in attempts:
                            try:
                                result = attempt()
                                if result and isinstance(result, str) and 'http' in result:
                                    url = result
                                    break
                            except:
                                continue
                        if url:
                            break
                        obj = getattr(obj, 'parent', None)
                    else:
                        break
                
                if not url:
                    wx.CallAfter(ui.message, "No URL found. Please navigate to a webpage first.")
                    return
                
                # Clean up URL
                if not url.startswith('http'):
                    if '://' in url:
                        url = 'https://' + url.split('://', 1)[1]
                    else:
                        url = 'https://' + url
                
                # Extract content
                title, content = self.reader.get_page_content(url)
                
                # Speak the results
                if content and content != "Could not extract meaningful content from this page.":
                    message = f"{title}. {content}"
                    wx.CallAfter(ui.message, message)
                else:
                    wx.CallAfter(ui.message, f"Page title: {title}. {content}")
                    
            except Exception as e:
                wx.CallAfter(ui.message, f"Error reading content: {str(e)}")
        
        # Run in background
        thread = threading.Thread(target=extract_and_speak, daemon=True)
        thread.start()
        
        ui.message("Reading web content...")
    
    script_readWebContent.__doc__ = "Read the main content of the current web page"
    
    # Use Insert+J gesture
    __gestures = {
        "kb:insert+j": "readWebContent",
    } 