#!/usr/bin/env python3
"""
Update GitHub Actions workflow cron times to match config.py posting schedule.

This script reads the POSTING_SCHEDULE from config.py and updates the
.github/workflows/daily-posts.yml file to use the correct cron times.

Usage:
    python3 update_workflow_schedule.py
"""

import os
import re
import sys
from pathlib import Path

# Add current directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import POSTING_SCHEDULE
except ImportError as e:
    print(f"❌ Error importing config: {e}")
    sys.exit(1)

def time_to_cron(time_str):
    """Convert HH:MM time string to cron format (MM H * * *)"""
    hour, minute = map(int, time_str.split(':'))
    return f"{minute} {hour} * * *"

def get_posting_times():
    """Get the posting times based on configuration"""
    posts_per_day = POSTING_SCHEDULE['posts_per_day']
    custom_times = POSTING_SCHEDULE.get('custom_times')
    
    # Use custom times if set, otherwise use predefined slots
    if custom_times:
        times = custom_times
        print(f"📅 Using custom times: {', '.join(times)}")
    else:
        time_slots = POSTING_SCHEDULE['time_slots']
        if posts_per_day not in time_slots:
            print(f"❌ Invalid posts_per_day: {posts_per_day}")
            print(f"   Valid options: {', '.join(map(str, time_slots.keys()))}")
            sys.exit(1)
        times = time_slots[posts_per_day]
        print(f"📅 Using predefined {posts_per_day} posts/day schedule")
    
    return times

def update_workflow_cron():
    """Update the workflow file with cron times from config"""
    workflow_path = Path(".github/workflows/daily-posts.yml")

    if not workflow_path.exists():
        print(f"❌ Workflow file not found: {workflow_path}")
        return False

    # Read current workflow content
    with open(workflow_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get posting times from config
    times = get_posting_times()
    
    print(f"\n🕐 Configured posting times (UTC):")
    for i, time in enumerate(times, 1):
        cron = time_to_cron(time)
        print(f"   {i}. {time} UTC → cron: '{cron}'")

    # Build new schedule section
    new_schedule_lines = []
    new_schedule_lines.append(f"    # {len(times)} posts per day - Auto-generated from config.py")
    new_schedule_lines.append("    # To change: Edit POSTING_SCHEDULE in config.py, then run: python3 update_workflow_schedule.py")
    
    for time in times:
        cron = time_to_cron(time)
        new_schedule_lines.append(f"    - cron: '{cron}'  # {time} UTC")
    
    new_schedule = "\n".join(new_schedule_lines)
    
    # Replace schedule section - match from "schedule:" to the next section
    # This pattern matches the schedule block including its cron entries
    schedule_pattern = r'(  schedule:\n)(?:    #.*\n)*(?:    - cron:.*\n)+'
    
    new_content = re.sub(
        schedule_pattern,
        f'  schedule:\n{new_schedule}\n',
        content,
        flags=re.MULTILINE
    )
    
    if new_content == content:
        print("\n⚠️  Warning: Workflow content unchanged. Pattern may not have matched.")
        print("   Manual verification recommended.")
        return False
    
    # Write updated content back
    with open(workflow_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("\n✅ Workflow cron times updated successfully!")
    print(f"   Posts per day: {len(times)}")
    print(f"   Times: {', '.join(times)} UTC")
    print("\n📝 Next steps:")
    print("   1. Review changes: git diff .github/workflows/daily-posts.yml")
    print("   2. Commit: git add .github/workflows/daily-posts.yml")
    print("   3. Commit: git commit -m 'Update posting schedule'")
    print("   4. Push: git push")

    return True

if __name__ == "__main__":
    print("🔄 Updating workflow schedule from config.py...")
    print(f"📊 Configuration: {POSTING_SCHEDULE['posts_per_day']} posts per day")
    print()
    
    success = update_workflow_cron()
    
    if not success:
        sys.exit(1)
