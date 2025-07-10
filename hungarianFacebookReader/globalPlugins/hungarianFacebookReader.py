# -*- coding: utf-8 -*-
# Hungarian Facebook Reader for NVDA
# Uses ONLY built-in Python modules and NVDA APIs for maximum Windows compatibility

import sys
import os
import threading
import re
import html
import time
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from urllib.error import URLError, HTTPError

# NVDA-specific imports (all built-in)
import globalPluginHandler
import ui
import api
import speech
import browseMode
import controlTypes
from logHandler import log
import wx

class WindowsCompatibleContentExtractor:
    """Windows-compatible content extractor using only Python standard library."""
    
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        self.timeout = 10
    
    def extract_content(self, url):
        """Extract content from URL using only standard library."""
        try:
            # Create request with proper headers
            headers = {
                'User-Agent': self.user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'hu-HU,hu;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'identity',  # No compression for simplicity
                'Connection': 'close'
            }
            
            request = Request(url, headers=headers)
            
            with urlopen(request, timeout=self.timeout) as response:
                content = response.read().decode('utf-8', errors='ignore')
            
            return self._parse_content(content, url)
            
        except (URLError, HTTPError, Exception) as e:
            log.error(f"Error extracting content from {url}: {e}")
            return None, f"Hiba a tartalom betöltésekor: {str(e)}"
    
    def _parse_content(self, html_content, url):
        """Parse HTML content and extract meaningful text."""
        
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        title = "Cím nélkül"
        if title_match:
            title = self._clean_text(title_match.group(1))
        
        # Facebook-specific parsing
        if 'facebook.com' in url.lower():
            return self._parse_facebook_content(html_content, title)
        
        # General content parsing
        return self._parse_general_content(html_content, title)
    
    def _parse_facebook_content(self, html_content, title):
        """Parse Facebook-specific content patterns."""
        
        posts = []
        
        # Facebook post patterns (simplified for compatibility)
        patterns = [
            # Look for post content in common Facebook structures
            r'<div[^>]*data-testid="post_message"[^>]*>(.*?)</div>',
            r'<div[^>]*userContent[^>]*>(.*?)</div>',
            # Look for text content in posts
            r'<p[^>]*dir="auto"[^>]*>(.*?)</p>',
            # Status updates
            r'<span[^>]*dir="auto"[^>]*>(.*?)</span>'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                clean_text = self._clean_text(match)
                # Filter out short or irrelevant content
                if clean_text and len(clean_text) > 15 and self._is_meaningful_content(clean_text):
                    posts.append(clean_text)
        
        if posts:
            # Limit to first 3 posts and concatenate
            content = "Facebook bejegyzések: " + " ... ".join(posts[:3])
            return title, content[:800]  # Limit length
        else:
            return title, "Nem találhatók bejegyzések ezen a Facebook oldalon."
    
    def _parse_general_content(self, html_content, title):
        """Parse general web content."""
        
        # Try to find main content areas
        content_patterns = [
            r'<article[^>]*>(.*?)</article>',
            r'<main[^>]*>(.*?)</main>',
            r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*id="[^"]*content[^"]*"[^>]*>(.*?)</div>',
        ]
        
        content = ""
        for pattern in content_patterns:
            matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if matches:
                content = matches[0]
                break
        
        # Fallback: extract paragraphs
        if not content:
            paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL)
            content = ' '.join(paragraphs[:5])  # First 5 paragraphs
        
        clean_content = self._clean_text(content)
        return title, clean_content[:1000] if clean_content else "Nem található tartalom."
    
    def _clean_text(self, text):
        """Clean HTML tags and normalize text."""
        if not text:
            return ""
        
        # Remove script and style content
        text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Decode HTML entities
        text = html.unescape(text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def _is_meaningful_content(self, text):
        """Check if text content is meaningful (not just navigation/ads)."""
        
        # Filter out common non-content patterns
        skip_patterns = [
            r'^(like|share|comment|követés|megosztás|tetszik)$',
            r'^\d+\s*(perc|óra|nap)',  # Time stamps
            r'^(reklám|hirdetés|sponsored)',
            r'^(cookie|adatvédelem|privacy)',
            r'^\s*$'  # Empty or whitespace
        ]
        
        text_lower = text.lower()
        for pattern in skip_patterns:
            if re.search(pattern, text_lower):
                return False
        
        # Must have some meaningful length
        return len(text) > 10

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """Hungarian Facebook Reader Global Plugin."""
    
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.extractor = WindowsCompatibleContentExtractor()
        log.info("Hungarian Facebook Reader inicializálva")
    
    def _get_current_url(self):
        """Get current browser URL."""
        try:
            # Get focus object
            focus = api.getFocusObject()
            
            # Look for URL in browse mode
            if hasattr(focus, 'treeInterceptor') and focus.treeInterceptor:
                ti = focus.treeInterceptor
                if hasattr(ti, 'rootNVDAObject'):
                    root = ti.rootNVDAObject
                    if hasattr(root, 'URL') and root.URL:
                        return root.URL
            
            # Look up the object hierarchy for URL
            obj = focus
            for _ in range(10):
                if obj:
                    if hasattr(obj, 'URL') and obj.URL:
                        return obj.URL
                    if hasattr(obj, 'value') and obj.value and 'http' in str(obj.value):
                        return obj.value
                    obj = obj.parent
                else:
                    break
            
            return None
            
        except Exception as e:
            log.error(f"Hiba az URL megszerzésekor: {e}")
            return None
    
    def script_readFacebookContent(self, gesture):
        """Read Facebook content intelligently. Gesture: NVDA+Shift+F"""
        
        def extract_and_speak():
            try:
                ui.message("Tartalom betöltése...")
                
                url = self._get_current_url()
                if not url:
                    wx.CallAfter(ui.message, "Nincs URL található. Navigálj egy weboldalra!")
                    return
                
                # Ensure URL is complete
                if not url.startswith('http'):
                    url = 'https://' + url
                
                title, content = self.extractor.extract_content(url)
                
                if content:
                    message = f"Cím: {title}. Tartalom: {content}"
                    wx.CallAfter(speech.speakMessage, message)
                else:
                    wx.CallAfter(ui.message, "Nem sikerült tartalmat kinyerni.")
                    
            except Exception as e:
                log.error(f"Hiba a tartalom olvasásakor: {e}")
                wx.CallAfter(ui.message, f"Hiba történt: {str(e)}")
        
        # Run extraction in background
        thread = threading.Thread(target=extract_and_speak, daemon=True)
        thread.start()
    
    def script_readCurrentElement(self, gesture):
        """Read current focused element. Gesture: NVDA+Shift+R"""
        
        try:
            focus = api.getFocusObject()
            
            if not focus:
                ui.message("Nincs aktív elem.")
                return
            
            # Collect element information
            info_parts = []
            
            if hasattr(focus, 'name') and focus.name:
                info_parts.append(f"Név: {focus.name}")
            
            if hasattr(focus, 'value') and focus.value:
                info_parts.append(f"Érték: {focus.value}")
            
            if hasattr(focus, 'description') and focus.description:
                info_parts.append(f"Leírás: {focus.description}")
            
            if hasattr(focus, 'role') and focus.role:
                role_name = controlTypes.Role.displayString(focus.role) if hasattr(controlTypes.Role, 'displayString') else str(focus.role)
                info_parts.append(f"Típus: {role_name}")
            
            if info_parts:
                message = ". ".join(info_parts)
                speech.speakMessage(message)
            else:
                ui.message("Nincs információ erről az elemről.")
                
        except Exception as e:
            log.error(f"Hiba az elem olvasásakor: {e}")
            ui.message(f"Hiba: {str(e)}")
    
    def script_announcePlugin(self, gesture):
        """Announce plugin status. Gesture: NVDA+Shift+H"""
        ui.message("Hungarian Facebook Reader aktív. NVDA+Shift+F: tartalom olvasása, NVDA+Shift+R: elem olvasása.")
    
    # Script descriptions for input gestures dialog
    script_readFacebookContent.__doc__ = "Facebook és webes tartalom intelligens olvasása"
    script_readCurrentElement.__doc__ = "Aktuális elem információinak felolvasása"
    script_announcePlugin.__doc__ = "Bővítmény állapotának bejelentése"
    
    # Gesture mappings
    __gestures = {
        "kb:NVDA+shift+f": "readFacebookContent",
        "kb:NVDA+shift+r": "readCurrentElement",
        "kb:NVDA+shift+h": "announcePlugin",
    }