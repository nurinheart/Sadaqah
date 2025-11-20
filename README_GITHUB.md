# 📿 Daily Hadith Automation - Sadaqah Jariah

**Automated Instagram posts with authenticated Sahih hadiths - 5 times daily via GitHub Actions**

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Instagram](https://img.shields.io/badge/instagram-automated-purple)
![GitHub Actions](https://img.shields.io/badge/github%20actions-enabled-success)

> Spread authentic Islamic knowledge automatically. Every post is a continuous charity (sadaqah jariah)!

---

## 🌟 Features

### ✅ Automated Posting
- **5 posts daily** via GitHub Actions (no server needed!)
- Posts at optimal times before/around prayer times
- Completely automated - set it and forget it

### ✅ Islamic Authentication
- Every hadith verified from **2+ authentic sources**
- Only **Sahih (authentic)** grade accepted
- Rotates across 6 authentic books
- **Impossible** to post weak/fabricated hadiths

### ✅ Professional Design
- Beautiful gradient backgrounds (6 themes)
- Proper **ﷺ symbol** rendering (60px, Arabic fonts)
- Clean, modern typography
- Instagram-optimized (1080x1350px)

### ✅ No Repeat System
- Tracks all posted hadiths
- Never posts same hadith twice
- Automatic cycle restart after 25 posts

### ✅ Reliable & Halal
- **No external image downloads** (no timeouts, no human faces)
- Pure text-based design
- Cross-platform font support
- Works on GitHub Actions (Ubuntu)

---

## 🚀 Quick Setup (5 Minutes)

### 1. Clone/Fork Repository

```bash
git clone https://github.com/YOUR_USERNAME/sadaqah-hadith.git
cd sadaqah-hadith
```

### 2. Run Setup Script

```bash
chmod +x setup-github.sh
./setup-github.sh
```

### 3. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/sadaqah-hadith.git
git push -u origin main
```

### 4. Add Instagram Secrets

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add `INSTAGRAM_USERNAME` (your Instagram username)
3. Add `INSTAGRAM_PASSWORD` (your Instagram password)

### 5. Enable Actions & Set Permissions

1. Go to **Actions** tab → Enable workflows
2. Go to **Settings** → **Actions** → **General**
3. Set **Workflow permissions** to "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"

### 6. Test First Post

1. Go to **Actions** tab
2. Click **Daily Hadith Posts** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait 1-2 minutes, check your Instagram!

**Done! Posts will now run automatically 5 times daily.**

---

## ⏰ Posting Schedule (UTC)

| Time | Prayer | Reason |
|------|--------|--------|
| 4:00 AM | Fajr | Best morning engagement |
| 11:00 AM | Dhuhr | Midday reminder |
| 2:00 PM | Asr | Afternoon peak |
| 5:00 PM | Maghrib | Evening peak traffic |
| 8:00 PM | Isha | Night peak (maximum reach) |

**Customize times** in `.github/workflows/daily-posts.yml`

---

## 📖 What Gets Posted

### Image Content
```
┌─────────────────────────────────┐
│                                 │
│    The Prophet ﷺ said:          │
│                                 │
│    [Hadith text with            │
│     beautiful typography]       │
│                                 │
│    Sahih al-Bukhari 1 (Sahih)   │
│    ✓ Verified from 2+ sources   │
│                                 │
└─────────────────────────────────┘
```

### Caption
```
"The reward of deeds depends upon intentions..."

— Prophet Muhammad ﷺ
📖 Sahih al-Bukhari 1 (Sahih)
✓ Verified from 2+ authentic sources

#Intention #Hadith #Islam #IslamicQuotes #Muslim
[15 hashtags total]
```

---

## 🎨 Customization

### Change Posting Times

Edit `.github/workflows/daily-posts.yml`:

```yaml
schedule:
  - cron: '0 4 * * *'   # 4:00 AM UTC
  - cron: '0 11 * * *'  # 11:00 AM UTC
  # Add more or adjust times
```

### Change Theme

Edit `config.py`:

```python
DEFAULT_THEME = "soft_cream"
# Options: warm_beige, sage_green, soft_cream, 
#          muted_blue, desert_sand, olive_tone
```

### Add More Hadiths

Edit `hadith_data.py`:

```python
{
    "text": "Your hadith text...",
    "primary_source": "Sahih al-Bukhari 1234",
    "verification_source": "Sahih Muslim 5678",
    "grade": "Sahih",
    "book": "Sahih al-Bukhari",
    "category": "Character"
}
```

System automatically validates authenticity!

---

## 📊 Current Database

- **25 authenticated hadiths**
- **6 authentic books**:
  - Sahih al-Bukhari (10)
  - Sahih Muslim (6)
  - Jami' at-Tirmidhi (6)
  - Sunan Ibn Majah (1)
  - Sunan ad-Daraqutni (1)
  - Sunan an-Nasa'i (1)
- **100% validation rate**
- **All verified from 2+ sources**

---

## 🛠️ Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Generate Post

```bash
python3 create_post.py
```

### Post to Instagram

```bash
python3 create_post.py --post
```

### Validate Hadiths

```bash
python3 validate_hadiths.py
```

---

## 📁 Project Structure

```
sadaqah-hadith/
├── .github/
│   └── workflows/
│       └── daily-posts.yml      # GitHub Actions workflow
├── config.py                     # Themes, fonts, settings
├── hadith_data.py               # 25 authenticated hadiths
├── generate_hadith_post.py      # Image generation
├── create_post.py               # Main entry point
├── instagram_poster.py          # Instagram automation
├── validate_hadiths.py          # Validation tool
├── requirements.txt             # Python dependencies
├── setup-github.sh              # Setup script
├── posted_hadiths.json          # Tracking (auto-updated)
└── GITHUB_SETUP.md              # Detailed instructions
```

---

## 🔒 Security & Privacy

### Secrets Management
- ✅ Instagram credentials stored as GitHub Secrets
- ✅ Never exposed in logs or code
- ✅ Encrypted at rest

### No External Dependencies
- ✅ No image downloads (eliminates timeout errors)
- ✅ No human faces (Islamic compliance)
- ✅ Self-contained fonts
- ✅ Reliable in GitHub Actions

### Session Management
- ✅ Instagram session cached between runs
- ✅ Reduces login frequency
- ✅ Handles 2FA automatically

---

## 🐛 Troubleshooting

### Workflow Not Running

**Check:**
- GitHub Actions enabled
- Secrets added correctly
- Workflow permissions set to "Read and write"

### Instagram Login Failed

**Fix:**
- Verify username/password in secrets
- Approve login notification from Instagram
- Works automatically after first approval

### Posts Not Appearing

**Check:**
- Account not shadowbanned
- Check error logs in failed workflow
- Verify secrets are correct

---

## 📈 Expected Results

### After Setup
- ✅ 5 posts daily, every day
- ✅ No manual intervention needed
- ✅ Automatic hadith rotation
- ✅ Never repeats content

### After 1 Week
- 35 posts (5 per day × 7 days)
- Growing follower count
- Consistent engagement
- Zero missed posts

### After 1 Month
- 150 posts (5 per day × 30 days)
- Established posting schedule
- Audience growth
- Sadaqah jariah benefits

---

## 🤲 Sadaqah Jariah (Ongoing Charity)

Every time someone:
- ✅ Reads your hadith post
- ✅ Learns from it
- ✅ Shares it
- ✅ Acts on it

**You earn continuous rewards!**

The Prophet ﷺ said: *"When a man dies, his good deeds come to an end, except three: ongoing charity, beneficial knowledge, and a righteous son who will pray for him."* - Sahih Muslim 1631

---

## 📚 Documentation

- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** - Complete setup guide
- **[AUTHENTICATION_SYSTEM.md](AUTHENTICATION_SYSTEM.md)** - Hadith validation
- **[AUTO_POSTING_SETUP.md](AUTO_POSTING_SETUP.md)** - Posting automation
- **[QUICK_START.md](QUICK_START.md)** - Quick reference

---

## 🎯 Roadmap

- [x] Automated posting via GitHub Actions
- [x] 5x daily posts at optimal times
- [x] Dual-source hadith verification
- [x] No external image dependencies
- [x] Cross-platform font support
- [ ] Add more hadiths (expand database)
- [ ] Multi-language support (Arabic, Urdu)
- [ ] Instagram Stories support
- [ ] Analytics dashboard

---

## 🤝 Contributing

Contributions welcome! To add hadiths:

1. Fork repository
2. Add authenticated hadiths to `hadith_data.py`
3. Ensure 2+ source verification
4. Run validation: `python3 validate_hadiths.py`
5. Submit pull request

**Important**: Only Sahih hadiths with proper verification!

---

## 📄 License

MIT License - Feel free to use for your own sadaqah jariah projects!

---

## 🌟 Acknowledgments

- **GitHub Actions** - Free automation platform
- **Pillow** - Image generation
- **instagrapi** - Instagram automation
- **Ubuntu Fonts** - Cross-platform support
- **The Ummah** - For inspiring this project

---

## 💬 Support

**Issues?** Open an issue on GitHub
**Questions?** Check documentation files
**Want to help?** Contribute more hadiths!

---

<div align="center">

**May Allah accept this as sadaqah jariah and grant continuous rewards** 🤲

**Made with ❤️ for the Muslim Ummah**

---

*"The best of people are those that bring most benefit to the rest of mankind."*  
— Sunan ad-Daraqutni 2/296 (Sahih)

</div>
