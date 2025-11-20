"""
Generate comparison samples to show the improvements
"""
from generate_hadith_post import HadithPostGenerator
import os

def generate_comparison_samples():
    print("🎨 GENERATING UPDATED DESIGN SAMPLES")
    print("=" * 60)
    print()
    print("✨ NEW FEATURES:")
    print("   • Proper ﷺ symbol (no more boxes!)")
    print("   • Symbol is BIGGER (60px vs 46px)")
    print("   • Bold reference (like heading)")
    print("   • Better spacing and padding")
    print("   • Enhanced aesthetic")
    print()
    print("Generating samples for all themes...")
    print()
    
    os.makedirs("updated_samples", exist_ok=True)
    
    themes = ["warm_beige", "sage_green", "soft_cream"]
    
    for theme in themes:
        print(f"Creating {theme}...")
        generator = HadithPostGenerator(theme)
        generator.generate_post("updated_samples", specific_index=0)
        print()
    
    print("=" * 60)
    print("✅ UPDATED SAMPLES GENERATED!")
    print("=" * 60)
    print()
    print("📂 CHECK THESE FOLDERS:")
    print("   • updated_samples/ - NEW design with ﷺ symbol")
    print("   • samples_minimal/ - OLD design (for comparison)")
    print()
    print("🎯 IMPROVEMENTS YOU'LL SEE:")
    print("   1. ﷺ symbol displays correctly (BIGGER!)")
    print("   2. Reference is bold (same weight as heading)")
    print("   3. Better spacing (more breathing room)")
    print("   4. Cleaner layout (larger padding)")
    print("   5. Enhanced visual hierarchy")
    print()
    print("💡 The difference is dramatic! Open both folders and compare.")
    print()

if __name__ == "__main__":
    generate_comparison_samples()
