import threading
import wx
import re
import os
import sys

# Guarantee that the add-on’s root directory (the parent of this file’s
# ``globalPlugins`` package) is on ``sys.path`` *before* we attempt absolute
# imports. Without this, NVDA may fail to resolve our internal modules.
_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

# NVDA-specific imports
import globalPluginHandler
import ui
import api
import braille

# Project-specific imports
from papaVoiceReader.extract_content import extract_article_content
from papaVoiceReader.facebook_parser import FacebookParser

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.facebook_parser = FacebookParser()

    def is_facebook_url(self, url):
        """Check if a URL is a Facebook URL."""
        return re.match(r'https?://(www\\.)?facebook\\.com', url)

    def script_readWebContent(self, gesture):
        try:
            ui.message("PapaVoice activated")
            browser = api.getForegroundObject()
            url = None
            
            # Try different ways to get the URL
            if hasattr(browser, 'value') and browser.value:
                url = browser.value
            elif hasattr(browser, 'URL') and browser.URL:
                url = browser.URL
            else:
                # Try to find the address bar
                parent = browser
                while parent and not url:
                    if hasattr(parent, 'value') and parent.value and ('http' in parent.value or 'www' in parent.value):
                        url = parent.value
                        break
                    parent = parent.parent
            
            if not url:
                ui.message("Could not get URL from the browser. Make sure you're in a web browser.")
                return
            
            ui.message(f"Processing URL: {url[:50]}...")

            if self.is_facebook_url(url):
                content = self.facebook_parser.parse(url)
                if content:
                    ui.message(content)
                else:
                    ui.message("No main content found on this Facebook page.")
            else:
                article_text = extract_article_content(url)
                if article_text:
                    # NVDA's message function can truncate very long strings.
                    # Break the output into reasonably sized chunks so it doesn't
                    # overwhelm speech/braille.
                    for chunk in _paginate(article_text, 800):
                        ui.message(chunk)
                else:
                    ui.message("No article content could be extracted.")
        except Exception as e:
            ui.message(f"Error: {e}")
    

# Helper -------------------------------------------------------------------

def _paginate(text: str, max_len: int):
    """Yield *text* in pieces no longer than *max_len* characters, trying to split
    on whitespace when possible."""
    start = 0
    while start < len(text):
        end = start + max_len
        if end < len(text):
            # Try not to split in the middle of a word.
            space = text.rfind(" ", start, end)
            if space != -1 and space > start:
                end = space
        yield text[start:end].strip()
        start = end + 1

# ---------------------------------------------------------------------------
# Expose script metadata at module level so NVDA can pick it up.
GlobalPlugin.script_readWebContent.category = "PapaVoice"
GlobalPlugin.script_readWebContent.description = (
    "Reads the main content of the current web page intelligently."
) 

__gestures__ = {
    "kb:nvda+a": "readWebContent",
}

GlobalPlugin.gestures = __gestures__