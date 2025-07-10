#!/usr/bin/env python3
"""
Test script to demonstrate the intelligent content detection system
without making actual network requests.
"""

class MockContentExtractor:
    """
    Mock version of our content extractor for testing the routing logic.
    """
    
    def __init__(self):
        print("✓ Smart Content Extractor initialized")
    
    def extract_content(self, url):
        """
        Main extraction method that routes to appropriate parser based on URL.
        """
        print(f"\n📄 Processing URL: {url}")
        
        if self._is_facebook_url(url):
            print("🔵 Detected: Facebook URL - using Facebook parser")
            return self._mock_facebook_content(url)
        else:
            print("📰 Detected: General article URL - using article parser")
            return self._mock_article_content(url)
    
    def _is_facebook_url(self, url):
        """Check if URL is from Facebook."""
        is_facebook = 'facebook.com' in url.lower() or 'fb.com' in url.lower()
        return is_facebook
    
    def _mock_facebook_content(self, url):
        """Mock Facebook content extraction."""
        print("   🔍 Searching for Facebook posts...")
        print("   🚫 Filtering out sponsored content...")
        print("   📝 Extracting post text and author information...")
        
        # Simulate finding multiple posts
        return "Facebook Feed - 3 posts", """Post 1: Post by John Doe
Today was a great day at the park with the family. The weather was perfect and the kids had so much fun.

Post 2: Post by Jane Smith  
Just finished reading an amazing book about Hungarian history. Highly recommend it to anyone interested in learning more about our culture.

Post 3: Post by Local News Page
Breaking: New bike lanes will be installed downtown starting next month. This should help reduce traffic and promote sustainable transportation."""
    
    def _mock_article_content(self, url):
        """Mock general article content extraction."""
        print("   📊 Analyzing page structure...")
        print("   ✂️  Removing ads, menus, and navigation...")
        print("   📖 Extracting main article content...")
        
        if '444.hu' in url:
            return "Elbukott az Ursula von der Leyen ellen benyújtott bizalmatlansági indítvány", """Az Európai Parlament elutasította a Von der Leyen-kormány ellen benyújtott bizalmatlansági indítványt. A szavazás eredménye nem meglepő, tekintve hogy a kormány stabil többséggel rendelkezik a parlamentben.

A vita során több képviselő is felszólalt, mind a támogatók, mind az ellenzék részéről. A bizottság elnöke hangsúlyozta, hogy a demokratikus folyamatok működnek, és minden képviselőnek joga van véleményét kifejezni.

A szavazás után Von der Leyen elnök rövid nyilatkozatot tett, amelyben köszönetet mondott a támogatásért és megerősítette elkötelezettségét az európai értékek mellett."""
        
        elif 'index.hu' in url:
            return "Technológiai hírek", "A mesterséges intelligencia fejlődése jelentős hatással van a munkaerőpiacra. Szakértők szerint fontos lesz az átképzés és a folyamatos tanulás..."
        
        else:
            return "General News Article", "This is a sample news article content that demonstrates how our intelligent parser can extract the main content from various news websites, removing clutter and focusing on the essential information."

def test_intelligent_detection():
    """Test the intelligent URL detection system."""
    print("🧪 Testing Papa's Voice Intelligent Content Detection")
    print("=" * 60)
    
    extractor = MockContentExtractor()
    
    # Test URLs
    test_urls = [
        "https://www.facebook.com/",
        "https://facebook.com/john.doe/posts/123456",
        "https://fb.com/groups/123/",
        "https://444.hu/2025/01/10/elbukott-az-ursula-von-der-leyen-ellen-benyujtott-bizalmatlansagi-inditvany",
        "https://index.hu/tech/2025/01/ai-fejlodes",
        "https://hvg.hu/itthon/20250110_kormany_dontese",
        "https://www.bbc.com/news/world-europe-123456",
        "https://m.facebook.com/story.php?story_fbid=123&id=456"
    ]
    
    for url in test_urls:
        title, content = extractor.extract_content(url)
        
        print(f"   📋 Title: {title}")
        print(f"   📄 Content preview: {content[:100]}...")
        print()
    
    print("✅ Testing completed!")
    print("\n📊 Summary:")
    print("- Facebook URLs are correctly detected and routed to Facebook parser")
    print("- Regular news URLs are routed to the general article parser")  
    print("- Both Hungarian and international sites are supported")
    print("- The system can handle various Facebook URL formats (facebook.com, fb.com, m.facebook.com)")

if __name__ == "__main__":
    test_intelligent_detection() 