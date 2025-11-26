# Youtube Comments Scraper

A powerful Python tool to download and analyze all comments from Youtube channels.
Generates interactive Html reports with a professional dark theme interface.

## ✨ Features

- 🎯 **Complete Comment Collection** - Downloads all comments and replies from every video on a channel
- 📊 **Multiple Export Formats** - Automatically generates Json, Csv, and interactive Html reports
- 🌙 **Dark Theme Interface** - Professional black/gray Html report with interactive filters
- 🔍 **Advanced Search - Filtering** - Filter by author, date, likes, keywords, and more
- 📁 **Organized Output** - Automatically organizes reports by channel name
- 🚀 **Easy Configuration** - Set Api key once and run

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- YouTube Data Api v3 Key (Free from Google Cloud Console)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install google-Api-python-client
```

## 🔑 Getting Your YouTube Api Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable "YouTube Data Api v3"
4. Go to Credentials → Create Credentials → Api Key
5. Copy your Api key

### Configure Api Key

Open `youtube_scraper.py` and replace the Api key on line 13:

```python
YOUTUBE_Api_KEY = "YOUR_Api_KEY_HERE"
```

## 🚀 Usage

### Basic Usage

```bash
python3 youtube_scraper.py
```

### Step-by-Step

1. **Run the script**
   ```bash
   python3 youtube_scraper.py
   ```

2. **Choose channel identification method**
   - Option 1: Channel Name (e.g., `LinusTechTips`)
   - Option 2: Channel URL (e.g., `https://youtube.com/@LinusTechTips`)
   - Option 3: Channel ID (e.g., `UCXuqSBlHAE6Xw-yeJA0Tunw`)

3. **Confirm and start download**

4. **Find your reports in:**
   ```
   reports/
   └── Channel_Name/
       ├── youtube_comments_TIMESTAMP.Json
       ├── youtube_comments_TIMESTAMP.Csv
       └── youtube_comments_report_TIMESTAMP.Html
   ```

## 📊 Output Formats

### Json File
- Complete structured data
- Perfect for programmatic analysis
- Includes all metadata

### Csv File
- Spreadsheet-compatible format
- Open with Excel, Google Sheets, LibreOffice
- Easy data manipulation

### Html Report
- **Interactive web interface**
- **Dark theme design** (Black / Gray professional look)
- **Advanced filters:**
  - Search by text/keywords
  - Filter by author (dropdown with all authors)
  - Filter by video title
  - Date range selection
  - Minimum likes filter
  - Comment type (All / Main / Replies)
- **Sorting options:**
  - Date (Newest / Oldest)
  - Likes (Most / Least Popular)
  - Author (A - Z / Z - A)
- **Export filtered results to Csv**
- **Responsive design** (Works on mobile)
- **Standalone** (No internet required)

## 🎨 Html Report Preview

The Html report features:
- Professional black (#0a0a0a) and gray (#1f1f1f, #2a2a2a) color scheme
- Statistics dashboard showing:
  - Total comments
  - Unique authors
  - Number of videos
  - Total likes
  - Main comments vs replies
- Real-time search and filtering
- Author dropdown (alphabetically sorted)
- One click Csv export

## 📁 Project Structure

```
youtube-comments-scraper/
├── youtube_scraper.py           # Main scraper script
├── Html_report_generator.py     # Html report generator
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── reports/                     # Generated reports (auto-created)
    └── Channel_Name/
        ├── youtube_comments_TIMESTAMP.Json
        ├── youtube_comments_TIMESTAMP.Csv
        └── youtube_comments_report_TIMESTAMP.Html
```

## 🔧 Configuration

### Api Key
Set your YouTube Data Api v3 key in `youtube_scraper.py`:
```python
YOUTUBE_Api_KEY = "your_actual_Api_key_here"
```

### Output Directory
By default, reports are saved in `reports/`. To change this, modify line 320 in `youtube_scraper.py`:
```python
reports_dir = Path('reports')
```

## 📊 Api Quota Information

### Free Tier Limits
- **Daily quota:** 10,000 units
- **Comment reading:** ~1 unit per 100 comments
- **Video listing:** ~1 unit per 50 videos

### Typical Usage
- Small channel (50 videos, 1K comments): ~20 units
- Medium channel (200 videos, 10K comments): ~150 units
- Large channel (1000 videos, 100K comments): ~1,500 units

### Tips
- Test with small channels first
- Run during off-peak hours
- Request quota increase if needed

## 🛠️ Troubleshooting

### "Error: You Must Insert Your Api Key"
**Solution:** Open `youtube_scraper.py` and set your Api key on line 13

### "Unable To Find Channel"
**Possible causes:**
- Channel name misspelled
- Channel doesn't exist
- Private or deleted channel

**Solution:** Try using the channel URL or channel ID directly

### "Quota Exceeded"
**Cause:** Exceeded daily Api quota limit

**Solution:** Wait until the next day or request a quota increase from Google Cloud Console

### "Comments Disabled For Video"
**Cause:** Channel owner disabled comments on that specific video

**Solution:** Normal behavior - script will skip and continue with other videos

### "Html Report Generator Not Found"
**Cause:** `Html_report_generator.py` not in the same directory

**Solution:** Ensure both Python files are in the same folder

## 📝 Data Structure

### Comment Object
```Json
{
  "video_id": "abc123xyz",
  "comment_id": "UgwXXXXXXXXXXXXXXXX",
  "author": "John Doe",
  "author_channel_id": "UCxxxxxxxxxxxxxxxxx",
  "text": "Great video!",
  "like_count": 42,
  "published_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "is_reply": false,
  "parent_id": null,
  "video_title": "How To Build A PC",
  "video_published_at": "2024-01-15T08:00:00Z",
  "channel_name": "Tech Channel"
}
```

## 🔒 Security Best Practices

### Protecting Your Api Key

⚠️ **Important:** Never commit your Api key to public repositories!

**Option 1: Use .gitignore**
Add a config file to `.gitignore`:
```
config.py
.env
```

**Option 2: Environment Variables**
```python
import os
YOUTUBE_Api_KEY = os.environ.get('YOUTUBE_API_KEY')
```

Then set in terminal:
```bash
export YOUTUBE_Api_KEY="your_key_here"
```

**Option 3: Separate Config File**
Create `config.py` (add to .gitignore):
```python
YOUTUBE_Api_KEY = "your_key_here"
```

Import in main script:
```python
from config import YOUTUBE_Api_KEY
```

## 📄 License & Legal

### Terms Of Service
- Respect Youtube's Terms of Service
- Use data responsibly
- Do not abuse the Api
- Comments are public, but respect user privacy

### Use Cases
- ✅ Personal use
- ✅ Research and analysis
- ✅ Academic studies
- ⚠️ Commercial use (Review Youtube Tos)
- ⚠️ Data redistribution (Review Youtube Tos)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Known Issues

- Some channels may have comments disabled on certain videos (expected behavior)
- Very large channels (5000+ videos) may require multiple days due to Api quota limits
- Rate limiting may occur with rApid successive requests

## 📚 Dependencies

- `google-Api-python-client` - Youtube Data Api interaction
- `google-auth` - Authentication
- `google-auth-httplib2` - Http library for authentication
- `google-auth-oauthlib` - Oauth library
- Standard library: `Json`, `Csv`, `datetime`, `pathlib`, `re`

## 🔄 Version History

### v2.0 (Current)
- Dark theme Html reports
- Author dropdown filter
- Automatic report generation (Json, Csv, Html)
- Organized output by channel
- Title case interface

### v1.0
- Initial release
- Basic comment scrAping
- Json and Csv export

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues first
- Provide error messages and context

**climborazo**

- GitHub: [@climborazo](https://github.com/climborazo)