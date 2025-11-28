# Posting Schedule Configuration Guide

## Overview

The Sadaqah project now supports flexible posting frequencies - you can easily configure how many hadith posts are published per day (1-5 posts) by simply editing `config.py` and running a single command.

## Quick Start

### Change Posting Frequency

1. **Edit `config.py`**:
   ```python
   POSTING_SCHEDULE = {
       "posts_per_day": 3,  # Change this number (1-5)
       # ... rest of config
   }
   ```

2. **Update the workflow**:
   ```bash
   python3 update_workflow_schedule.py
   ```

3. **Commit and push**:
   ```bash
   git add config.py .github/workflows/daily-posts.yml
   git commit -m "Update posting schedule to 3 posts per day"
   git push
   ```

That's it! GitHub Actions will now run at the new times.

## Predefined Schedules

The system includes optimized time slots for different posting frequencies:

| Posts/Day | Times (UTC) | Description |
|-----------|-------------|-------------|
| 1 | 12:00 | Midday post |
| 2 | 06:00, 18:00 | Morning & evening |
| 3 | 06:00, 12:00, 18:00 | Morning, noon, evening |
| 4 | 06:00, 11:00, 15:00, 20:00 | Spread throughout day |
| 5 | 04:00, 11:00, 14:00, 17:00, 20:00 | Prayer times alignment |

## Custom Times

Want specific posting times? Use `custom_times` in `config.py`:

```python
POSTING_SCHEDULE = {
    "posts_per_day": 3,  # This is ignored when custom_times is set
    
    # Your custom times (UTC)
    "custom_times": ["08:30", "14:15", "19:45"],
    
    # ... rest of config
}
```

Then run `python3 update_workflow_schedule.py` to apply.

## Technical Details

### How It Works

1. **Configuration**: `config.py` contains `POSTING_SCHEDULE` dict
2. **Update Script**: `update_workflow_schedule.py` reads config and updates workflow YAML
3. **Workflow**: `.github/workflows/daily-posts.yml` has cron schedules that trigger posts
4. **Automation**: GitHub Actions runs at scheduled times and posts hadiths

### Files Modified

- `config.py` - Your posting schedule configuration
- `.github/workflows/daily-posts.yml` - GitHub Actions cron times (auto-updated)

### Timezone Note

All times in `config.py` are **UTC**. Convert your local time to UTC:

- EST/EDT (New York): UTC -5/-4
- PST/PDT (Los Angeles): UTC -8/-7
- GMT (London): UTC +0
- IST (India): UTC +5:30
- AEST (Sydney): UTC +10

Example: To post at 9 AM EST (UTC-5), set time to `14:00` UTC.

## Validation

The updater script validates your configuration:

- ✅ Checks `posts_per_day` is between 1-5
- ✅ Verifies time format (HH:MM)
- ✅ Confirms workflow file exists
- ✅ Shows what times will be used

## Troubleshooting

### Script shows "Pattern may not have matched"

The workflow file format might have changed. Check:
```bash
head -15 .github/workflows/daily-posts.yml
```

Should see `schedule:` section with cron times.

### Times not updating

1. Make sure you saved `config.py`
2. Re-run: `python3 update_workflow_schedule.py`
3. Check git status: `git status`
4. Verify: `git diff .github/workflows/daily-posts.yml`

### Posts not running at expected times

Remember:
- Times are in **UTC**, not your local time
- GitHub Actions may have up to 5-10 minute delays
- Check Actions tab on GitHub for execution logs

## Examples

### Morning and Evening Posts
```python
"posts_per_day": 2  # 06:00 and 18:00 UTC
```

### Three Times a Day
```python
"posts_per_day": 3  # 06:00, 12:00, 18:00 UTC
```

### Custom Schedule (Prayer Times)
```python
"custom_times": ["05:30", "13:00", "16:30", "19:00", "21:00"]
```

## Benefits

- ✅ **Flexible**: Change frequency anytime
- ✅ **Simple**: Edit one number in config.py
- ✅ **Validated**: Script checks for errors
- ✅ **Visible**: See exact times before applying
- ✅ **Tracked**: Workflow changes are in git

## Support

Created: January 2025  
For issues or questions about the posting schedule system, check the configuration in `config.py` or review the workflow in `.github/workflows/daily-posts.yml`.
