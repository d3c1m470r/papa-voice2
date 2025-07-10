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

# NVDA-specific imports
import globalPluginHandler
import scriptHandler
import ui
import api
from textInfos.offsets import OffsetsTextInfo

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    # --- The content extraction logic from our script ---
    def extract_article_content(self, url):
        """
        Fetches a URL, extracts the main article content, and returns it as plain text.
        """
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"Error fetching URL: {e}", ""

        doc = Document(response.text)
        title = doc.title()
        content_html = doc.summary()

        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        content_text = h.handle(content_html)
        
        return title, content_text

    # --- The function that runs in a background thread ---
    def threaded_extract(self, url):
        try:
            title, content = self.extract_article_content(url)
            if title and content:
                # Use wx.CallAfter to safely update the UI from the thread
                wx.CallAfter(ui.browseableMessage, f"<h1>{title}</h1><br/>{content}", "Article Content")
            elif title:
                wx.CallAfter(ui.message, title)
            else:
                wx.CallAfter(ui.message, "Could not extract content.")
        except Exception as e:
            wx.CallAfter(ui.message, f"An error occurred: {e}")

    # --- The script that is triggered by the user's key press ---
    def script_readArticle(self, gesture):
        """
        Gets the URL from the focused object and starts the extraction process.
        Bound to NVDA+Shift+U by default.
        """
        # Get the currently focused object
        obj = api.getFocusObject()
        # A simple way to get a URL is to check the object's value.
        # This works well for the address bar in most browsers.
        url = obj.value

        # A more robust way for links is to find a text info object
        if not url:
            try:
                text_info = obj.makeTextInfo(api.textInfos.POSITION_CARET)
                if isinstance(text_info, OffsetsTextInfo):
                    url = text_info.URL
            except (RuntimeError, NotImplementedError):
                pass
        
        if url and url.startswith(('http://', 'https://')):
            ui.message("Fetching article...")
            # Run the extraction in a separate thread to not freeze NVDA
            thread = threading.Thread(target=self.threaded_extract, args=(url,))
            thread.daemon = True
            thread.start()
        else:
            ui.message("No URL found in the current object.")

    # Assign a gesture to the script
    __gestures = {
        "kb:nvda+j": "readArticle",
    } 