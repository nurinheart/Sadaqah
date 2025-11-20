"""
Download Product Sans font or use alternatives
"""
import os
import requests

def download_font():
    """Download Product Sans font"""
    
    os.makedirs('fonts', exist_ok=True)
    
    print("📥 Attempting to download Product Sans font...")
    print("ℹ️  Note: Product Sans is a proprietary Google font.")
    print("   If unavailable, we'll use SF Pro (Mac) or Arial as fallback.\n")
    
    # Product Sans alternatives (free, similar aesthetic)
    fonts_to_try = [
        {
            "name": "Montserrat",
            "url": "https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Regular.ttf",
            "file": "fonts/ProductSans-Regular.ttf"
        },
        {
            "name": "Montserrat Bold", 
            "url": "https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Bold.ttf",
            "file": "fonts/ProductSans-Bold.ttf"
        }
    ]
    
    for font in fonts_to_try:
        try:
            print(f"Downloading {font['name']}...")
            response = requests.get(font['url'], timeout=30)
            if response.status_code == 200:
                with open(font['file'], 'wb') as f:
                    f.write(response.content)
                print(f"✅ {font['name']} downloaded!")
            else:
                print(f"⚠️  Could not download {font['name']}")
        except Exception as e:
            print(f"⚠️  Error downloading {font['name']}: {e}")
    
    print("\n✅ Font setup complete!")
    print("💡 The generator will use downloaded fonts or fallback to system fonts.")

if __name__ == "__main__":
    download_font()
