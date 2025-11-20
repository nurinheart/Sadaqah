# 🚀 QUICK START GUIDE

Welcome! Your Daily Hadith Post Generator is ready to use. Here's everything you need to know in 2 minutes.

## ✅ What's Ready

- ✅ Modern, aesthetic design with Montserrat font
- ✅ Fixed ﷺ symbol (displays as (ﷺ))
- ✅ 20 authentic hadiths loaded
- ✅ 6 beautiful color themes
- ✅ Two modes: with images or minimal
- ✅ Instagram-ready format (1080x1350px)
- ✅ Auto-tracking (no repeats)

## 📂 Check Your Samples

1. Open **`samples_minimal/`** - Clean text-only designs
2. Open **`samples_with_images/`** - Designs with topic images
3. Pick which style you prefer!

## ⚡ Generate Your First Post

### Super Simple:
```bash
python3 create_post.py
```

That's it! Your post is in the `output/` folder.

## ⚙️ Quick Settings

### Turn images ON or OFF:
```bash
python3 settings.py images off    # Minimal mode (recommended)
python3 settings.py images on     # With images mode
```

### Change color theme:
```bash
python3 settings.py theme sage_green
```

Options: `warm_beige`, `sage_green`, `soft_cream`, `muted_blue`, `desert_sand`, `olive_tone`

### Add your watermark:
```bash
python3 settings.py watermark your_account_name
```

## 📱 Post to Instagram

1. **Generate**: `python3 create_post.py`
2. **Open** the image from `output/` folder
3. **Upload** to Instagram
4. **Add music**: Search "Quran" in Instagram music
   - Surah Ar-Rahman (most popular)
   - Surah Al-Mulk
   - Surah Ya-Sin
5. **Add hashtags**:
   ```
   #Hadith #Islam #IslamicQuotes #Muslim #ProphetMuhammad 
   #IslamicReminders #SahihBukhari #Quran #Allah #Deen
   ```
6. **Post!** 🚀

## 🎨 Recommended Setup for Beginners

```bash
# 1. Use minimal mode (cleaner, more consistent)
python3 settings.py images off

# 2. Pick warm beige theme (classic, proven)
python3 settings.py theme warm_beige

# 3. Add your account name
python3 settings.py watermark your_account

# 4. Generate your first post!
python3 create_post.py
```

## 📅 Daily Workflow

Every day:
1. Run: `python3 create_post.py`
2. Upload to Instagram with Quran music
3. That's it! The script handles everything else.

## 🤖 Automate It (Optional)

Set it to auto-generate every day at 8 AM:

```bash
crontab -e
```

Add this line:
```
0 8 * * * cd /Users/rafathamaan/Documents/Sadaqah && /usr/local/bin/python3 create_post.py
```

## ❓ Quick Troubleshooting

**Problem**: ﷺ symbol looks weird
- **Solution**: It now shows as (ﷺ) - this is intentional for better font compatibility

**Problem**: Fonts look basic
- **Solution**: Montserrat is downloaded. If issues, it falls back to system fonts (still looks good!)

**Problem**: Images not downloading
- **Solution**: Check internet connection, or just disable images: `python3 settings.py images off`

**Problem**: Want to start over with hadiths
- **Solution**: Delete `posted_hadiths.json` to reset tracking

## 📚 More Help

- **Design tips**: Read `DESIGN_GUIDE.md`
- **Full documentation**: Read `README.md`
- **Add more hadiths**: Edit `hadith_data.py`
- **Customize colors**: Edit `config.py`

## 💡 Pro Tips

1. **Be consistent**: Post same time daily
2. **One theme**: Stick to one color theme for brand consistency
3. **Engage**: Reply to all comments
4. **Share to stories**: More reach!
5. **Track analytics**: See what times get best engagement

## 🤲 Making it Sadaqah Jariah

This tool is designed to:
- ✅ Share authentic Islamic knowledge
- ✅ Reach people continuously (even while you sleep!)
- ✅ Never repeat hadiths
- ✅ Be completely free and open source
- ✅ Earn you ongoing rewards from every person who benefits

**May Allah accept this and make it a means of continuous good deeds for you! 🤲**

---

## 🎯 Your Action Items Right Now:

1. ✅ Check `samples_minimal/` and `samples_with_images/` folders
2. ✅ Decide: images ON or OFF? (`python3 settings.py images off`)
3. ✅ Pick a theme (`python3 settings.py theme warm_beige`)
4. ✅ Generate first post (`python3 create_post.py`)
5. ✅ Post to Instagram!

**You're all set! 🚀**
