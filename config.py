import os

# Configuration for Daily Hadith Post Generator

# Instagram post dimensions (4:5 ratio)
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1350

# Theme configurations
THEMES = {
    "warm_beige": {
        "name": "Warm Beige",
        "bg_colors": ["#F5E6D3", "#E8D4B8"],  # Gradient: warm beige to light tan
        "text_color": "#2C2416",  # Dark brown - main hadith
        "heading_color": "#C17817",  # Gold/amber - "The Prophet said"
        "source_color": "#8B4513",  # Saddle brown - reference (distinct)
    },
    "sage_green": {
        "name": "Sage Green",
        "bg_colors": ["#E8F3E8", "#D4E7D4"],  # Gradient: light sage to soft green
        "text_color": "#1B3A1B",  # Very dark green - main hadith
        "heading_color": "#2E7D32",  # Medium green - heading
        "source_color": "#D84315",  # Deep orange - reference (pops!)
    },
    "soft_cream": {
        "name": "Soft Cream",
        "bg_colors": ["#FFF8E7", "#F5E9D3"],  # Gradient: cream to light beige
        "text_color": "#1A1A1A",  # Almost black - main hadith
        "heading_color": "#8B4513",  # Saddle brown - heading
        "source_color": "#C17817",  # Gold - reference
    },
    "muted_blue": {
        "name": "Muted Blue",
        "bg_colors": ["#E3F2FD", "#BBDEFB"],  # Gradient: pale blue to light blue
        "text_color": "#0D47A1",  # Navy blue - main hadith
        "heading_color": "#1976D2",  # Bright blue - heading
        "source_color": "#E65100",  # Deep orange - reference (contrast!)
    },
    "desert_sand": {
        "name": "Desert Sand",
        "bg_colors": ["#FAF3E0", "#E8D7C3"],  # Gradient: sand to light tan
        "text_color": "#3E2723",  # Deep brown - main hadith
        "heading_color": "#BF360C",  # Deep orange - heading (pops!)
        "source_color": "#6D4C41",  # Medium brown - reference
    },
    "olive_tone": {
        "name": "Olive Tone",
        "bg_colors": ["#F1F3E8", "#E0E5D3"],  # Gradient: pale olive to light olive
        "text_color": "#1B5E20",  # Dark green - main hadith
        "heading_color": "#827717",  # Olive gold - heading
        "source_color": "#D84315",  # Deep orange - reference (contrast!)
    }
}

# Default theme (you can change this after reviewing samples)
DEFAULT_THEME = "warm_beige"

# Font settings
FONTS = {
    "heading": {
        "size": 46,  # Bigger for "The Prophet ﷺ said:"
        "family": "Product Sans"
    },
    "symbol": {
        "size": 60,  # Much bigger for ﷺ symbol
        "family": "Arabic"  # Special Arabic font for symbol
    },
    "main_text": {
        "size": 54,  # Slightly bigger
        "family": "Product Sans"
    },
    "source": {
        "size": 40,  # Bigger and bold like heading
        "family": "Product Sans"
    }
}

# Font file paths (download Product Sans if needed)
FONT_PATHS = {
    "product_sans_regular": "fonts/ProductSans-Regular.ttf",
    "product_sans_bold": "fonts/ProductSans-Bold.ttf",
}

# System fonts that support Arabic/Islamic symbols
ARABIC_FONTS = [
    # Linux/Ubuntu fonts (GitHub Actions)
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    # macOS fonts
    "/System/Library/Fonts/Supplemental/GeezaPro.ttc",
    "/System/Library/Fonts/Supplemental/Baghdad.ttf",
    "/System/Library/Fonts/Supplemental/KufiStandardGK.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "Arial Unicode MS.ttf",
]

# Layout settings - OPTIMIZED for Instagram 10-slide limit
PADDING = 60  # Reduced padding to fit more text per slide (was 90)
LINE_SPACING = 1.5  # Optimized line spacing (was 1.6)
MAX_TEXT_WIDTH = IMAGE_WIDTH - (PADDING * 2)

# Aesthetic enhancements
HEADING_LETTER_SPACING = 2  # Add letter spacing for modern look
SOURCE_LETTER_SPACING = 1
TEXT_SHADOW = False  # Set to True for subtle shadow effect

# Branding (optional watermark)
WATERMARK = "@NectarFromProphet"  # Change to your account name or leave empty
WATERMARK_SIZE = 28
WATERMARK_OPACITY = 100  # 0-255, lower is more subtle

# Image settings - LOCAL IMAGES ONLY (no timeouts, guaranteed halal)
USE_IMAGES = True  # Enabled with local nature images
IMAGE_HEIGHT_RATIO = 0.30  # Image takes 25% of top height
IMAGE_OPACITY = 0.95  # Higher opacity to make images clearly visible

# Local image paths - stored in repository (nature/Islamic patterns only)
# ROOT FIX: No external downloads = no timeouts, no inappropriate content
LOCAL_IMAGES = {
    "Intention": "images/nature/mountains_sunrise.jpg",
    "Character": "images/nature/mountain_lake.jpg",
    "Brotherhood": "images/nature/forest_path.jpg",
    "Speech": "images/nature/sunset_sky.jpg",
    "Worship": "images/nature/night_stars.jpg",
    "Teaching": "images/patterns/geometric_gold.jpg",
    "Charity": "images/nature/light_rays.jpg",
    "Kindness": "images/nature/flowers_field.jpg",
    "Patience": "images/nature/calm_water.jpg",
    "Helping Others": "images/nature/clouds_sunset.jpg",
    "Knowledge": "images/patterns/islamic_pattern.jpg",  # Using pattern instead
    "Legacy": "images/nature/ancient_tree.jpg",
    "Golden Rule": "images/patterns/geometric_gold.jpg",  # Using gold pattern
    "Service": "images/nature/mountain_peak.jpg",
    "Mercy": "images/nature/peaceful_sky.jpg",
    "Parents": "images/nature/green_hills.jpg",
    "Quran": "images/patterns/geometric_gold.jpg",  # Using gold pattern
    "default": "images/nature/serene_sky.jpg"
}

# Instagram Credentials
INSTAGRAM_USERNAME = os.environ.get("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.environ.get("INSTAGRAM_PASSWORD")
INSTAGRAM_SESSION_DATA = os.environ.get("INSTAGRAM_SESSION_DATA")

# Hadith API and Data
HADITH_API_URL = "https://api.hadith.sbs/"

# Default hadith theme (can be overridden)
HADITH_THEME = "soft_cream"

# Logging configuration
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "hadith_generator.log"

# Error handling
ERROR_REPORTING_ENABLED = True
ERROR_REPORT_EMAIL = "youremail@example.com"  # Change to your email
