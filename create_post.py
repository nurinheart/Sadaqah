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
    print(f"📚 Hadith Database: {stats['total']} Verified Sahih Hadiths")
    print(f"📖 From {len(stats['collections'])} Authentic Collections:")
    for collection, count in stats['collections'].items():
        print(f"   • {collection.title()}: {count} hadiths")
    print(f"✓ All hadiths verified as Sahih from CDN API")
    print()
    
    # Check command line arguments
    auto_post = '--post' in sys.argv or '-p' in sys.argv
    prefer_short = '--prefer-short' in sys.argv or '--short' in sys.argv
    theme = DEFAULT_THEME
    specific_index = None
    
    # Parse arguments
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ['--post', '-p']:
            pass
        elif arg in ['--prefer-short', '--short']:
            pass  # Already handled
        elif arg == '--index' and i + 1 < len(sys.argv):
            specific_index = int(sys.argv[i + 1])
            i += 1
        elif arg == '--auto-post' and i + 1 < len(sys.argv):
            auto_post = sys.argv[i + 1].lower() in ['true', 'yes', '1']
            i += 1
        elif not arg.startswith('--'):
            theme = arg
        i += 1
    
    if prefer_short:
        print(f"📊 Short mode: Preferring hadiths that fit in <=10 slides")
    
    # Generate post
    generator = HadithPostGenerator(theme)
    
    print(f"🎨 Theme: {theme}")
    print(f"🖼️  Images: {'Enabled' if USE_IMAGES else 'Disabled (Minimal)'}")
    print(f"📱 Auto-post: {'Yes' if auto_post else 'No'}")
    if specific_index is not None:
        print(f"📍 Using hadith index: {specific_index}")
    print()
    
    filenames, index, hadith = generator.generate_post(
        specific_index=specific_index,
        prefer_short=prefer_short
    )
    
    if len(filenames) == 1:
        print(f"✅ Generated: {filenames[0]}")
    else:
        print(f"✅ Generated {len(filenames)} slides:")
        for i, fname in enumerate(filenames, 1):
            print(f"   Slide {i}: {fname}")
    
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
            
            # Post as single image or carousel, with auto-story sharing
            poster.post_image(filenames, caption, hashtags, share_to_story=True)
            
            print()
            print("🎉 POSTED TO INSTAGRAM!")
            if len(filenames) > 1:
                print(f"📱 Posted as CAROUSEL with {len(filenames)} slides")
            print("📱 Auto-shared to STORY with link to post!")
            print()
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
            import traceback
            traceback.print_exc()
            print("   You can still post manually!")
    else:
        print("📱 MANUAL POSTING:")
        if len(filenames) > 1:
            print(f"   📖 This is a CAROUSEL with {len(filenames)} slides")
            print("   1. Open Instagram app")
            print("   2. Create new post → Select multiple images")
            print("   3. Select all slides in order from 'output' folder")
        else:
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
