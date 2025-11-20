"""
Quick test script to generate samples with different configurations
"""
from generate_hadith_post import HadithPostGenerator
from config import THEMES
import os

def test_with_images():
    """Test with images enabled"""
    print("🎨 Generating samples WITH images...\n")
    
    # Update config temporarily
    import config
    config.USE_IMAGES = True
    
    os.makedirs("samples_with_images", exist_ok=True)
    
    # Generate one sample from each theme with first hadith
    for theme_name in list(THEMES.keys())[:3]:  # Just 3 themes for quick test
        print(f"Creating {THEMES[theme_name]['name']} with image...")
        generator = HadithPostGenerator(theme_name)
        generator.generate_post("samples_with_images", specific_index=0)
        print()

def test_without_images():
    """Test without images (minimal)"""
    print("🎨 Generating samples WITHOUT images (minimal)...\n")
    
    # Update config temporarily
    import config
    config.USE_IMAGES = False
    
    os.makedirs("samples_minimal", exist_ok=True)
    
    # Generate one sample from each theme
    for theme_name in list(THEMES.keys())[:3]:  # Just 3 themes for quick test
        print(f"Creating {THEMES[theme_name]['name']} minimal...")
        generator = HadithPostGenerator(theme_name)
        generator.generate_post("samples_minimal", specific_index=0)
        print()

if __name__ == "__main__":
    print("=" * 60)
    print("MODERN AESTHETIC HADITH POST GENERATOR - TEST")
    print("=" * 60)
    print()
    
    # Test both versions
    test_without_images()
    print("\n" + "=" * 60 + "\n")
    test_with_images()
    
    print("\n✅ All samples generated!")
    print("📂 Check folders: samples_minimal/ and samples_with_images/")
    print("\n💡 To choose:")
    print("   - Edit config.py")
    print("   - Set USE_IMAGES = True (with images) or False (minimal)")
