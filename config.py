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
        "accent_color": "#C17817",  # Vibrant orange - for highlighting religious terms (distinct!)
    },
    "sage_green": {
        "name": "Sage Green",
        "bg_colors": ["#E8F3E8", "#D4E7D4"],  # Gradient: light sage to soft green
        "text_color": "#1B3A1B",  # Very dark green - main hadith
        "heading_color": "#2E7D32",  # Medium green - heading
        "source_color": "#D84315",  # Deep orange - reference (pops!)
        "accent_color": "#C17817",  # Deep orange - for highlighting religious terms
    },
    "soft_cream": {
        "name": "Soft Cream",
        "bg_colors": ["#FFF8E7", "#F5E9D3"],  # Gradient: cream to light beige
        "text_color": "#1A1A1A",  # Almost black - main hadith
        "heading_color": "#8B4513",  # Saddle brown - heading
        "source_color": "#C17817",  # Gold - reference
        "accent_color": "#C0392B",  # Rich red - for highlighting religious terms (stands out!)
    },
    "muted_blue": {
        "name": "Muted Blue",
        "bg_colors": ["#E3F2FD", "#BBDEFB"],  # Gradient: pale blue to light blue
        "text_color": "#0D47A1",  # Navy blue - main hadith
        "heading_color": "#1976D2",  # Bright blue - heading
        "source_color": "#E65100",  # Deep orange - reference (contrast!)
        "accent_color": "#D84315",  # Deep orange - for highlighting religious terms
    },
    "desert_sand": {
        "name": "Desert Sand",
        "bg_colors": ["#FAF3E0", "#E8D7C3"],  # Gradient: sand to light tan
        "text_color": "#3E2723",  # Deep brown - main hadith
        "heading_color": "#BF360C",  # Deep orange - heading (pops!)
        "source_color": "#6D4C41",  # Medium brown - reference
        "accent_color": "#C0392B",  # Rich red - for highlighting religious terms
    },
    "olive_tone": {
        "name": "Olive Tone",
        "bg_colors": ["#F1F3E8", "#E0E5D3"],  # Gradient: pale olive to light olive
        "text_color": "#1B5E20",  # Dark green - main hadith
        "heading_color": "#827717",  # Olive gold - heading
        "source_color": "#D84315",  # Deep orange - reference (contrast!)
        "accent_color": "#E74C3C",  # Bright red-orange - for highlighting religious terms
    }
}

# Default theme (you can change this after reviewing samples)
DEFAULT_THEME = "warm_beige"

# ============================================================================
# FONT SETTINGS - Control all font sizes and styles
# ============================================================================

FONTS = {
    "heading": {
        "size": 46,  # Size for "The Prophet ﷺ said:" heading
        "family": "Product Sans"
    },
    "symbol": {
        "size": 54,  # Size for ﷺ symbol in text (matches main_text for inline use)
        "family": "GeezaPro"  # GeezaPro renders the symbol beautifully
    },
    "main_text": {
        "size": 54,  # Hadith content text size
        "family": "Product Sans"
    },
    "source": {
        "size": 38,  # Reference text size (configurable)
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

# ============================================================================
# LAYOUT SETTINGS - Full control over spacing, positioning, and alignment
# ============================================================================

# Heading display options
SHOW_HEADING_FIRST_SLIDE = True  # Show "The Prophet ﷺ said:" on first slide
SHOW_HEADING_CONTINUATION_SLIDES = True  # Show "Continuation:" on other slides

# Padding and margins (in pixels)
PADDING_TOP = 40  # Top padding from image to content
PADDING_BOTTOM = 60  # Bottom padding 
PADDING_LEFT = 60  # Left padding for content
PADDING_RIGHT = 60  # Right padding for content

# Legacy padding (for backward compatibility)
PADDING = 60  # Used for some calculations

# Content spacing
LINE_SPACING = 1.5  # Line height multiplier (1.5 = 150% of font size)
HEADING_TO_CONTENT_GAP = 35  # Gap between heading and hadith text
CONTENT_TO_REFERENCE_GAP = 50  # Gap between content and reference

# Text alignment
TEXT_ALIGNMENT = "left"  # Options: "left", "center", "right", "justify"
HEADING_ALIGNMENT = "center"  # Options: "left", "center", "right"
REFERENCE_ALIGNMENT = "center"  # Options: "left", "center", "right"

# Content area configuration
CONTENT_LEFT_MARGIN = 80  # Left margin for content (for left-aligned text)
CONTENT_RIGHT_MARGIN = 80  # Right margin for content
MAX_TEXT_WIDTH = IMAGE_WIDTH - CONTENT_LEFT_MARGIN - CONTENT_RIGHT_MARGIN

# Aesthetic enhancements
HEADING_LETTER_SPACING = 2  # Add letter spacing for modern look
SOURCE_LETTER_SPACING = 1
TEXT_SHADOW = False  # Set to True for subtle shadow effect

# ============================================================================
# TEXT HIGHLIGHTING - Emphasize religious terms in content
# ============================================================================

# Enable highlighting of religious terms (Allah, Prophet, Messenger, etc.)
HIGHLIGHT_RELIGIOUS_TERMS = True

# Terms/phrases to highlight (automatically detected in text)
# These will be displayed in the theme's accent_color (distinct from regular text)
HIGHLIGHT_TERMS = [
    "Allah",
    "Allaah",
    "Allah's",
    "Allaah's", 
    "the Prophet",
    "The Prophet",
    "Prophet",
    "Messenger",
    "Apostle",
    "Allah's Messenger",
    "Allaah's Messenger",
    "Messenger of Allah",
    "Messenger of Allaah",
    "(SAW)",
    "(S.A.W.)",
    "(PBUH)",
    "(Peace Be Upon Him)",
    "(S.a.w)"
]

# Highlight the symbol with brackets (ﷺ) in accent color
HIGHLIGHT_SYMBOL_WITH_BRACKETS = True

# Branding (optional watermark)
WATERMARK = "@NectarFromProphet"  # Change to your account name or leave empty
WATERMARK_SIZE = 28
WATERMARK_OPACITY = 100  # 0-255, lower is more subtle

# Image settings - LOCAL IMAGES ONLY (no timeouts, guaranteed halal)
USE_IMAGES = True  # Enabled with local nature images
IMAGE_HEIGHT_RATIO = 0.25  # Image takes 25% of top height (reduced from 0.30 for more content space)
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

# ===== POSTING SCHEDULE CONFIGURATION =====
# Control how many posts per day and when they should run
POSTING_SCHEDULE = {
    "posts_per_day": 2,  # Options: 1, 2, 3, 4, or 5 posts per day
    
    # Predefined time slots for different posting frequencies
    # Times are in UTC - adjust based on your audience timezone
    "time_slots": {
        1: ["12:00"],  # 1 post: midday
        2: ["06:00", "18:00"],  # 2 posts: morning & evening
        3: ["06:00", "12:00", "18:00"],  # 3 posts: morning, noon, evening
        4: ["06:00", "11:00", "15:00", "20:00"],  # 4 posts: spread throughout day
        5: ["04:00", "11:00", "14:00", "17:00", "20:00"]  # 5 posts: prayer times alignment
    },
    
    # Custom time slots (optional) - overrides predefined slots if set
    # Format: ["HH:MM", "HH:MM", ...] in UTC
    "custom_times": None,  # Set to list of times to override, e.g., ["08:30", "16:45"]
}

# 🚨 IMPORTANT: After changing posts_per_day or custom_times:
# Run: python3 update_workflow_schedule.py
# Then commit and push the updated .github/workflows/daily-posts.yml file
