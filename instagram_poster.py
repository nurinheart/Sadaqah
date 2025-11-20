"""
Instagram Auto-Poster
Posts generated hadith images to Instagram automatically
"""

import os
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, TwoFactorRequired, ChallengeRequired
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class InstagramPoster:
    def __init__(self):
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        self.session_file = os.getenv('SESSION_FILE', 'instagram_session.json')
        self.client = Client()
        
        # Load session if exists
        if os.path.exists(self.session_file):
            try:
                self.client.load_settings(self.session_file)
                self.client.login(self.username, self.password)
                print("✅ Logged in using saved session")
            except:
                print("⚠️  Session expired, logging in fresh...")
                self.login()
        else:
            self.login()
    
    def login(self):
        """Login to Instagram"""
        if not self.username or not self.password:
            raise ValueError("❌ Instagram credentials not set! Create .env file with your username and password")
        
        try:
            print(f"🔐 Logging in as @{self.username}...")
            self.client.login(self.username, self.password)
            
            # Save session for future use
            self.client.dump_settings(self.session_file)
            print("✅ Logged in successfully!")
            
        except TwoFactorRequired:
            code = input("Enter 2FA code: ")
            self.client.login(self.username, self.password, verification_code=code)
            self.client.dump_settings(self.session_file)
            print("✅ Logged in successfully with 2FA!")
            
        except ChallengeRequired:
            print("⚠️  Instagram security challenge required.")
            print("Please login manually via Instagram app and try again.")
            raise
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            raise
    
    def post_image(self, image_path, caption, hashtags=None):
        """Post image to Instagram"""
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"❌ Image not found: {image_path}")
        
        # Build full caption with hashtags
        full_caption = caption
        if hashtags:
            full_caption += "\n\n" + " ".join(hashtags)
        
        try:
            print(f"📤 Uploading to Instagram...")
            print(f"   Image: {image_path}")
            print(f"   Caption length: {len(full_caption)} chars")
            
            # Upload photo
            media = self.client.photo_upload(
                image_path,
                caption=full_caption
            )
            
            print(f"✅ Posted successfully!")
            print(f"   Post ID: {media.pk}")
            print(f"   Link: https://www.instagram.com/p/{media.code}/")
            
            return media
            
        except Exception as e:
            print(f"❌ Failed to post: {e}")
            raise
    
    def test_connection(self):
        """Test if logged in and working"""
        try:
            user_info = self.client.user_info_by_username(self.username)
            print(f"✅ Connected as @{user_info.username}")
            print(f"   Followers: {user_info.follower_count}")
            print(f"   Following: {user_info.following_count}")
            print(f"   Posts: {user_info.media_count}")
            return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False


def get_default_caption(hadith_text, source, category=None):
    """Generate a good default caption with hadith text"""
    caption = f'"{hadith_text}"\n\n'
    caption += f"— Prophet Muhammad ﷺ\n"
    caption += f"📖 {source} (Sahih)\n"
    caption += f"✓ Verified from 2+ authentic sources\n\n"
    
    if category:
        caption += f"#{category} "
    
    return caption


def get_default_hashtags():
    """Get default hashtags for hadith posts"""
    return [
        "#Hadith",
        "#Islam",
        "#IslamicQuotes",
        "#Muslim",
        "#ProphetMuhammad",
        "#IslamicReminders",
        "#SahihBukhari",
        "#Quran",
        "#Allah",
        "#Deen",
        "#IslamicPost",
        "#MuslimCommunity",
        "#IslamicKnowledge",
        "#Sunnah",
        "#Dawah"
    ]


if __name__ == "__main__":
    # Test the Instagram poster
    print("=" * 60)
    print("📱 INSTAGRAM AUTO-POSTER TEST")
    print("=" * 60)
    print()
    
    try:
        poster = InstagramPoster()
        poster.test_connection()
        
        print()
        print("✅ Instagram poster is ready!")
        print("💡 You can now use auto-posting in create_post.py")
        
    except Exception as e:
        print()
        print("❌ Setup incomplete. Please:")
        print("   1. Create .env file (copy from .env.example)")
        print("   2. Add your Instagram username and password")
        print("   3. Run this test again")
