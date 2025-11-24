"""
One-time migration script to convert posted_hadiths.json from index-based to unique ID format
"""
import json
from datetime import datetime
from hadith_data import get_sahih_hadiths

# Load current index-based tracking
with open('posted_hadiths.json', 'r') as f:
    posted_indices = json.load(f)

# Load hadiths with new unique IDs
hadiths = get_sahih_hadiths()

# Convert indices to unique IDs
posted_ids = []
metadata = {}

for idx in posted_indices:
    if idx < len(hadiths):
        hadith = hadiths[idx]
        base_id = hadith['base_id']
        unique_id = hadith['unique_id']
        variant = hadith['variant']
        
        # Add base_id to posted list (this marks the entire hadith including all variants)
        if base_id not in posted_ids:
            posted_ids.append(base_id)
        
        # Store metadata
        metadata[base_id] = {
            'posted_date': datetime.now().strftime('%Y-%m-%d'),
            'variant': variant,
            'unique_id': unique_id,
            'reference': hadith['reference']
        }

# Create new structure
new_structure = {
    'posted_ids': posted_ids,
    'metadata': metadata,
    'migration_info': {
        'migrated_at': datetime.now().isoformat(),
        'original_indices': posted_indices,
        'note': 'Migrated from index-based to unique ID tracking system'
    }
}

# Write new structure
with open('posted_hadiths.json', 'w') as f:
    json.dump(new_structure, f, indent=2, ensure_ascii=False)

print(f"✅ Migration complete!")
print(f"   Converted {len(posted_indices)} indices -> {len(posted_ids)} unique IDs")
print(f"   Structure: {list(new_structure.keys())}")
print(f"   Sample IDs: {posted_ids[:5]}")
# Migration complete - archived
