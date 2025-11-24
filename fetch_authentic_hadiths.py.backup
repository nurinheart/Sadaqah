#!/usr/bin/env python3
"""
Fetch and verify authentic Sahih hadiths from CDN API.
Creates a database of verified hadiths ready for Instagram posting.

This script:
1. Fetches hadiths from free CDN-hosted authentic sources
2. Verifies each hadith is graded Sahih (authentic)
3. Ensures NO summarization or modification (raw text only)
4. Balances across all 6 major hadith books
5. Saves to verified_hadiths.json for use by generate_hadith_post.py
"""

import json
from datetime import datetime
from hadith_api import HadithAPIClient, create_verified_hadith_database


def save_hadith_database(hadiths: list, filename: str = "verified_hadiths.json"):
    """
    Save verified hadiths to JSON file with metadata.
    """
    database = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "total_hadiths": len(hadiths),
            "source": "cdn.jsdelivr.net/gh/fawazahmed0/hadith-api",
            "verification": "All hadiths verified as Sahih (authentic)",
            "modification": "NO summarization or modification - raw authentic text",
            "collections": list(set(h['collection'] for h in hadiths))
        },
        "hadiths": hadiths
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Saved {len(hadiths)} hadiths to {filename}")


def load_hadith_database(filename: str = "verified_hadiths.json") -> list:
    """
    Load verified hadiths from JSON file.
    Returns empty list if file doesn't exist.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('hadiths', [])
    except FileNotFoundError:
        return []


def get_next_hadith(exclude_references: list = None) -> dict:
    """
    Get next hadith from verified database.
    Excludes already posted hadiths.
    Returns None if database needs refresh.
    """
    hadiths = load_hadith_database()
    
    if not hadiths:
        print("⚠️  No hadiths in database. Run fetch_authentic_hadiths.py first.")
        return None
    
    exclude_references = exclude_references or []
    
    # Filter out already posted hadiths
    available = [h for h in hadiths if h['reference'] not in exclude_references]
    
    if not available:
        print("⚠️  All hadiths have been posted. Consider expanding database.")
        return None
    
    # Return first available (database already curated in balanced order)
    return available[0]


def refresh_database():
    """
    Refresh the verified hadith database by fetching from API.
    """
    print("🔄 REFRESHING HADITH DATABASE FROM CDN\n")
    
    hadiths = create_verified_hadith_database()
    
    if hadiths:
        save_hadith_database(hadiths)
        print(f"\n✅ Database refreshed with {len(hadiths)} verified Sahih hadiths")
        return True
    else:
        print("\n❌ Failed to refresh database")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--refresh":
        # Force refresh from API
        refresh_database()
    else:
        # Check if database exists
        hadiths = load_hadith_database()
        
        if not hadiths:
            print("📥 No database found. Creating new one...\n")
            refresh_database()
        else:
            print(f"✅ Database already exists with {len(hadiths)} hadiths")
            print("\nTo refresh from API, run:")
            print("  python3 fetch_authentic_hadiths.py --refresh")
            
            # Show sample
            print("\n📖 Sample Hadith:")
            sample = hadiths[0]
            print(f"  Reference: {sample['reference']}")
            print(f"  Category: {sample.get('category', 'N/A')}")
            print(f"  Grade: {sample.get('grade', 'Unknown')}")
            print(f"  Length: {len(sample['text'])} characters")
            print(f"  Text: {sample['text'][:150]}...")
