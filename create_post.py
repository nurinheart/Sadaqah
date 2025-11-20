"""
Easy-to-use script for generating daily hadith posts
"""
from generate_hadith_post import HadithPostGenerator
from config import DEFAULT_THEME, USE_IMAGES
from hadith_data import get_sahih_hadiths, get_hadith_stats
import sys
import os

def main():
    print("=" * 60)
    print("📿 DAILY HADITH POST GENERATOR")
    print("=" * 60)
    print()
    
    # Show hadith statistics
    stats = get_hadith_stats()
    print(f"📚 Hadith Database: {stats['total_sahih']} Verified Sahih Hadiths")
    print(f"📖 From {stats['total_books']} Authentic Books:")
    for book, count in stats['by_book'].items():
        print(f"   • {book}: {count} hadiths")
    print(f"✓ All hadiths verified from 2+ sources")
    print()
    
    # Check command line arguments
    auto_post = '--post' in sys.argv or '-p' in sys.argv
    theme = DEFAULT_THEME
    
    for arg in sys.argv[1:]:
        if arg not in ['--post', '-p']:
            theme = arg
    
    # Generate post
    generator = HadithPostGenerator(theme)
    
    print(f"🎨 Theme: {theme}")
    print(f"🖼️  Images: {'Enabled' if USE_IMAGES else 'Disabled (Minimal)'}")
    print(f"📱 Auto-post: {'Yes' if auto_post else 'No'}")
    print()
    
    filename, index, hadith = generator.generate_post()
    
    print(f"✅ Generated: {filename}")
    print(f"📖 Hadith {index + 1}/{len(generator.hadiths)}")
    print(f"📚 Book: {hadith['book']}")
    print(f"✓ Grade: {hadith['grade']} (Verified)")
    print(f"🎨 Theme: {generator.theme['name']}")
    print(f"📝 Text: {hadith['text'][:50]}...")
    print()
    print("=" * 60)
    print("✅ POST GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    
    # Auto-post to Instagram if requested
    if auto_post:
        try:
            from instagram_poster import InstagramPoster, get_default_caption, get_default_hashtags
            
            print("📱 AUTO-POSTING TO INSTAGRAM...")
            print()
            
            poster = InstagramPoster()
            caption = get_default_caption(
                hadith['text'], 
                hadith['primary_source'],
                hadith.get('category')
            )
            hashtags = get_default_hashtags()
            
            poster.post_image(filename, caption, hashtags)
            
            print()
            print("🎉 POSTED TO INSTAGRAM!")
            print("⚠️  IMPORTANT: Add Quran audio manually:")
            print("   1. Open Instagram app")
            print("   2. Find your post")
            print("   3. Edit → Add Music → Search 'Quran'")
            print("   4. Select Surah Ar-Rahman or another")
            print("   5. Save!")
            
        except ImportError:
            print("⚠️  Instagram auto-posting not set up yet.")
            print("   Run: pip install instagrapi")
            print("   Then create .env file with credentials")
        except Exception as e:
            print(f"❌ Auto-posting failed: {e}")
            print("   You can still post manually!")
    else:
        print("📱 MANUAL POSTING:")
        print("   1. Open the image from 'output' folder")
        print("   2. Upload to Instagram")
        print("   3. Add Quran recitation from Instagram music library")
        print("   4. Add hashtags (see suggestions below)")
        print("   5. Post! 🚀")
        print()
        print("💡 TIP: Use --post flag for auto-posting")
        print("   python3 create_post.py --post")
    
    print()
    print("💡 SUGGESTED HASHTAGS:")
    print("   #Hadith #Islam #IslamicQuotes #Muslim #ProphetMuhammad")
    print("   #IslamicReminders #SahihBukhari #Quran #Allah #Deen")
    print("   #IslamicPost #MuslimCommunity #IslamicKnowledge")
    print()
    print("🎵 SUGGESTED QURAN TRACKS:")
    print("   - Surah Ar-Rahman (Most popular)")
    print("   - Surah Al-Mulk")
    print("   - Surah Ya-Sin")
    print()

if __name__ == "__main__":
    main()
