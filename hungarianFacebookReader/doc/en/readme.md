# Hungarian Facebook Reader for NVDA

## Overview

This NVDA add-on provides intelligent Facebook content reading optimized for Hungarian users. It helps blind and visually impaired users access Facebook content more efficiently by filtering out ads and providing clean, summarized content.

## Features

- **Windows Compatible**: Uses only Python standard library modules included with NVDA
- **Hungarian Language Support**: All messages and interface in Hungarian
- **Intelligent Content Extraction**: Filters Facebook posts and general web content
- **No External Dependencies**: Works without additional libraries
- **Background Processing**: Non-blocking content extraction

## Keyboard Shortcuts

- **NVDA+Shift+F**: Read Facebook/web content intelligently
- **NVDA+Shift+R**: Read current element information
- **NVDA+Shift+H**: Announce plugin status

## Installation

1. Download the `hungarianFacebookReader.nvda-addon` file
2. Open NVDA
3. Go to Tools > Manage Add-ons
4. Click "Install" and select the downloaded file
5. Restart NVDA when prompted

## Usage

### Reading Facebook Content
1. Navigate to a Facebook page in your web browser
2. Press **NVDA+Shift+F** to extract and read the main content
3. The add-on will identify Facebook posts and read them cleanly

### Reading General Web Content
1. Navigate to any webpage
2. Press **NVDA+Shift+F** to extract the main article content
3. The add-on will identify and read the primary content area

### Reading Current Element
1. Navigate to any element on a webpage
2. Press **NVDA+Shift+R** to get detailed information about the current element

## Requirements

- **NVDA**: Version 2019.3 or later
- **Windows**: Windows 7 or later
- **Python**: Python 3.7+ (included with modern NVDA)
- **Internet**: Required for content extraction

## Compatibility

This add-on is designed for maximum Windows compatibility:
- Uses only Python standard library modules
- No external dependencies (requests, beautifulsoup, etc.)
- Compatible with all NVDA versions from 2019.3+
- Works with all major web browsers

## Supported Websites

- **Facebook**: Optimized post extraction and reading
- **News websites**: Article content extraction
- **Blogs**: Main content identification
- **General web pages**: Content area detection

## Hungarian Language Features

- All user messages in Hungarian
- Optimized for Hungarian Facebook content
- Hungarian-specific content filtering patterns
- Cultural context awareness

## Technical Details

### Libraries Used
- `urllib.request`: For web requests (Python standard library)
- `html`: For HTML entity decoding (Python standard library)
- `re`: For text pattern matching (Python standard library)
- `threading`: For background processing (Python standard library)

### Content Extraction
- Facebook-specific DOM pattern recognition
- General web content area detection
- HTML tag cleaning and text normalization
- Intelligent content filtering

## Troubleshooting

### Content Extraction Fails
1. Ensure you're on a webpage with accessible content
2. Check your internet connection
3. Try refreshing the page and using the shortcut again
4. Check NVDA's log viewer for detailed error messages

### Add-on Not Working
1. Verify NVDA version is 2019.3 or later
2. Restart NVDA after installation
3. Check that gestures aren't conflicting with other add-ons
4. Review NVDA log for error messages

### Facebook Content Not Found
1. Ensure you're logged into Facebook
2. Try on different Facebook pages (timeline, posts, groups)
3. Facebook's structure changes frequently - content may vary

## Performance

- Background processing prevents NVDA freezing
- Intelligent timeout handling for slow connections
- Memory-efficient text processing
- Minimal impact on NVDA performance

## Privacy and Security

- No data collection or transmission
- Content processing happens locally
- No cookies or session storage
- Respects user privacy completely

## Future Enhancements

- Enhanced Hungarian language processing
- Support for Facebook comments and reactions
- Customizable content filtering options
- Additional social media platform support
- Voice rate optimization for Hungarian speech

## Contributing

Contributions welcome for:
- Improving Facebook content detection patterns
- Adding support for more Hungarian websites
- Enhancing content filtering algorithms
- Bug fixes and performance improvements

## License

Released under GNU General Public License v2.0, same as NVDA.

## Support

For support, please:
1. Check this documentation first
2. Review NVDA's log viewer for errors
3. Test with different websites and content
4. Report issues with specific examples