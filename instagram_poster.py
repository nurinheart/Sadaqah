"""
Instagram Auto-Poster with Carousel and Story Support
Posts generated hadith images to Instagram automatically
✅ Carousel support for multi-slide posts
✅ Auto-story posting with link to feed post
✅ Exact implementation from NectarFromQuran
"""

import os
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, TwoFactorRequired, ChallengeRequired
from instagrapi.types import StoryLink
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
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
        session_data = os.getenv('INSTAGRAM_SESSION_DATA')
        
        if session_data:
            try:
                print("🔐 Attempting to log in using session data...")
                session_dict = json.loads(session_data)
                self.client.set_settings(session_dict)
                self.client.login_by_sessionid(self.client.sessionid)
                print("✅ Logged in successfully using session data.")
                return
            except Exception as e:
                print(f"⚠️  Session login failed: {e}")
                print("   Please generate a new session.json and update the INSTAGRAM_SESSION_DATA secret.")
                raise
        
        if not self.username or not self.password:
            raise ValueError("❌ Instagram credentials not set! Please set INSTAGRAM_SESSION_DATA secret.")
        
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
    
    def post_image(self, image_paths, caption, hashtags=None, share_to_story=True):
        """
        Post image(s) to Instagram as single post or carousel
        Automatically shares to story with link if share_to_story=True
        
        Args:
            image_paths: Single path or list of paths for carousel
            caption: Post caption
            hashtags: Optional hashtags list
            share_to_story: Whether to auto-share to story with link
        
        Returns:
            media object with .code attribute for URL
        """
        # Handle both single image and list
        if isinstance(image_paths, str):
            image_paths = [image_paths]
        
        # Verify all files exist
        for path in image_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"❌ Image not found: {path}")
        
        # Build full caption with hashtags
        full_caption = caption
        if hashtags:
            full_caption += "\n\n" + " ".join(hashtags)
        
        try:
            # Single image or carousel?
            if len(image_paths) == 1:
                print(f"📤 Uploading single image to Instagram...")
                print(f"   Image: {image_paths[0]}")
                print(f"   Caption length: {len(full_caption)} chars")
                
                media = self.client.photo_upload(
                    image_paths[0],
                    caption=full_caption
                )
            else:
                print(f"📤 Uploading carousel with {len(image_paths)} slides...")
                media = self.post_carousel(image_paths, full_caption)
            
            print(f"✅ Posted successfully!")
            print(f"   Post ID: {media.pk}")
            print(f"   Post Code: {media.code}")
            post_url = f"https://www.instagram.com/p/{media.code}/"
            print(f"   Link: {post_url}")
            
            # Auto-share to story with link
            if share_to_story:
                print(f"\n📱 Sharing to story with link...")
                self.share_to_story(image_paths[0], post_url)
            
            return media
            
        except Exception as e:
            print(f"❌ Failed to post: {e}")
            raise
    
    def post_carousel(self, image_paths, caption):
        """Post multiple images as carousel"""
        try:
            # Convert to Path objects
            paths = [Path(img) for img in image_paths]
            
            # Instagram carousels only support JPG - convert PNG to JPG
            jpg_paths = []
            for path in paths:
                if path.suffix.lower() == '.png':
                    jpg_path = path.with_suffix('.jpg')
                    # Convert PNG to JPG
                    img = Image.open(path)
                    # Convert RGBA to RGB (remove alpha channel)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = rgb_img
                    img.save(jpg_path, 'JPEG', quality=95)
                    jpg_paths.append(jpg_path)
                else:
                    jpg_paths.append(path)
            
            print(f"📤 Uploading carousel with {len(jpg_paths)} slides...")
            
            # Upload as album/carousel
            media = self.client.album_upload(
                paths=jpg_paths,
                caption=caption
            )
            
            print(f"✅ Carousel posted successfully!")
            print(f"🔗 Media Code: {media.code}")
            
            # Cleanup temporary JPG files
            for orig_path, jpg_path in zip(paths, jpg_paths):
                if orig_path != jpg_path and jpg_path.exists():
                    jpg_path.unlink()
            
            return media
            
        except Exception as e:
            print(f"❌ Carousel post failed: {e}")
            import traceback
            traceback.print_exc()
            
            # Cleanup temporary JPG files on error
            try:
                for orig_path, jpg_path in zip(paths, jpg_paths):
                    if orig_path != jpg_path and jpg_path.exists():
                        jpg_path.unlink()
            except:
                pass
            
            raise
    
    def share_to_story(self, image_path, post_url=None):
        """
        Share an image to Instagram Story
        Optionally add a link sticker to the feed post
        Exact implementation from NectarFromQuran
        
        Args:
            image_path: Path to image for story background
            post_url: URL to feed post (adds link sticker if provided)
        
        Returns:
            Story media pk or None if failed
        """
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                print(f"❌ Story image not found: {image_path}")
                return None
            
            # Create proper story canvas (1080x1920 for Instagram stories)
            carousel_img = Image.open(image_path)
            
            story_width = 1080
            story_height = 1920
            story_img = Image.new('RGB', (story_width, story_height), color=(0, 0, 0))
            
            # Center the carousel image vertically on story canvas
            y_offset = (story_height - carousel_img.height) // 2
            story_img.paste(carousel_img, (0, y_offset))
            
            # Add "Tap to view full post →" text at bottom
            draw = ImageDraw.Draw(story_img)
            
            try:
                # Try system fonts
                font_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 100)
                font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 75)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Main text
            main_text = "New Post"
            sub_text = "Tap to view"
            
            # Get text dimensions
            bbox_main = draw.textbbox((0, 0), main_text, font=font_large)
            main_width = bbox_main[2] - bbox_main[0]
            main_height = bbox_main[3] - bbox_main[1]
            
            bbox_sub = draw.textbbox((0, 0), sub_text, font=font_small)
            sub_width = bbox_sub[2] - bbox_sub[0]
            sub_height = bbox_sub[3] - bbox_sub[1]
            
            # Position at bottom
            main_x = (story_width - main_width) // 2
            main_y = story_height - main_height - sub_height - 120
            
            sub_x = (story_width - sub_width) // 2
            sub_y = main_y + main_height + 20
            
            # Draw text with outline for visibility
            outline_color = (0, 0, 0)
            text_color = (255, 255, 255)
            
            # Draw main text with outline
            for adj_x in range(-3, 4):
                for adj_y in range(-3, 4):
                    draw.text((main_x + adj_x, main_y + adj_y), main_text, 
                             font=font_large, fill=outline_color)
            draw.text((main_x, main_y), main_text, font=font_large, fill=text_color)
            
            # Draw sub text with outline
            for adj_x in range(-2, 3):
                for adj_y in range(-2, 3):
                    draw.text((sub_x + adj_x, sub_y + adj_y), sub_text, 
                             font=font_small, fill=outline_color)
            draw.text((sub_x, sub_y), sub_text, font=font_small, fill=(200, 200, 200))
            
            # Save story image
            story_path = str(image_path).replace('.png', '_story.png')
            story_img.save(story_path)
            
            print(f"📤 Uploading to story (1080x1920)...")
            
            # Upload to story with link
            if post_url:
                link = StoryLink(webUri=post_url)
                media = self.client.photo_upload_to_story(
                    path=story_path,
                    links=[link]
                )
            else:
                media = self.client.photo_upload_to_story(path=story_path)
            
            print(f"✅ Story posted successfully!")
            print(f"🔗 Story PK: {media.pk}")
            
            # Cleanup temp file
            if os.path.exists(story_path):
                os.remove(story_path)
            
            return media.pk
            
        except Exception as e:
            print(f"❌ Story post failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
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
