import requests
from bs4 import BeautifulSoup
import html2text
import re

class FacebookParser:
    def __init__(self):
        self.h = html2text.HTML2Text()
        self.h.ignore_links = True
        self.h.ignore_images = True
        
    def extract_facebook_posts(self, url):
        """
        Extracts posts from a Facebook feed page.
        Returns a list of post dictionaries with title and content.
        """
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return [{"title": "Error", "content": f"Error fetching Facebook page: {e}"}]

        soup = BeautifulSoup(response.text, 'html.parser')
        posts = []
        
        # Facebook post containers - based on research about Facebook's DOM structure
        # Look for various possible post container selectors
        post_selectors = [
            '[data-testid="Keycommand_wrapper_feed_story"]',  # Main feed posts
            '[data-pagelet*="FeedUnit"]',  # Alternative feed structure
            '[role="article"]',  # ARIA article role posts
            '[data-testid*="story"]',  # Story containers
        ]
        
        found_posts = []
        for selector in post_selectors:
            found_posts.extend(soup.select(selector))
        
        # If no specific post containers found, try to find content blocks
        if not found_posts:
            # Fallback: look for div elements that might contain posts
            found_posts = soup.find_all('div', class_=re.compile(r'.*'))
            # Filter for elements that are likely posts (have substantial content)
            found_posts = [post for post in found_posts if post.get_text(strip=True) and len(post.get_text(strip=True)) > 50]
        
        for i, post_element in enumerate(found_posts[:10]):  # Limit to first 10 posts
            try:
                post_data = self._extract_post_data(post_element, i)
                if post_data:
                    posts.append(post_data)
            except Exception as e:
                # Continue processing other posts if one fails
                continue
        
        if not posts:
            # Fallback: if no posts found, return a general description of the page
            page_text = soup.get_text()[:1000]  # First 1000 characters
            clean_text = self.h.handle(page_text)
            posts.append({
                "title": "Facebook Page Content",
                "content": clean_text
            })
        
        return posts
    
    def _extract_post_data(self, post_element, post_index):
        """
        Extracts data from a single Facebook post element.
        """
        # Skip if this looks like an ad (contains "Sponsored" text)
        post_text = post_element.get_text()
        if self._is_sponsored_content(post_element, post_text):
            return None
        
        # Try to find post author/title
        title = self._extract_post_title(post_element, post_index)
        
        # Extract main content
        content = self._extract_post_content(post_element)
        
        if not content or len(content.strip()) < 20:
            return None
            
        return {
            "title": title,
            "content": content
        }
    
    def _is_sponsored_content(self, post_element, post_text):
        """
        Detects if a post is sponsored/ad content using various methods.
        """
        # Method 1: Look for "Sponsored" text variations
        sponsored_patterns = [
            r'sponsored',
            r'hirdetés',  # Hungarian for advertisement
            r'reklám',    # Hungarian for ad
            r'promoted',
            r'promóció'   # Hungarian for promotion
        ]
        
        for pattern in sponsored_patterns:
            if re.search(pattern, post_text, re.IGNORECASE):
                return True
        
        # Method 2: Check for spans with "Sponsored" in data attributes or aria-labels
        sponsored_spans = post_element.find_all('span', attrs={
            'aria-labelledby': True
        })
        
        for span in sponsored_spans:
            labelledby_id = span.get('aria-labelledby')
            if labelledby_id:
                # Look for the element with this ID
                label_element = post_element.find(id=labelledby_id)
                if label_element and 'sponsored' in label_element.get_text().lower():
                    return True
        
        # Method 3: Look for common ad-related class names or attributes
        ad_indicators = [
            'sponsored',
            'ad-',
            'advertisement',
            'promo'
        ]
        
        for indicator in ad_indicators:
            if post_element.find(attrs={'class': re.compile(indicator, re.I)}):
                return True
        
        return False
    
    def _extract_post_title(self, post_element, post_index):
        """
        Extracts a title for the post (author name, page name, etc.)
        """
        # Try to find author/poster name
        title_selectors = [
            'h2 a',  # Common pattern for post author
            'h3 a',  # Alternative heading pattern
            '[data-testid*="author"]',  # Author containers
            'strong',  # Bold text often contains names
            '[role="link"]'  # Link elements that might be names
        ]
        
        for selector in title_selectors:
            title_element = post_element.select_one(selector)
            if title_element:
                title_text = title_element.get_text(strip=True)
                if title_text and len(title_text) < 100:  # Reasonable title length
                    return f"Post by {title_text}"
        
        # Fallback
        return f"Facebook Post {post_index + 1}"
    
    def _extract_post_content(self, post_element):
        """
        Extracts the main content text from a post.
        """
        # Remove script and style elements
        for script in post_element(["script", "style"]):
            script.decompose()
        
        # Try to find the main text content area
        text_selectors = [
            '[data-testid*="text"]',  # Text content containers
            '[data-testid*="content"]',  # Content containers
            'p',  # Paragraph elements
            '[role="text"]'  # Text role elements
        ]
        
        content_parts = []
        
        for selector in text_selectors:
            text_elements = post_element.select(selector)
            for element in text_elements:
                text = element.get_text(strip=True)
                if text and len(text) > 10:  # Skip very short text
                    content_parts.append(text)
        
        if content_parts:
            # Join and deduplicate content
            content = ' '.join(content_parts)
            # Remove excessive whitespace
            content = re.sub(r'\s+', ' ', content)
            return content[:2000]  # Limit length
        
        # Fallback: get all text from the post element
        all_text = post_element.get_text(separator=' ', strip=True)
        # Clean up the text
        all_text = re.sub(r'\s+', ' ', all_text)
        return all_text[:1000] if all_text else ""

def extract_facebook_content(url):
    """
    Main function to extract content from Facebook URLs.
    """
    parser = FacebookParser()
    
    if 'facebook.com' in url.lower() or 'fb.com' in url.lower():
        posts = parser.extract_facebook_posts(url)
        
        # Format the output for the screen reader
        if len(posts) == 1:
            return posts[0]['title'], posts[0]['content']
        else:
            # Multiple posts - combine them
            title = f"Facebook Feed - {len(posts)} posts"
            content_parts = []
            for i, post in enumerate(posts, 1):
                content_parts.append(f"Post {i}: {post['title']}\n{post['content']}")
            
            combined_content = '\n\n'.join(content_parts)
            return title, combined_content
    else:
        # Not a Facebook URL
        return "Not Facebook Content", "This URL is not from Facebook."

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python facebook_parser.py <FACEBOOK_URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    title, content = extract_facebook_content(url)
    
    print(f"--- Title ---\n{title}\n")
    print(f"--- Content ---\n{content}\n") 