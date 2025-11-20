# 📿 Daily Hadith Post Generator

**Modern, Aesthetic, Minimal Islamic Content for Instagram**

Automated Instagram post generator for sharing authentic Sahih hadiths as sadaqah jariah.

## ✨ NEW FEATURES

- ✅ **Modern typography** with Montserrat font (Product Sans alternative)
- ✅ **Fixed ﷺ symbol** display with proper formatting
- ✅ **Optional topic images** - Halal, aesthetic images matching hadith themes
- ✅ **Two modes**: With images or minimal (text-only)
- ✅ **Clean, modern aesthetic** with better spacing
- ✅ **Instagram 4:5 format** (1080x1350px) - perfect for feed posts
- ✅ No duplicate hadiths - tracks what's been posted
- ✅ English translations only
- ✅ Authentic sources (Sahih Bukhari, Sahih Muslim, etc.)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Choose Your Theme

First, generate samples of all themes:

```bash
python generate_hadith_post.py
```

This creates sample images in `theme_samples/` folder. Review them and pick your favorite!

### 3. Set Your Theme

Edit `config.py` and change the `DEFAULT_THEME`:

```python
DEFAULT_THEME = "warm_beige"  # or sage_green, soft_cream, etc.
```

### 4. Generate Daily Posts

Edit `generate_hadith_post.py` and uncomment Option 2 at the bottom:

```python
# Option 2: Generate a single post with default theme
generator = HadithPostGenerator()
generator.generate_post()
```

Run it:
```bash
python generate_hadith_post.py
```

### 5. Post to Instagram

1. Open the generated image from the `output/` folder
2. Upload to Instagram as a post
3. Add Quran recitation from Instagram's music library
4. Post! 🎉

## 🎨 Available Themes

1. **Warm Beige** - Cozy, warm tones with brown text
2. **Sage Green** - Calming green aesthetic
3. **Soft Cream** - Classic cream with charcoal text
4. **Muted Blue** - Peaceful blue palette
5. **Desert Sand** - Sandy, earthy tones
6. **Olive Tone** - Natural olive greens

## 📝 Customization

### Add More Hadiths

Edit `hadith_data.py` and add to the `HADITHS` list:

```python
{
    "text": "Your hadith text here",
    "source": "Sahih al-Bukhari 1234",
    "category": "Category"
}
```

### Change Colors

Edit the theme colors in `config.py`:

```python
THEMES = {
    "your_theme": {
        "bg_colors": ["#COLOR1", "#COLOR2"],  # Gradient colors
        "text_color": "#COLOR3",
        "accent_color": "#COLOR4",
        "source_color": "#COLOR5",
    }
}
```

### Adjust Layout

Modify `config.py`:
- `PADDING` - Space from edges
- Font sizes in `FONTS` dictionary
- `LINE_SPACING` - Space between text lines
- `WATERMARK` - Your account name (or leave empty)

## 🤖 Automation (Optional)

### Daily Generation

Create a cron job (Mac/Linux) to generate daily:

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 8 AM
0 8 * * * cd /Users/rafathamaan/Documents/Sadaqah && /usr/local/bin/python3 generate_hadith_post.py
```

### Cloud Automation

Deploy to a cloud service (AWS Lambda, Google Cloud Functions, etc.) to:
1. Generate posts automatically
2. Store them in cloud storage
3. Optionally: Auto-post via Instagram API (requires business account)

## 📊 Tracking

The script automatically tracks posted hadiths in `posted_hadiths.json` to avoid repeats.

To reset and start over:
```bash
rm posted_hadiths.json
```

## 🎵 Suggested Quran Tracks for Instagram

When posting, add these surahs as background music:
- Surah Ar-Rahman (Most popular)
- Surah Al-Mulk
- Surah Ya-Sin
- Surah Al-Kahf
- Surah Al-Waqiah

## 📱 Posting Tips

1. **Consistency** - Post at the same time daily
2. **Hashtags** - Use relevant Islamic hashtags
3. **Engagement** - Reply to comments, build community
4. **Stories** - Repost to stories for more reach
5. **Pin important posts** - Pin your intro post

## 🤲 Making it Sadaqah Jariah

1. Open source this on GitHub for others to use
2. Encourage shares and saves
3. Keep content authentic and beneficial
4. Never monetize - keep it purely for Allah's sake
5. Remind people to share for barakah

## 🛠️ Troubleshooting

**Fonts look wrong?**
- The script uses system fonts. Edit `get_font()` in `generate_hadith_post.py` to specify fonts installed on your system.

**Colors not showing?**
- Make sure hex colors in `config.py` start with `#` and are 6 digits

**Image quality?**
- Images are saved at 95% quality. For perfect quality, change `quality=95` to `quality=100`

## 📄 License

Free to use for dawah and sadaqah purposes. Not for commercial use.

---

**May Allah accept this as sadaqah jariah and grant you continuous rewards! 🤲**
