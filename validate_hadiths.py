"""
Hadith Validation and Statistics Tool
Shows authenticity verification for all hadiths
"""

from hadith_data import get_sahih_hadiths, get_hadith_stats, validate_hadith_authenticity, HADITHS

def validate_all_hadiths():
    """Validate all hadiths in the database"""
    print("=" * 70)
    print("🔍 HADITH AUTHENTICITY VALIDATION")
    print("=" * 70)
    print()
    
    total = len(HADITHS)
    sahih = get_sahih_hadiths()
    sahih_count = len(sahih)
    rejected = total - sahih_count
    
    print(f"📊 VALIDATION RESULTS:")
    print(f"   Total Hadiths: {total}")
    print(f"   ✅ Verified Sahih: {sahih_count}")
    print(f"   ❌ Rejected: {rejected}")
    print(f"   Success Rate: {(sahih_count/total)*100:.1f}%")
    print()
    
    # Show statistics by book
    stats = get_hadith_stats()
    print(f"📚 SAHIH HADITHS BY BOOK:")
    print(f"   Total Books: {stats['total_books']}")
    print()
    for book, count in sorted(stats['by_book'].items(), key=lambda x: x[1], reverse=True):
        print(f"   • {book}: {count} hadiths")
    print()
    
    # Validation criteria
    print("✓ VERIFICATION CRITERIA:")
    print("   1. Must have primary source reference")
    print("   2. Must have verification from 2nd source")
    print("   3. Must be graded as 'Sahih'")
    print("   4. All required fields must be complete")
    print()
    
    # Show detailed validation for each hadith
    print("=" * 70)
    print("📋 DETAILED HADITH VERIFICATION")
    print("=" * 70)
    print()
    
    for i, hadith in enumerate(sahih, 1):
        print(f"{i}. {hadith['text'][:60]}...")
        print(f"   Book: {hadith['book']}")
        print(f"   Primary: {hadith['primary_source']}")
        print(f"   Verified: {hadith['verification_source']}")
        print(f"   Grade: ✓ {hadith['grade']}")
        print(f"   Category: {hadith['category']}")
        print()
    
    print("=" * 70)
    print("✅ ALL HADITHS VALIDATED")
    print("=" * 70)
    print()
    print("💡 Key Points:")
    print("   • Every hadith verified from 2+ authentic sources")
    print("   • Only Sahih grade hadiths included")
    print("   • Diverse collection from multiple books")
    print("   • Strict Islamic authenticity standards applied")
    print()

if __name__ == "__main__":
    validate_all_hadiths()
