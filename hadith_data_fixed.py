"""
Hadith database loader - FIXED VERSION
✅ Handles duplicate hadiths during refresh
✅ Works with unique ID tracking system
✅ Never adds already-posted hadiths
"""

import json
from typing import List, Dict
from pathlib import Path

DATABASE_FILE = Path(__file__).parent / "verified_hadiths.json"

def load_verified_hadiths() -> List[Dict]:
    """Load verified hadiths from JSON file"""
    if not DATABASE_FILE.exists():
        print(f"⚠️  WARNING: {DATABASE_FILE} not found!")
        print("   Run: python3 fetch_authentic_hadiths.py --refresh")
        return []
    
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            hadiths = data.get('hadiths', [])
            print(f"✅ Loaded {len(hadiths)} verified Sahih hadiths")
            return hadiths
    except Exception as e:
        print(f"❌ Error loading hadith database: {e}")
        return []

def get_sahih_hadiths() -> List[Dict]:
    """Get all Sahih hadiths with enhanced metadata"""
    hadiths = load_verified_hadiths()
    transformed = []
    
    for h in hadiths:
        transformed_hadith = {
            'text': h['text'],
            'primary_source': h['reference'],
            'verification_source': f"{h['source']} verified",
            'grade': 'Sahih',
            'book': h['reference'].split(' ')[0] + ' ' + h['reference'].split(' ')[1],
            'category': h.get('category', 'General'),
            'reference': h['reference'],
            'chapter': h.get('chapter', ''),
            'narrator': h.get('narrator', ''),
            'source': h.get('source', ''),
            'collection': h.get('collection', ''),
            'hadith_number': h.get('hadith_number', 0),
            # Add unique identifier for tracking
            'unique_id': f"{h.get('collection', 'unknown')}_{h.get('hadith_number', 0)}"
        }
        transformed.append(transformed_hadith)
    
    return transformed

def get_hadith_stats() -> Dict:
    """Get statistics about the hadith database"""
    hadiths = load_verified_hadiths()
    if not hadiths:
        return {"total": 0, "collections": {}, "categories": {}}
    
    collections = {}
    categories = {}
    
    for h in hadiths:
        # Count by collection
        collection = h.get('collection', 'unknown')
        collections[collection] = collections.get(collection, 0) + 1
        
        # Count by category
        category = h.get('category', 'General')
        categories[category] = categories.get(category, 0) + 1
    
    return {
        "total": len(hadiths),
        "collections": collections,
        "categories": categories
    }

def add_hadiths_safely(new_hadiths: List[Dict], posted_hadith_ids: List[str] = None) -> List[Dict]:
    """
    Add new hadiths to database, skipping duplicates and already-posted ones.
    
    Args:
        new_hadiths: List of new hadith dictionaries
        posted_hadith_ids: List of already-posted unique IDs to skip
        
    Returns:
        List of hadiths that were actually added
    """
    if posted_hadith_ids is None:
        posted_hadith_ids = []
    
    existing_hadiths = load_verified_hadiths()
    existing_ids = {f"{h.get('collection', 'unknown')}_{h.get('hadith_number', 0)}" 
                   for h in existing_hadiths}
    
    added_hadiths = []
    
    for new_hadith in new_hadiths:
        unique_id = f"{new_hadith.get('collection', 'unknown')}_{new_hadith.get('hadith_number', 0)}"
        
        # Skip if already exists in database
        if unique_id in existing_ids:
            print(f"⏭️  Skipping {new_hadith.get('reference', 'Unknown')} - already in database")
            continue
            
        # Skip if already posted (lifetime tracking)
        if unique_id in posted_hadith_ids:
            print(f"⏭️  Skipping {new_hadith.get('reference', 'Unknown')} - already posted")
            continue
            
        # Add to database
        existing_hadiths.append(new_hadith)
        existing_ids.add(unique_id)
        added_hadiths.append(new_hadith)
        print(f"➕ Added: {new_hadith.get('reference', 'Unknown')} (ID: {unique_id})")
    
    # Save updated database
    if added_hadiths:
        database = {
            "metadata": {
                "created_at": json.loads(open(DATABASE_FILE, 'r').read()).get('metadata', {}).get('created_at', ''),
                "total_hadiths": len(existing_hadiths),
                "source": "cdn.jsdelivr.net/gh/fawazahmed0/hadith-api + updates",
                "verification": "All hadiths verified as Sahih (authentic)",
                "modification": "NO summarization or modification - raw authentic text",
                "collections": list(set(h['collection'] for h in existing_hadiths if 'collection' in h))
            },
            "hadiths": existing_hadiths
        }
        
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump(database, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Database updated: {len(added_hadiths)} new hadiths added")
    
    return added_hadiths

if __name__ == "__main__":
    # Test the functions
    hadiths = get_sahih_hadiths()
    print(f"✅ Total hadiths: {len(hadiths)}")
    
    if hadiths:
        sample = hadiths[0]
        print(f"✅ Sample hadith ID: {sample.get('unique_id', 'N/A')}")
        print(f"✅ Sample reference: {sample.get('reference', 'N/A')}")
    
    stats = get_hadith_stats()
    print(f"✅ Stats: {stats}")
