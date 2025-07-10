import threading
import wx
import re

# NVDA-specific imports
import globalPluginHandler
import ui
import api
import braille

# Project-specific imports
from .extract_content import extract_article_content
from .facebook_parser import FacebookParser

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.facebook_parser = FacebookParser()

    def is_facebook_url(self, url):
        """Check if a URL is a Facebook URL."""
        return re.match(r'https?://(www\\.)?facebook\\.com', url)

    def script_readWebContent(self, gesture):
        try:
            browser = api.getForegroundObject()
            if browser.role == api.controlTypes.ROLE_PANE:
                browser = browser.parent
            url = browser.value
            if not url:
                ui.message("Could not get URL from the browser.")
                return

            if self.is_facebook_url(url):
                content = self.facebook_parser.parse(url)
                if content:
                    ui.message(content)
                else:
                    ui.message("No main content found on this Facebook page.")
            else:
                article_content = extract_article_content(url)
                if article_content:
                    ui.message(article_content)
                else:
                    ui.message("No article content could be extracted.")
        except Exception as e:
            ui.message(f"Error: {e}")
    
    script_readWebContent.category = "PapaVoice"
    script_readWebContent.description = "Reads the main content of the current web page intelligently."
    script_readWebContent.gesture = "kb:nvda+alt+i" 