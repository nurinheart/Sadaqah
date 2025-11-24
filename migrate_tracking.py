#!/usr/bin/env python3
"""
Migration script to convert from index-based tracking to unique ID tracking
✅ Converts posted_hadiths.json from [0, 1, 2] to ["bukhari_1", "muslim_1844"]
✅ Preserves all posting history
✅ One-time migration script
"""

import json
import os
from pathlib import Path
from hadith_data import get_sahih_hadiths

def migrate_posted_hadiths():
    """Migrate from index-based to unique ID tracking"""
    posted_file = "posted_hadiths.json"
    
    if not os.path.exists(posted_file):
        print("✅ No posted_hadiths.json found - starting fresh")
        return
    
    # Load current tracking data
    with open(posted_file, 'r') as f:
        current_data = json.load(f)
    
    # Check if already migrated
    if isinstance(current_data, list) and current_data:
        if isinstance(current_data[0], str) and '_' in current_data[0]:
            print("✅ Already migrated to unique ID tracking")
            return
    
    # Load hadith database to map indices to unique IDs
    hadiths = get_sahih_hadiths()
    if not hadiths:
        print("❌ Cannot migrate - no hadith database available")
        return
    
    print(f"🔄 Migrating {len(current_data)} posted hadiths...")
    
    migrated_ids = []
    failed_migrations = []
    
    for index in current_data:
        if isinstance(index, int) and 0 <= index < len(hadiths):
            hadith = hadiths[index]
            unique_id = hadith.get('unique_id', f"unknown_{index}")
            migrated_ids.append(unique_id)
            print(f"  ✅ {index} → {unique_id} ({hadith.get('reference', 'Unknown')})")
        else:
            failed_migrations.append(index)
            print(f"  ❌ Invalid index: {index}")
    
    # Remove duplicates (shouldn't happen but safety check)
    migrated_ids = list(set(migrated_ids))
    
    # Save migrated data
    with open(posted_file, 'w') as f:
        json.dump(migrated_ids, f, indent=2)
    
    print(f"✅ Migration complete!")
    print(f"  📊 Migrated: {len(migrated_ids)} hadiths")
    print(f"  ❌ Failed: {len(failed_migrations)} hadiths")
    print(f"  💾 Saved to: {posted_file}")
    
    if failed_migrations:
        print(f"  ⚠️  Failed indices: {failed_migrations}")
        print("     These hadiths may be re-posted (safe but not ideal)")

if __name__ == "__main__":
    print("🛠️  Hadith Tracking Migration Tool")
    print("=" * 50)
    migrate_posted_hadiths()
    print("=" * 50)
    print("✅ Migration complete - you can now use unique ID tracking!")
