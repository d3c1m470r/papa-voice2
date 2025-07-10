import sys
import os

# Add addon lib and src to path
addon_folder = os.path.dirname(__file__)
lib_folder = os.path.join(addon_folder, 'lib')
src_folder = os.path.abspath(os.path.join(addon_folder, '..', '..', 'src'))
if lib_folder not in sys.path:
    sys.path.insert(0, lib_folder)
if src_folder not in sys.path:
    sys.path.insert(0, src_folder)

import threading
import wx
import re

# NVDA-specific imports
import globalPluginHandler
import ui
import api

# Project-specific imports
from extract_content import extract_article_content
from facebook_parser import FacebookParser

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.facebook_parser = FacebookParser()

    def is_facebook_url(self, url):
        """Check if a URL is a Facebook URL."""
        return re.match(r'https?://(www\.)?facebook\.com', url)

    def script_readWebContent(self, gesture):
        """Read web page content intelligently."""
        
        def extract_and_speak():
            try:
                # Get current focus object
                focus_obj = api.getFocusObject()
                url = None
                
                # Multiple strategies to get URL
                # Use a simplified approach to get URL
                obj = focus_obj
                for _ in range(5):  # Search up to 5 levels
                    if obj:
                        if hasattr(obj, 'URL'):
                            url = obj.URL
                            if url:
                                break
                        if hasattr(obj, 'value') and isinstance(obj.value, str) and 'http' in obj.value:
                            url = obj.value
                            if url:
                                break
                        obj = obj.parent
                    else:
                        break
                
                if not url:
                    wx.CallAfter(ui.message, "No URL found. Please navigate to a webpage first.")
                    return

                if not url.startswith('http'):
                    url = 'https://' + url

                ui.message("Fetching content...")

                if self.is_facebook_url(url):
                    posts = self.facebook_parser.extract_facebook_posts(url)
                    if posts:
                        full_text = "Facebook content: "
                        for post in posts:
                            full_text += f"{post['title']}. {post['content']}\n\n"
                        wx.CallAfter(ui.message, full_text)
                    else:
                        wx.CallAfter(ui.message, "Could not extract any posts from this Facebook page.")
                else:
                    title, content = extract_article_content(url)
                    if content:
                        message = f"{title}. {content}"
                        wx.CallAfter(ui.message, message)
                    else:
                        wx.CallAfter(ui.message, f"Page title: {title}. Could not extract main content.")
                    
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