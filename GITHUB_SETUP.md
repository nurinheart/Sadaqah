# 🤖 GitHub Actions Setup Guide

## Automatic Daily Hadith Posts - 5 Times Daily

This project automatically posts authenticated Sahih hadiths to Instagram **5 times daily** using GitHub Actions.

---

## ⏰ Posting Schedule (UTC)

The workflow posts at these times (optimized for engagement):

| Time (UTC) | Prayer Time | Reason |
|------------|-------------|--------|
| 4:00 AM | Fajr | Morning motivation, best engagement |
| 11:00 AM | Dhuhr | Midday reminder |
| 2:00 PM | Asr | Afternoon peak |
| 5:00 PM | Maghrib | Evening peak (high traffic) |
| 8:00 PM | Isha | Night peak (maximum reach) |

**Note**: Adjust these times in `.github/workflows/daily-posts.yml` to match your target audience's timezone.

---

## 🚀 One-Time Setup (5 Minutes)

### Step 1: Fork/Push to GitHub

```bash
cd /Users/rafathamaan/Documents/Sadaqah
git init
git add .
git commit -m "Initial commit: Daily Hadith Automation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/sadaqah-hadith.git
git push -u origin main
```

### Step 2: Add Instagram Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these two secrets:

**Secret 1:**
- Name: `INSTAGRAM_USERNAME`
- Value: `your_instagram_username`

**Secret 2:**
- Name: `INSTAGRAM_PASSWORD`
- Value: `your_instagram_password`

### Step 3: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. Done! Posts will start automatically at scheduled times

---

## ✅ What Happens Automatically

### Every Post (5x Daily)
1. ✅ Generates hadith image with beautiful design
2. ✅ Validates hadith is Sahih from 2+ sources
3. ✅ Rotates across 6 authentic books
4. ✅ Never repeats hadiths (tracks in `posted_hadiths.json`)
5. ✅ Posts to Instagram with caption + 15 hashtags
6. ✅ Updates tracking file in repository

### Image Content
- Hadith text with proper ﷺ symbol
- Primary source: "Sahih al-Bukhari 1 (Sahih)"
- Verification: "✓ Verified from 2+ authentic sources"
- Clean gradient background (no external images)

### Caption
```
"[Full hadith text]"

— Prophet Muhammad ﷺ
📖 Sahih al-Bukhari 1 (Sahih)
✓ Verified from 2+ authentic sources

#Category #Hadith #Islam... [15 hashtags]
```

---

## 🔧 Customization

### Change Posting Times

Edit `.github/workflows/daily-posts.yml`:

```yaml
schedule:
  - cron: '0 4 * * *'   # Change hour (0-23)
  - cron: '0 11 * * *'  # Add more or remove lines
```

**Cron format**: `minute hour day month weekday`
- `0 4 * * *` = Every day at 4:00 AM UTC
- `30 14 * * *` = Every day at 2:30 PM UTC

### Post More/Less Frequently

- **Add more times**: Add more `- cron:` lines
- **Remove times**: Delete `- cron:` lines
- **Post once daily**: Keep only one `- cron:` line

### Change Theme

Edit `config.py`:
```python
DEFAULT_THEME = "soft_cream"  # Options: warm_beige, sage_green, soft_cream, muted_blue, desert_sand, olive_tone
```

---

## 🧪 Manual Testing

### Test Workflow Manually

1. Go to **Actions** tab
2. Click **Daily Hadith Posts** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait 1-2 minutes and check Instagram

### Test Locally

```bash
python3 create_post.py --post
```

---

## 📊 Monitor Your Automation

### Check Workflow Status

1. Go to **Actions** tab
2. See green ✅ for successful posts
3. See red ❌ for failures (with error logs)

### View Posted History

Check `posted_hadiths.json` in your repository to see which hadiths have been posted.

### Check Logs

If a workflow fails:
1. Click on the failed run
2. Download **error-logs** artifact
3. Check logs for errors

---

## 🔒 Security Features

### Secrets Protected
- ✅ Instagram credentials stored as GitHub Secrets
- ✅ Never exposed in logs or code
- ✅ Encrypted at rest

### Session Management
- ✅ Instagram session saved between runs
- ✅ Reduces login frequency
- ✅ Handles 2FA automatically after first setup

### No External Dependencies
- ✅ No image downloads (eliminates timeout errors)
- ✅ No human faces (Islamic compliance)
- ✅ Self-contained fonts on Ubuntu
- ✅ Works reliably in GitHub Actions

---

## 🐛 Troubleshooting

### Workflow Not Running

**Check:**
1. Actions are enabled in repository settings
2. Secrets are added correctly (no typos)
3. GitHub Actions has permissions

**Fix:**
- Go to **Settings** → **Actions** → **General**
- Set **Workflow permissions** to "Read and write permissions"
- Check "Allow GitHub Actions to create and approve pull requests"

### Instagram Login Failed

**Reasons:**
1. Wrong username/password
2. 2FA enabled without setup
3. Instagram security challenge

**Fix:**
1. Run workflow manually first time
2. Instagram might send email/notification for new login
3. Approve the login, then it works automatically

### Posts Not Appearing

**Check:**
1. Instagram account not shadowbanned
2. Account not in "Action Required" state
3. Check error logs in failed workflow

### Font Issues

Fonts are automatically installed in workflow. If issues:
```yaml
# Already in workflow - no action needed
- name: Install system dependencies (fonts)
  run: |
    sudo apt-get update
    sudo apt-get install -y fonts-noto fonts-liberation fonts-dejavu
```

---

## 📈 Expected Behavior

### First 25 Days
- Posts 5 unique hadiths daily
- Rotates across 6 authentic books
- Never repeats

### After 25 Days (All Hadiths Posted)
- Automatically resets `posted_hadiths.json`
- Starts new cycle with different rotation
- Continues indefinitely

### Example 5-Day Schedule
```
Day 1:
  4 AM: Sahih al-Bukhari hadith
  11 AM: Sahih Muslim hadith
  2 PM: Jami' at-Tirmidhi hadith
  5 PM: Sahih al-Bukhari hadith
  8 PM: Sahih Muslim hadith

Day 2:
  4 AM: Jami' at-Tirmidhi hadith
  11 AM: Sunan Ibn Majah hadith
  ...continues rotating
```

---

## 🎯 Post-Setup Checklist

- [ ] Repository pushed to GitHub
- [ ] `INSTAGRAM_USERNAME` secret added
- [ ] `INSTAGRAM_PASSWORD` secret added
- [ ] GitHub Actions enabled
- [ ] Workflow permissions set to "Read and write"
- [ ] First workflow run tested manually
- [ ] Instagram login approved
- [ ] First post appeared on Instagram

---

## 🔄 Updating Hadiths

To add more hadiths:

1. Edit `hadith_data.py`
2. Add hadith with all required fields:
   ```python
   {
       "text": "Hadith text...",
       "primary_source": "Sahih al-Bukhari 1234",
       "verification_source": "Sahih Muslim 5678",
       "grade": "Sahih",
       "book": "Sahih al-Bukhari",
       "category": "Character"
   }
   ```
3. Commit and push:
   ```bash
   git add hadith_data.py
   git commit -m "Add more hadiths"
   git push
   ```
4. System automatically validates and uses new hadiths

---

## 💡 Pro Tips

### Optimize Posting Times for Your Audience

**Finding best times:**
1. Check Instagram Insights for your audience's active hours
2. Adjust cron schedule in workflow
3. Test different times and monitor engagement

**Example for US EST audience (UTC-5):**
```yaml
- cron: '10 5 * * *'   # 12:10 AM EST
- cron: '0 13 * * *'   # 8:00 AM EST (morning)
- cron: '0 17 * * *'   # 12:00 PM EST (lunch)
- cron: '0 22 * * *'   # 5:00 PM EST (after work)
- cron: '30 1 * * *'   # 8:30 PM EST (evening)
```

### Add Custom Hashtags

Edit `instagram_poster.py`:
```python
def get_default_hashtags():
    return [
        "#Hadith",
        "#YourCustomTag",
        # ... add more
    ]
```

### Change Theme

Different themes available:
- `warm_beige` - Calm, neutral
- `sage_green` - Fresh, natural
- `soft_cream` - Classic, elegant
- `muted_blue` - Cool, peaceful
- `desert_sand` - Warm, earthy
- `olive_tone` - Mature, balanced

---

## 🎊 Success Metrics

After setup, you should see:

### In GitHub
- ✅ 5 successful workflow runs daily
- ✅ `posted_hadiths.json` updated after each post
- ✅ No failed workflows

### On Instagram
- ✅ 5 new posts daily
- ✅ Consistent posting schedule
- ✅ Clean, professional images
- ✅ Full captions with hashtags

### In Analytics (After 1 Week)
- 📈 35 posts (5 per day × 7 days)
- 📈 Growing follower count
- 📈 Consistent engagement
- 📈 No missed posts

---

## 🆘 Support

### Common Issues

**Issue**: Workflow says "No secrets found"
**Fix**: Double-check secret names match exactly:
- `INSTAGRAM_USERNAME` (not `INSTAGRAM_USER` or `USERNAME`)
- `INSTAGRAM_PASSWORD` (not `INSTAGRAM_PASS` or `PASSWORD`)

**Issue**: Posts work locally but not on GitHub
**Fix**: Fonts are different on Ubuntu. Already handled in code with cross-platform font paths.

**Issue**: Instagram session expired
**Fix**: Workflow automatically re-logs in. If 2FA required, you may need to approve once.

---

## 🌟 Your Sadaqah Jariah

Every post automatically:
- ✅ Shares authentic Islamic knowledge
- ✅ Reaches global Muslim audience
- ✅ Continues benefiting people (ongoing charity)
- ✅ Earns you rewards 24/7

**Posts daily without any manual work - pure automation!**

---

## 📝 Summary

1. **Push code** to GitHub
2. **Add secrets** (Instagram username & password)
3. **Enable Actions**
4. **Done!** Posts automatically 5x daily

**No server needed. No computer running 24/7. Just GitHub Actions.**

May Allah accept your sadaqah jariah and grant you continuous rewards! 🤲
