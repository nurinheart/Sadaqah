"""
Quick settings configurator
"""
import sys

def update_config(use_images=None, theme=None, watermark=None):
    """Update config.py settings"""
    
    # Read current config
    with open('config.py', 'r') as f:
        lines = f.readlines()
    
    # Update settings
    new_lines = []
    for line in lines:
        if use_images is not None and 'USE_IMAGES = ' in line and 'Set to False' in line:
            new_lines.append(f"USE_IMAGES = {use_images}  # Set to False to disable images\n")
        elif theme is not None and 'DEFAULT_THEME = ' in line:
            new_lines.append(f'DEFAULT_THEME = "{theme}"\n')
        elif watermark is not None and 'WATERMARK = ' in line and 'Change to your' in line:
            new_lines.append(f'WATERMARK = "{watermark}"  # Change to your account name or leave empty\n')
        else:
            new_lines.append(line)
    
    # Write back
    with open('config.py', 'w') as f:
        f.writelines(new_lines)

def main():
    print("⚙️  QUICK SETTINGS CONFIGURATOR")
    print("=" * 60)
    print()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 settings.py images on|off")
        print("  python3 settings.py theme <theme_name>")
        print("  python3 settings.py watermark <text>")
        print()
        print("Examples:")
        print("  python3 settings.py images off")
        print("  python3 settings.py theme sage_green")
        print("  python3 settings.py watermark my_account")
        print()
        print("Available themes:")
        print("  - warm_beige")
        print("  - sage_green")
        print("  - soft_cream")
        print("  - muted_blue")
        print("  - desert_sand")
        print("  - olive_tone")
        return
    
    setting_type = sys.argv[1].lower()
    
    if setting_type == "images":
        if len(sys.argv) < 3:
            print("❌ Please specify 'on' or 'off'")
            return
        
        value = sys.argv[2].lower()
        use_images = value == "on"
        update_config(use_images=use_images)
        print(f"✅ Images {'enabled' if use_images else 'disabled'}")
        print(f"   Mode: {'With decorative images' if use_images else 'Minimal (text only)'}")
        
    elif setting_type == "theme":
        if len(sys.argv) < 3:
            print("❌ Please specify theme name")
            return
        
        theme = sys.argv[2]
        valid_themes = ['warm_beige', 'sage_green', 'soft_cream', 'muted_blue', 'desert_sand', 'olive_tone']
        
        if theme not in valid_themes:
            print(f"❌ Invalid theme. Choose from: {', '.join(valid_themes)}")
            return
        
        update_config(theme=theme)
        print(f"✅ Theme set to: {theme}")
        
    elif setting_type == "watermark":
        if len(sys.argv) < 3:
            print("❌ Please specify watermark text")
            return
        
        watermark = sys.argv[2]
        update_config(watermark=watermark)
        print(f"✅ Watermark set to: {watermark}")
        
    else:
        print(f"❌ Unknown setting: {setting_type}")
        print("   Valid options: images, theme, watermark")
        return
    
    print()
    print("🚀 Ready! Run: python3 create_post.py")

if __name__ == "__main__":
    main()
