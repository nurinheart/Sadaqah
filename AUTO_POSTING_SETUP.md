# 🤖 Automatic Daily Posting Setup

## How to Post Automatically to Instagram

Currently, the system posts **ONLY when you run the command manually**. Here's how to set up automatic daily posting:

---

## Option 1: macOS Cron Job (Recommended)

### Step 1: Create Launch Agent
```bash
mkdir -p ~/Library/LaunchAgents
```

### Step 2: Create Plist File
```bash
nano ~/Library/LaunchAgents/com.sadaqah.dailyhadith.plist
```

### Step 3: Add This Configuration
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sadaqah.dailyhadith</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/rafathamaan/Documents/Sadaqah/create_post.py</string>
        <string>--post</string>
    </array>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    
    <key>WorkingDirectory</key>
    <string>/Users/rafathamaan/Documents/Sadaqah</string>
    
    <key>StandardOutPath</key>
    <string>/Users/rafathamaan/Documents/Sadaqah/logs/output.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/rafathamaan/Documents/Sadaqah/logs/error.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
```

**This posts daily at 9:00 AM**

### Step 4: Create Logs Directory
```bash
mkdir -p /Users/rafathamaan/Documents/Sadaqah/logs
```

### Step 5: Load the Launch Agent
```bash
launchctl load ~/Library/LaunchAgents/com.sadaqah.dailyhadith.plist
```

### Step 6: Verify It's Loaded
```bash
launchctl list | grep sadaqah
```

---

## Option 2: Cron Job (Alternative)

### Step 1: Edit Crontab
```bash
crontab -e
```

### Step 2: Add This Line
```bash
# Post daily hadith at 9:00 AM
0 9 * * * cd /Users/rafathamaan/Documents/Sadaqah && /usr/local/bin/python3 create_post.py --post >> logs/output.log 2>&1
```

### Step 3: Save and Exit
Press `Esc`, type `:wq`, press `Enter`

---

## ⏰ Customize Posting Time

Change the `Hour` and `Minute` values:

### Popular Times (with reasoning):

**9:00 AM** - Morning motivation
```xml
<key>Hour</key>
<integer>9</integer>
<key>Minute</key>
<integer>0</integer>
```

**12:00 PM** - Midday reminder
```xml
<key>Hour</key>
<integer>12</integer>
<key>Minute</key>
<integer>0</integer>
```

**6:00 PM** - After Asr prayer
```xml
<key>Hour</key>
<integer>18</integer>
<key>Minute</key>
<integer>0</integer>
```

**9:00 PM** - Evening reflection
```xml
<key>Hour</key>
<integer>21</integer>
<key>Minute</key>
<integer>0</integer>
```

---

## 📅 Post Multiple Times Per Day

### Add Multiple Calendar Intervals

```xml
<key>StartCalendarInterval</key>
<array>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <dict>
        <key>Hour</key>
        <integer>18</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</array>
```

**This posts twice daily: 9 AM and 6 PM**

---

## 🔍 Check Logs

### View Output Log
```bash
tail -f /Users/rafathamaan/Documents/Sadaqah/logs/output.log
```

### View Error Log
```bash
tail -f /Users/rafathamaan/Documents/Sadaqah/logs/error.log
```

---

## 🛑 Stop Automatic Posting

### Unload Launch Agent
```bash
launchctl unload ~/Library/LaunchAgents/com.sadaqah.dailyhadith.plist
```

### Remove Cron Job
```bash
crontab -e
# Delete the line with create_post.py
```

---

## ✅ Current System Features

### 1. Auto-Posting
✅ **Caption**: Includes full hadith text + source + verification
✅ **Hashtags**: 15 relevant Islamic hashtags automatically added
✅ **Image**: Generated with proper formatting

### 2. No Repeats System
✅ Tracks all posted hadiths in `posted_hadiths.json`
✅ Never posts the same hadith twice
✅ When all 25 hadiths posted, automatically resets and starts over
✅ Book rotation ensures variety

### 3. Authentication Display
✅ Shows primary source: "Sahih al-Bukhari 1 (Sahih)"
✅ Shows verification: "✓ Verified from 2+ authentic sources"
✅ No specific second source shown (as you requested)

---

## 📱 What Gets Posted Automatically

### Image
- Beautiful gradient background
- Hadith text with proper ﷺ symbol (60px)
- Source: "Sahih al-Bukhari 1 (Sahih)"
- Verification: "✓ Verified from 2+ authentic sources"

### Caption
```
"The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended."

— Prophet Muhammad ﷺ
📖 Sahih al-Bukhari 1 (Sahih)
✓ Verified from 2+ authentic sources

#Intention #Hadith #Islam #IslamicQuotes #Muslim #ProphetMuhammad...
```

### Hashtags (15 total)
```
#Hadith #Islam #IslamicQuotes #Muslim #ProphetMuhammad 
#IslamicReminders #SahihBukhari #Quran #Allah #Deen 
#IslamicPost #MuslimCommunity #IslamicKnowledge #Sunnah #Dawah
```

---

## ⚠️ Important: Quran Audio

Instagram API doesn't support adding music automatically. You'll need to:

1. **Option A**: Add music manually to first few posts
2. **Option B**: Use Instagram's "Save as Draft" feature:
   - Post saves as draft automatically
   - You add music manually
   - Then publish

*Unfortunately, there's no way to auto-add music via API*

---

## 🔢 Posting Frequency & Rotation

### Current Stats
- **Total Hadiths**: 25 Sahih authenticated
- **Posting Pattern**: Rotates across 6 books
- **No Repeats**: Tracks in posted_hadiths.json
- **After 25 Posts**: Automatically resets and starts over

### Example 25-Day Cycle
```
Day 1: Sahih al-Bukhari hadith
Day 2: Sahih Muslim hadith
Day 3: Jami' at-Tirmidhi hadith
Day 4: Sahih al-Bukhari hadith
...
Day 25: Last hadith
Day 26: Cycle restarts (different rotation)
```

---

## 🧪 Test Automatic Posting

### Test Launch Agent (without waiting)
```bash
launchctl start com.sadaqah.dailyhadith
```

### Check if it worked
```bash
cat /Users/rafathamaan/Documents/Sadaqah/logs/output.log
```

### Test Manual Posting
```bash
python3 create_post.py --post
```

---

## 📊 Monitor Your Posts

### Check Posted History
```bash
cat posted_hadiths.json
```

Shows indices of all posted hadiths.

### Check Logs
```bash
# Last 20 lines of output
tail -20 logs/output.log

# Real-time monitoring
tail -f logs/output.log
```

---

## 💡 Pro Tips

### 1. Computer Must Be On
Launch Agents only run when Mac is powered on. Consider:
- Using a always-on Mac Mini
- Using cloud server (VPS)
- Manual posting if computer sleeps

### 2. Instagram Session
- System saves session in `instagram_session.json`
- Remains logged in between posts
- Re-login only if session expires

### 3. Two-Factor Authentication
- If Instagram has 2FA enabled
- First run will ask for code
- Saves session for future posts

---

## 🚀 Quick Setup Command

Run this to set up daily 9 AM posting:

```bash
# Create logs directory
mkdir -p ~/Documents/Sadaqah/logs

# Create launch agent
cat > ~/Library/LaunchAgents/com.sadaqah.dailyhadith.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sadaqah.dailyhadith</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/rafathamaan/Documents/Sadaqah/create_post.py</string>
        <string>--post</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/rafathamaan/Documents/Sadaqah</string>
    <key>StandardOutPath</key>
    <string>/Users/rafathamaan/Documents/Sadaqah/logs/output.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/rafathamaan/Documents/Sadaqah/logs/error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOF

# Load it
launchctl load ~/Library/LaunchAgents/com.sadaqah.dailyhadith.plist

# Test it
launchctl start com.sadaqah.dailyhadith

echo "✅ Setup complete! Check logs/output.log for results"
```

---

## ✅ Summary

| Feature | Status |
|---------|--------|
| Auto-posting with caption | ✅ Yes |
| Auto-posting with hashtags | ✅ Yes (15 hashtags) |
| Auto-posting with Quran audio | ❌ Must add manually |
| No repeat hadiths | ✅ Yes (tracked) |
| Automatic timing | ⚠️ Set up Launch Agent |
| Book rotation | ✅ Yes (6 books) |
| Verification display | ✅ Yes (simplified) |

**Run `python3 create_post.py --post` to test the new caption!**
