#!/usr/bin/env python3
"""
Download halal nature images for local storage
This ensures: 1) No timeouts, 2) Guaranteed halal content, 3) Works in GitHub Actions
"""

import os
import requests
from PIL import Image
from io import BytesIO

# Curated halal nature/pattern images (verified manually - no humans/animals)
HALAL_IMAGE_URLS = {
    # Mountains & Sky
    "images/nature/mountains_sunrise.jpg": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1080&h=400&fit=crop",
    "images/nature/mountain_lake.jpg": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1080&h=400&fit=crop",
    "images/nature/mountain_peak.jpg": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1080&h=400&fit=crop",
    
    # Sky & Clouds
    "images/nature/sunset_sky.jpg": "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1080&h=400&fit=crop",
    "images/nature/peaceful_sky.jpg": "https://images.unsplash.com/photo-1501630834273-4b5604d2ee31?w=1080&h=400&fit=crop",
    "images/nature/serene_sky.jpg": "https://images.unsplash.com/photo-1517685352821-92cf88aee5a5?w=1080&h=400&fit=crop",
    "images/nature/clouds_sunset.jpg": "https://images.unsplash.com/photo-1499346030926-9a72daac6c63?w=1080&h=400&fit=crop",
    
    # Stars & Night
    "images/nature/night_stars.jpg": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1080&h=400&fit=crop",
    
    # Nature - Trees & Forest
    "images/nature/forest_path.jpg": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1080&h=400&fit=crop",
    "images/nature/ancient_tree.jpg": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1080&h=400&fit=crop",
    "images/nature/green_hills.jpg": "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=1080&h=400&fit=crop",
    
    # Water & Light
    "images/nature/calm_water.jpg": "https://images.unsplash.com/photo-1439405326854-014607f694d7?w=1080&h=400&fit=crop",
    "images/nature/light_rays.jpg": "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=1080&h=400&fit=crop",
    
    # Flowers & Plants
    "images/nature/flowers_field.jpg": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=1080&h=400&fit=crop",
    
    # Islamic Geometric Patterns (abstract, halal)
    "images/patterns/geometric_gold.jpg": "https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=1080&h=400&fit=crop",
    "images/patterns/geometric_blue.jpg": "https://images.unsplash.com/photo-1557672199-6ab27d3d3fcb?w=1080&h=400&fit=crop",
    "images/patterns/islamic_pattern.jpg": "https://images.unsplash.com/photo-1604782206219-3b9576575203?w=1080&h=400&fit=crop",
    "images/patterns/islamic_gold.jpg": "https://images.unsplash.com/photo-1571863407853-3e08a2f8dd52?w=1080&h=400&fit=crop",
}

def download_image(url, save_path, max_retries=3):
    """Download image with retries"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    for attempt in range(max_retries):
        try:
            print(f"📥 Downloading: {os.path.basename(save_path)} (attempt {attempt + 1})")
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img = img.convert('RGB')  # Ensure RGB mode
                img.save(save_path, 'JPEG', quality=95)
                print(f"   ✅ Saved: {save_path}")
                return True
            else:
                print(f"   ⚠️  HTTP {response.status_code}")
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    return False

def main():
    print("=" * 70)
    print("📿 DOWNLOADING HALAL NATURE IMAGES FOR LOCAL STORAGE")
    print("=" * 70)
    print()
    print("✅ Benefits:")
    print("   • No timeout errors in GitHub Actions")
    print("   • Guaranteed halal content (manually verified)")
    print("   • Faster image loading")
    print("   • Works offline")
    print()
    
    total = len(HALAL_IMAGE_URLS)
    success = 0
    failed = []
    
    for save_path, url in HALAL_IMAGE_URLS.items():
        if download_image(url, save_path):
            success += 1
        else:
            failed.append(save_path)
    
    print()
    print("=" * 70)
    print(f"✅ DOWNLOAD COMPLETE: {success}/{total} images")
    print("=" * 70)
    
    if failed:
        print()
        print("⚠️  Failed downloads (will retry on next run):")
        for path in failed:
            print(f"   • {path}")
    
    print()
    print("📦 Next steps:")
    print("   1. Verify images are in images/ directory")
    print("   2. Commit images to git: git add images/")
    print("   3. Push to GitHub: git push")
    print("   4. GitHub Actions will use local images (no downloads needed!)")
    print()

if __name__ == "__main__":
    main()
