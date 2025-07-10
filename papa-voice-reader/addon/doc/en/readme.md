# Papa Voice Reader

## Overview

Papa Voice Reader is an intelligent NVDA add-on that extracts and reads the main content from web pages, news articles, blogs, and Facebook posts while automatically skipping ads, menus, and other clutter.

## Features

- **Intelligent Content Extraction**: Automatically identifies and extracts the main content from web pages
- **Facebook Post Support**: Specialized parser for Hungarian Facebook posts
- **Clutter Removal**: Skips ads, navigation menus, and other distracting elements
- **Easy Activation**: Simple keyboard shortcut to read content instantly

## Installation

1. Download the `papaVoiceReader-1.0.0.nvda-addon` file
2. Open the file with NVDA (or press Enter on it in Windows Explorer)
3. Follow the installation prompts
4. Restart NVDA when prompted

## Usage

1. Navigate to any web page, news article, blog post, or Facebook post
2. Press **NVDA+Alt+I** to activate Papa Voice Reader
3. The add-on will automatically extract and read the main content

## Keyboard Shortcuts

- **NVDA+Alt+I**: Read the main content of the current web page intelligently

## Supported Content Types

- News articles and blog posts
- General web pages
- Hungarian Facebook posts
- Any webpage with identifiable main content

## Requirements

- NVDA 2025.1 or later
- Internet connection for content extraction
- Web browser (Chrome, Firefox, Edge, etc.)

## Compatibility

- **Minimum NVDA Version**: 2025.1
- **Last Tested Version**: 2025.1.2
- **Supported Languages**: Hungarian (specialized Facebook support), English and other languages (general web content)

## Troubleshooting

### Add-on doesn't work
- Ensure you're on a supported web page
- Check that you have an active internet connection
- Verify the page has extractable content

### No content found
- Try refreshing the page and attempting again
- Some pages may not have easily extractable content
- Facebook posts may require being logged in to access

### Error messages
- If you encounter errors, try restarting NVDA
- Check that the webpage has fully loaded before using the add-on

## Technical Details

Papa Voice Reader uses advanced content extraction algorithms including:
- Mozilla's Readability library for general web content
- BeautifulSoup for HTML parsing
- Specialized Facebook post extraction
- Intelligent content filtering and cleanup

## Support

For issues, questions, or feedback:
- Visit: https://github.com/papa-voice/papa-voice-reader
- Report bugs through the GitHub issue tracker

## Version History

### Version 1.0.0
- Initial release
- Intelligent content extraction for web pages
- Hungarian Facebook post support
- NVDA 2025.1+ compatibility
- Keyboard shortcut: NVDA+Alt+I

## License

This add-on is distributed under the GNU General Public License v2.0.

## Credits

- **Author**: fagyhalal
- **Content Extraction**: Mozilla Readability, BeautifulSoup
- **Web Handling**: Python Requests library
- **NVDA Integration**: NVDA Add-on Framework