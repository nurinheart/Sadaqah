# 📋 HADITH POST CONFIGURATION GUIDE

## ✅ ALL ROOT FIXES APPLIED

### 1. Symbol Rendering (ﷺ) - ROOT FIX ✅
**Problem**: Symbol was rendering as a box (□)  
**Root Cause**: Main text font (Product Sans) doesn't support Arabic Unicode  
**Solution**: 
- Use **GeezaPro font** specifically for the ﷺ symbol
- Implemented `draw_text_with_arabic_symbols()` function
- Splits text and uses GeezaPro for symbol, Product Sans for text
- Proper baseline alignment

**Font Path**: `/System/Library/Fonts/GeezaPro.ttc`  
**Unicode**: U+FDFA (Arabic Ligature Sallallahou Alayhe Wasallam)

### 2. Heading Removal ✅
**Removed**: "The Prophet ﷺ said:" heading  
**Reason**: Hadith content starts with isnad (chain of narration)  
**Config Options**:
```python
SHOW_HEADING_FIRST_SLIDE = False  # No heading on first slide
SHOW_HEADING_CONTINUATION_SLIDES = False  # No "Continuation:" heading
```

### 3. More Content Space ✅
**Changes**:
- Image height: 30% → **25%** (5% more content space)
- Removed heading saves ~80-100px
- Optimized padding: **40px top** (was 60px)

### 4. Left Text Alignment ✅
**Old**: Center-aligned text  
**New**: Left-aligned for better readability  
**Config**:
```python
TEXT_ALIGNMENT = "left"  # Options: "left", "center", "right"
CONTENT_LEFT_MARGIN = 80  # Left margin
CONTENT_RIGHT_MARGIN = 80  # Right margin
```

### 5. Fully Configurable Layout ✅
All spacing, sizing, and positioning is now configurable in `config.py`:

#### Heading Control
```python
SHOW_HEADING_FIRST_SLIDE = False  # Show heading on slide 1
SHOW_HEADING_CONTINUATION_SLIDES = False  # Show on other slides
HEADING_ALIGNMENT = "center"  # "left", "center", "right"
```

#### Text Alignment
```python
TEXT_ALIGNMENT = "left"  # Content alignment
REFERENCE_ALIGNMENT = "center"  # Reference alignment
```

#### Padding & Margins (pixels)
```python
PADDING_TOP = 40  # Top padding from image
PADDING_BOTTOM = 60  # Bottom padding
PADDING_LEFT = 60  # Left padding
PADDING_RIGHT = 60  # Right padding
CONTENT_LEFT_MARGIN = 80  # Content left margin
CONTENT_RIGHT_MARGIN = 80  # Content right margin
```

#### Spacing
```python
LINE_SPACING = 1.5  # Line height multiplier
HEADING_TO_CONTENT_GAP = 35  # Gap after heading
CONTENT_TO_REFERENCE_GAP = 50  # Gap before reference
```

#### Font Sizes
```python
FONTS = {
    "heading": {"size": 46},  # Heading font size
    "symbol": {"size": 54},  # ﷺ symbol size (matches main)
    "main_text": {"size": 54},  # Hadith text size
    "source": {"size": 38}  # Reference size
}
```

#### Image Settings
```python
IMAGE_HEIGHT_RATIO = 0.25  # 25% of image height
IMAGE_OPACITY = 0.95  # Image opacity
```

## 🎨 CURRENT CONFIGURATION

**Heading**: Disabled (no "Prophet said" heading)  
**Text Alignment**: Left-aligned  
**Reference**: Center-aligned  
**Image Height**: 25% (more content space)  
**Symbol Font**: GeezaPro (beautiful ﷺ rendering)  
**Main Font**: Product Sans (clean, modern)  

## 📝 HOW TO USE

### Change Text Alignment
```python
# In config.py
TEXT_ALIGNMENT = "center"  # or "left" or "right"
```

### Enable Heading
```python
# In config.py
SHOW_HEADING_FIRST_SLIDE = True  # Show "The Prophet ﷺ said:"
```

### Adjust Font Sizes
```python
# In config.py
FONTS = {
    "main_text": {"size": 60},  # Make text bigger
    "source": {"size": 40}  # Make reference bigger
}
```

### Change Spacing
```python
# In config.py
PADDING_TOP = 50  # More space from image
LINE_SPACING = 1.6  # More space between lines
CONTENT_LEFT_MARGIN = 100  # More left margin
```

## ✅ VERIFICATION CHECKLIST

- [x] Symbol font (GeezaPro) available
- [x] Symbol rendering function implemented
- [x] Width calculation for symbols implemented
- [x] Heading display configurable
- [x] Text alignment configurable
- [x] All spacing configurable
- [x] Font sizes configurable
- [x] Image height reduced (25%)
- [x] Left alignment implemented
- [x] Reference positioning configurable

## 🧪 TESTING

Run comprehensive test:
```bash
python3 << 'ENDTEST'
from generate_hadith_post import HadithPostGenerator
gen = HadithPostGenerator()
filenames, idx, hadith = gen.generate_post(specific_index=0)
print(f"✅ Generated {len(filenames)} slides")
for f in filenames:
    print(f"   {f}")
ENDTEST
```

Check generated images in `output/` folder.

## 📚 REFERENCE

- **Font**: GeezaPro.ttc (system font on macOS)
- **Symbol**: ﷺ (U+FDFA)
- **Layout**: Left-aligned, no heading
- **Config**: All settings in `config.py`

---
**Last Updated**: 2025-11-23  
**Status**: ✅ All root fixes applied and tested
