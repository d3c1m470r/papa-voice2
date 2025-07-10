# -*- coding: utf-8 -*-
# Hungarian Facebook Reader for NVDA - Clean Implementation

import threading
import re
import html
from urllib.request import urlopen, Request

# NVDA imports
import globalPluginHandler
import ui
import api
import speech
from logHandler import log
import wx

class ContentExtractor:
	def __init__(self):
		self.timeout = 8
	
	def extract_content(self, url):
		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
			request = Request(url, headers=headers)
			
			with urlopen(request, timeout=self.timeout) as response:
				content = response.read().decode('utf-8', errors='ignore')
			
			title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE)
			title = html.unescape(title_match.group(1)) if title_match else "Nincs cím"
			
			if 'facebook.com' in url.lower():
				posts = []
				patterns = [r'<p[^>]*>(.*?)</p>']
				
				for pattern in patterns:
					matches = re.findall(pattern, content, re.DOTALL)
					for match in matches:
						text = re.sub(r'<[^>]+>', '', match)
						text = html.unescape(text).strip()
						if text and len(text) > 20:
							posts.append(text)
							if len(posts) >= 2:
								break
				
				if posts:
					result = "Facebook: " + " ... ".join(posts)
					return title, result[:500]
			
			# General content
			paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content)
			text = ' '.join(paragraphs[:3])
			text = re.sub(r'<[^>]+>', '', text)
			text = html.unescape(text).strip()
			
			return title, text[:600] if text else "Nincs tartalom"
			
		except Exception as e:
			return None, f"Hiba: {str(e)}"

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.extractor = ContentExtractor()
		log.info("Hungarian Facebook Reader betöltve")
	
	def _get_url(self):
		try:
			focus = api.getFocusObject()
			
			if hasattr(focus, 'treeInterceptor') and focus.treeInterceptor:
				ti = focus.treeInterceptor
				if hasattr(ti, 'rootNVDAObject') and hasattr(ti.rootNVDAObject, 'URL'):
					return ti.rootNVDAObject.URL
			
			obj = focus
			for _ in range(8):
				if obj and hasattr(obj, 'URL') and obj.URL:
					return obj.URL
				obj = obj.parent if obj else None
			
			return None
		except:
			return None
	
	def script_readContent(self, gesture):
		"""Read web content. NVDA+Shift+F"""
		
		def process():
			try:
				ui.message("Betöltés...")
				
				url = self._get_url()
				if not url:
					wx.CallAfter(ui.message, "Nincs URL.")
					return
				
				if not url.startswith('http'):
					url = 'https://' + url
				
				title, content = self.extractor.extract_content(url)
				
				if content and len(content) > 10:
					message = f"{title}. {content}"
					wx.CallAfter(speech.speakMessage, message)
				else:
					wx.CallAfter(ui.message, "Nincs tartalom.")
				
			except Exception as e:
				wx.CallAfter(ui.message, f"Hiba: {str(e)}")
		
		thread = threading.Thread(target=process, daemon=True)
		thread.start()
	
	def script_status(self, gesture):
		"""Plugin status. NVDA+Shift+H"""
		ui.message("Hungarian Facebook Reader aktív.")
	
	# Gesture bindings
	__gestures = {
		"kb:NVDA+shift+f": "readContent",
		"kb:NVDA+shift+h": "status",
	}