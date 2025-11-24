"""
Daily Hadith Post Generator with Multi-Slide Carousel Support
Creates beautiful, consistent Instagram posts with Sahih hadiths
✅ Multi-slide carousel for long hadiths (exact structure from NectarFromQuran)
✅ Auto-story posting with link to feed post
✅ Dynamic image selection to prevent repetition
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import os
import random
from datetime import datetime
import textwrap
from config import *
from hadith_data import get_sahih_hadiths, validate_hadith_authenticity


class HadithPostGenerator:
    def __init__(self, theme_name=DEFAULT_THEME):
        self.theme = THEMES.get(theme_name, THEMES[DEFAULT_THEME])
        self.posted_file = "posted_hadiths.json"
        self.image_usage_file = "image_usage.json"
        self.hadiths = get_sahih_hadiths()  # Only use validated Sahih hadiths
        self.load_posted_hadiths()
        self.load_image_usage()
        
    def load_posted_hadiths(self):
        """Load list of already posted hadith unique IDs to avoid repeats"""
        if os.path.exists(self.posted_file):
            with open(self.posted_file, 'r') as f:
                data = json.load(f)
                
                # Handle old format (array of indices) - should not happen after migration
                if isinstance(data, list):
                    print("⚠️  WARNING: Old index-based format detected!")
                    print("   Run: python3 migrate_posted_hadiths.py")
                    self.posted_ids = set()
                    self.posted_metadata = {}
                    return
                
                # New format (dict with posted_ids and metadata)
                self.posted_ids = set(data.get('posted_ids', []))
                self.posted_metadata = data.get('metadata', {})
        else:
            self.posted_ids = set()
            self.posted_metadata = {}
    
    def load_image_usage(self):
        """Load image usage tracking to prevent repetition"""
        if os.path.exists(self.image_usage_file):
            with open(self.image_usage_file, 'r') as f:
                self.image_usage = json.load(f)
        else:
            self.image_usage = {}
    
    def save_image_usage(self):
        """Save image usage tracking"""
        with open(self.image_usage_file, 'w') as f:
            json.dump(self.image_usage, f)
    
    def save_posted_hadith(self, hadith: dict):
        """
        Save hadith as posted using its unique base_id
        
        This marks the entire hadith (including all variants) as posted
        Example: Posting Muslim:251b will mark 'muslim:251' as posted
        
        Args:
            hadith: Hadith dict with base_id, unique_id, variant, reference fields
        """
        base_id = hadith['base_id']
        
        # Add to posted IDs set
        self.posted_ids.add(base_id)
        
        # Update metadata
        self.posted_metadata[base_id] = {
            'posted_date': datetime.now().strftime('%Y-%m-%d'),
            'variant': hadith.get('variant'),
            'unique_id': hadith['unique_id'],
            'reference': hadith['reference']
        }
        
        # Save to file with new structure
        with open(self.posted_file, 'w') as f:
            json.dump({
                'posted_ids': list(self.posted_ids),
                'metadata': self.posted_metadata
            }, f, indent=2, ensure_ascii=False)
    
    def get_next_hadith(self, prefer_short=False):
        """
        Get next unposted Sahih hadith with rotation across books
        
        Uses unique base_id to track posted hadiths, ensuring lifetime tracking
        with no resets. Once a hadith is posted, it's never posted again.
        
        Args:
            prefer_short: If True, prefer hadiths that will fit in <=10 slides (Instagram limit)
        
        Returns:
            Tuple of (hadith_dict, index) or (None, None) if all posted
        """
        # Filter to unposted hadiths (check by base_id)
        available = []
        for i, hadith in enumerate(self.hadiths):
            base_id = hadith['base_id']
            if base_id not in self.posted_ids:
                available.append((i, hadith))
        
        if not available:
            print("✅ All hadiths have been posted!")
            print("   To continue, add more hadiths to verified_hadiths.json")
            print("   Run: python3 fetch_authentic_hadiths.py --refresh")
            return None, None
        
        # Get book distribution for rotation
        posted_books = {}
        for base_id in self.posted_ids:
            # Extract collection from base_id (e.g., 'bukhari:1' -> 'bukhari')
            collection = base_id.split(':')[0]
            posted_books[collection] = posted_books.get(collection, 0) + 1
        
        # If prefer_short, filter to hadiths <=800 chars (roughly 10 slides max)
        if prefer_short:
            short_available = [(i, h) for i, h in available if len(h['text']) <= 800]
            if short_available:
                available = short_available
                print(f"📊 Filtering to {len(available)} short hadiths (<=10 slides)")
        
        # Pick from least-posted book for variety
        best_choice = None
        min_count = float('inf')
        
        for idx, hadith in available:
            collection = hadith['collection']
            count = posted_books.get(collection, 0)
            if count < min_count:
                min_count = count
                best_choice = (idx, hadith)
        
        if best_choice is None:
            best_choice = available[0]
        
        index, hadith = best_choice
        
        # Double-check authenticity before posting
        if not validate_hadith_authenticity(hadith):
            print(f"⚠️  WARNING: Hadith {hadith['unique_id']} failed validation, skipping...")
            self.save_posted_hadith(hadith)
            return self.get_next_hadith(prefer_short=prefer_short)
        
        return hadith, index
    
    def create_gradient_background(self):
        """Create a smooth gradient background"""
        img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))
        draw = ImageDraw.Draw(img)
        
        # Parse colors
        color1 = self.hex_to_rgb(self.theme['bg_colors'][0])
        color2 = self.hex_to_rgb(self.theme['bg_colors'][1])
        
        # Create vertical gradient
        for y in range(IMAGE_HEIGHT):
            # Calculate interpolation factor
            factor = y / IMAGE_HEIGHT
            
            # Interpolate between colors
            r = int(color1[0] * (1 - factor) + color2[0] * factor)
            g = int(color1[1] * (1 - factor) + color2[1] * factor)
            b = int(color1[2] * (1 - factor) + color2[2] * factor)
            
            draw.line([(0, y), (IMAGE_WIDTH, y)], fill=(r, g, b))
        
        return img
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def get_font(self, font_type, size=None, bold=False):
        """
        Get font with proper Unicode support for Arabic symbols
        ROOT FIX: GeezaPro for symbols, Product Sans for text
        """
        if size is None:
            size = FONTS[font_type]['size']
        
        # Special handling for Arabic/symbol fonts ONLY for 'symbol' type
        # Special handling for Arabic/symbol fonts ONLY for 'symbol' type
        if font_type == 'symbol':
            # GeezaPro is the best font for ﷺ symbol on macOS
            # Priority order based on availability and rendering quality
            unicode_fonts = [
                '/System/Library/Fonts/GeezaPro.ttc',  # PRIMARY - Best rendering
                '/System/Library/Fonts/Supplemental/GeezaPro.ttc',
                '/System/Library/Fonts/Supplemental/Baghdad.ttc',
                '/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf',  # Linux
                '/Library/Fonts/Arial Unicode.ttf',
                '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
            ]
            
            for font_path in unicode_fonts:
                if not os.path.exists(font_path):
                    continue
                    
                try:
                    font = ImageFont.truetype(font_path, size)
                    # Verify font can render the symbol
                    bbox = font.getbbox('ﷺ')
                    if bbox[2] - bbox[0] > 0:  # Has actual width
                        font_name = os.path.basename(font_path)
                        return font
                except Exception as e:
                    continue
            
            # Fallback warning
            print("⚠️  WARNING: No suitable Arabic font found for ﷺ symbol!")
            print("   Symbol may render as box. Install GeezaPro font.")
            
        # For all other font types (heading, main_text, source), use Product Sans
        product_sans_path = FONT_PATHS['product_sans_bold'] if bold else FONT_PATHS['product_sans_regular']
        try:
            if os.path.exists(product_sans_path):
                return ImageFont.truetype(product_sans_path, size)
        except:
            pass
        
        # Fallback to clean system fonts
        font_options = [
            '/System/Library/Fonts/Supplemental/Arial.ttf',
            '/System/Library/Fonts/SFNS.ttf',  # San Francisco (macOS)
            '/System/Library/Fonts/Helvetica.ttc',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
            'Arial.ttf',
        ]
        
        for font_path in font_options:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, size)
            except:
                continue
        
        # Last resort
        return ImageFont.load_default()
    
    def draw_text_with_symbol(self, draw, x, y, text_before, symbol, text_after, font, symbol_font, color, symbol_color=None):
        """Draw text with special symbol handling for proper baseline alignment"""
        if symbol_color is None:
            symbol_color = color
        
        current_x = x
        
        # Make symbol font slightly bigger for better visibility (10% larger)
        symbol_size = int(symbol_font.size * 1.1)
        symbol_font_large = self.get_font('symbol', size=symbol_size)
        
        # Get baseline information for proper alignment
        text_bbox = font.getbbox(text_before)
        text_ascent = abs(text_bbox[1])  # Distance from baseline to top
        
        symbol_bbox = symbol_font_large.getbbox(symbol)
        symbol_ascent = abs(symbol_bbox[1])  # Distance from baseline to top
        
        # Calculate vertical offset to align baselines and raise symbol slightly
        baseline_offset = text_ascent - symbol_ascent - 10  # Raise 5px
        
        # Draw "The Prophet "
        draw.text((current_x, y), text_before, fill=color, font=font)
        current_x += text_bbox[2] - text_bbox[0] + 2  # Small spacing before symbol
        
        # Draw ﷺ symbol aligned to text baseline (slightly raised)
        draw.text((current_x, y + baseline_offset), symbol, fill=symbol_color, font=symbol_font_large)
        current_x += symbol_bbox[2] - symbol_bbox[0] + 2  # Small spacing after symbol
        
        # Draw " said:"
        draw.text((current_x, y), text_after, fill=color, font=font)
        
        # Return total width for centering
        after_bbox = font.getbbox(text_after)
        return (text_bbox[2] - text_bbox[0]) + (symbol_bbox[2] - symbol_bbox[0]) + (after_bbox[2] - after_bbox[0]) + 4
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within max width"""
        lines = []
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            words = paragraph.split()
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = font.getbbox(test_line)
                width = bbox[2] - bbox[0]
                
                if width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
        
        return lines
    
    def draw_text_with_arabic_symbols(self, draw, x, y, text, main_font, symbol_font, color):
        """
        ROOT FIX: Draw text with proper Arabic symbol (ﷺ) rendering and highlighting
        - Highlights ALL religious terms (Allah, the Prophet, Messenger, etc.) in NEW accent color
        - Highlights "(ﷺ)" including brackets in accent color
        - Uses GeezaPro font for ﷺ symbol, Product Sans for text
        - Configurable via HIGHLIGHT_RELIGIOUS_TERMS and HIGHLIGHT_TERMS in config
        """
        # Use NEW dedicated accent_color for religious terms (distinct and aesthetic!)
        accent_color = self.theme.get('accent_color', self.theme['heading_color'])
        symbol = 'ﷺ'
        
        # Check if highlighting is enabled
        if not HIGHLIGHT_RELIGIOUS_TERMS:
            # No highlighting - just render with proper symbol font
            if symbol not in text:
                draw.text((x, y), text, fill=color, font=main_font)
                return
            
            # Handle symbol without highlighting
            parts = text.split(symbol)
            current_x = x
            for i, part in enumerate(parts):
                if part:
                    draw.text((current_x, y), part, fill=color, font=main_font)
                    bbox = main_font.getbbox(part)
                    current_x += bbox[2] - bbox[0]
                
                if i < len(parts) - 1:
                    symbol_font_sized = self.get_font('symbol', size=int(main_font.size))
                    text_bbox = main_font.getbbox('A')
                    symbol_bbox = symbol_font_sized.getbbox(symbol)
                    text_ascent = abs(text_bbox[1])
                    symbol_ascent = abs(symbol_bbox[1])
                    y_offset = text_ascent - symbol_ascent
                    draw.text((current_x, y + y_offset), symbol, fill=color, font=symbol_font_sized)
                    current_x += symbol_bbox[2] - symbol_bbox[0] + 2
            return
        
        # Get highlight terms from config
        highlight_terms = HIGHLIGHT_TERMS if 'HIGHLIGHT_TERMS' in globals() else []
        
        # Separate multi-word phrases and single words
        highlight_phrases = [term for term in highlight_terms if ' ' in term]
        highlight_words = [term for term in highlight_terms if ' ' not in term]
        
        current_x = x
        remaining_text = text
        
        while remaining_text:
            # Find the earliest occurrence of any highlight phrase, word, or symbol pattern
            earliest_pos = len(remaining_text)
            found_phrase = None
            found_type = None  # 'phrase', 'word', or 'symbol'
            
            # Check for multi-word phrases FIRST (to avoid breaking them into single words)
            for phrase in highlight_phrases:
                pos = remaining_text.find(phrase)
                if pos != -1 and pos < earliest_pos:
                    earliest_pos = pos
                    found_phrase = phrase
                    found_type = 'phrase'
            
            # Check for (ﷺ) pattern - symbol with brackets
            symbol_with_brackets = f"({symbol})"
            pos = remaining_text.find(symbol_with_brackets)
            if pos != -1 and pos < earliest_pos:
                earliest_pos = pos
                found_phrase = symbol_with_brackets
                found_type = 'symbol_brackets'
            
            # Check for standalone symbol
            pos = remaining_text.find(symbol)
            if pos != -1 and pos < earliest_pos:
                earliest_pos = pos
                found_phrase = symbol
                found_type = 'symbol'
            
            # Check for single highlight words (if no phrase/symbol found earlier)
            if found_type is None or earliest_pos > 0:
                for word in highlight_words:
                    # Find word boundaries to avoid partial matches
                    pos = 0
                    while pos < len(remaining_text):
                        pos = remaining_text.find(word, pos)
                        if pos == -1:
                            break
                        
                        # Check if it's a whole word (not part of another word)
                        before_ok = pos == 0 or remaining_text[pos-1] in ' \n\t.,;:!?\'"'
                        after_ok = (pos + len(word) >= len(remaining_text) or 
                                   remaining_text[pos + len(word)] in ' \n\t.,;:!?\'"\'s')
                        
                        if before_ok and after_ok and pos < earliest_pos:
                            earliest_pos = pos
                            found_phrase = word
                            found_type = 'word'
                            break
                        pos += 1
            
            # Draw text before the highlight
            if earliest_pos > 0:
                before_text = remaining_text[:earliest_pos]
                draw.text((current_x, y), before_text, fill=color, font=main_font)
                bbox = main_font.getbbox(before_text)
                current_x += bbox[2] - bbox[0]
            
            # No more highlights found
            if earliest_pos >= len(remaining_text):
                break
            
            # Draw the highlighted phrase, word, or symbol
            if found_type in ['phrase', 'word']:
                # Highlight phrase/word in accent color with bold font
                bold_font = self.get_font('main_text', size=int(main_font.size), bold=True)
                draw.text((current_x, y), found_phrase, fill=accent_color, font=bold_font)
                bbox = bold_font.getbbox(found_phrase)
                current_x += bbox[2] - bbox[0]
                remaining_text = remaining_text[earliest_pos + len(found_phrase):]
                
            elif found_type == 'symbol_brackets':
                # Highlight (ﷺ) with brackets in accent color with bold font
                bold_font = self.get_font('main_text', size=int(main_font.size), bold=True)
                
                # Draw opening bracket in bold
                draw.text((current_x, y), "(", fill=accent_color, font=bold_font)
                bracket_bbox = bold_font.getbbox("(")
                current_x += bracket_bbox[2] - bracket_bbox[0]
                
                # Draw symbol with proper font
                symbol_font_sized = self.get_font('symbol', size=int(main_font.size))
                text_bbox = bold_font.getbbox('A')
                symbol_bbox = symbol_font_sized.getbbox(symbol)
                text_ascent = abs(text_bbox[1])
                symbol_ascent = abs(symbol_bbox[1])
                y_offset = text_ascent - symbol_ascent
                
                draw.text((current_x, y + y_offset), symbol, fill=accent_color, font=symbol_font_sized)
                current_x += symbol_bbox[2] - symbol_bbox[0]
                
                # Draw closing bracket in bold
                draw.text((current_x, y), ")", fill=accent_color, font=bold_font)
                bracket_bbox = bold_font.getbbox(")")
                current_x += bracket_bbox[2] - bracket_bbox[0] + 2
                
                remaining_text = remaining_text[earliest_pos + len(symbol_with_brackets):]
                
            elif found_type == 'symbol':
                # Draw standalone symbol with proper font in accent color
                symbol_font_sized = self.get_font('symbol', size=int(main_font.size))
                text_bbox = main_font.getbbox('A')
                symbol_bbox = symbol_font_sized.getbbox(symbol)
                text_ascent = abs(text_bbox[1])
                symbol_ascent = abs(symbol_bbox[1])
                y_offset = text_ascent - symbol_ascent
                
                draw.text((current_x, y + y_offset), symbol, fill=accent_color, font=symbol_font_sized)
                current_x += symbol_bbox[2] - symbol_bbox[0] + 2
                remaining_text = remaining_text[earliest_pos + len(symbol):]
    
    def get_text_width_with_symbols(self, text, main_font, symbol_font):
        """
        Calculate actual width of text including properly rendered symbols and highlighted phrases
        This needs to match the rendering logic in draw_text_with_arabic_symbols
        """
        symbol = 'ﷺ'
        
        # Simple approximation: calculate width treating all text with main font
        # and symbols with symbol font
        total_width = 0
        remaining = text
        
        while symbol in remaining:
            parts = remaining.split(symbol, 1)
            # Width of text before symbol
            if parts[0]:
                bbox = main_font.getbbox(parts[0])
                total_width += bbox[2] - bbox[0]
            
            # Width of symbol
            symbol_bbox = symbol_font.getbbox(symbol)
            total_width += symbol_bbox[2] - symbol_bbox[0] + 2
            
            # Continue with rest
            remaining = parts[1] if len(parts) > 1 else ""
        
        # Add remaining text
        if remaining:
            bbox = main_font.getbbox(remaining)
            total_width += bbox[2] - bbox[0]
        
        return total_width
    
    def load_local_image(self, image_path):
        """Load image from local filesystem - ROOT FIX: no timeouts, guaranteed halal"""
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                return img
            else:
                print(f"⚠️  Local image not found: {image_path}")
                return None
        except Exception as e:
            print(f"⚠️  Error loading local image: {e}")
            return None
    
    def get_all_available_images(self):
        """Get all available images from nature and patterns folders"""
        all_images = []
        
        # Scan nature folder
        nature_path = "images/nature"
        if os.path.exists(nature_path):
            for img_file in os.listdir(nature_path):
                if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    all_images.append(os.path.join(nature_path, img_file))
        
        # Scan patterns folder
        patterns_path = "images/patterns"
        if os.path.exists(patterns_path):
            for img_file in os.listdir(patterns_path):
                if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    all_images.append(os.path.join(patterns_path, img_file))
        
        return all_images
    
    def select_least_used_image(self, category):
        """Select image that has been used least recently - all real nature photos"""
        all_images = self.get_all_available_images()
        
        if not all_images:
            return LOCAL_IMAGES.get(category, LOCAL_IMAGES['default'])
        
        # Sort all images by usage count (least used first)
        sorted_images = sorted(all_images, key=lambda x: self.image_usage.get(x, 0))
        
        # Pick from the 3 least used images randomly to add variety
        candidates = sorted_images[:min(3, len(sorted_images))]
        selected = random.choice(candidates)
        
        # Update usage count
        self.image_usage[selected] = self.image_usage.get(selected, 0) + 1
        self.save_image_usage()
        
        return selected
    
    def add_image_overlay(self, base_img, category):
        """Add halal nature/pattern image from LOCAL storage (no network calls)"""
        if not USE_IMAGES:
            return base_img
        
        # Get least used image to prevent repetition
        image_path = self.select_least_used_image(category)
        
        # Load local image - NO network calls, NO timeouts, NO inappropriate content
        overlay_img = self.load_local_image(image_path)
        if not overlay_img:
            return base_img
        
        # Calculate dimensions
        overlay_height = int(IMAGE_HEIGHT * IMAGE_HEIGHT_RATIO)
        
        # Resize and crop image to fit width
        aspect_ratio = overlay_img.width / overlay_img.height
        new_width = IMAGE_WIDTH
        new_height = int(new_width / aspect_ratio)
        
        if new_height < overlay_height:
            new_height = overlay_height
            new_width = int(new_height * aspect_ratio)
        
        overlay_img = overlay_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center crop
        left = (new_width - IMAGE_WIDTH) // 2
        top = (new_height - overlay_height) // 2
        overlay_img = overlay_img.crop((left, top, left + IMAGE_WIDTH, top + overlay_height))
        
        # Apply opacity
        overlay_img = overlay_img.convert('RGBA')
        alpha = overlay_img.split()[3]
        alpha = alpha.point(lambda p: int(p * IMAGE_OPACITY))
        overlay_img.putalpha(alpha)
        
        # Create a gradient fade at bottom of image
        fade_height = 60
        for y in range(fade_height):
            alpha_value = int(255 * IMAGE_OPACITY * (1 - y / fade_height))
            for x in range(IMAGE_WIDTH):
                if y < overlay_height:
                    pixel = overlay_img.getpixel((x, overlay_height - fade_height + y))
                    overlay_img.putpixel((x, overlay_height - fade_height + y), 
                                        (pixel[0], pixel[1], pixel[2], alpha_value))
        
        # Paste onto base image
        base_img.paste(overlay_img, (0, 0), overlay_img)
        
        return base_img
    
    def generate_single_slide(self, hadith, text_chunk, slide_num, total_slides, index, output_path, is_continuation=False, selected_image_path=None):
        """Generate a single slide for multi-slide carousel"""
        # Create background
        img = self.create_gradient_background()
        
        # Add category image if enabled (use the SAME image for all slides)
        if selected_image_path:
            overlay_img = self.load_local_image(selected_image_path)
            if overlay_img:
                # Apply the same overlay logic
                overlay_height = int(IMAGE_HEIGHT * IMAGE_HEIGHT_RATIO)
                aspect_ratio = overlay_img.width / overlay_img.height
                new_width = IMAGE_WIDTH
                new_height = int(new_width / aspect_ratio)
                
                if new_height < overlay_height:
                    new_height = overlay_height
                    new_width = int(new_height * aspect_ratio)
                
                overlay_img = overlay_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Center crop
                left = (new_width - IMAGE_WIDTH) // 2
                top = (new_height - overlay_height) // 2
                overlay_img = overlay_img.crop((left, top, left + IMAGE_WIDTH, top + overlay_height))
                
                # Apply opacity
                overlay_img = overlay_img.convert('RGBA')
                alpha = overlay_img.split()[3]
                alpha = alpha.point(lambda p: int(p * IMAGE_OPACITY))
                overlay_img.putalpha(alpha)
                
                # Create gradient fade
                fade_height = 60
                for y in range(fade_height):
                    alpha_value = int(255 * IMAGE_OPACITY * (1 - y / fade_height))
                    for x in range(IMAGE_WIDTH):
                        if y < overlay_height:
                            pixel = overlay_img.getpixel((x, overlay_height - fade_height + y))
                            overlay_img.putpixel((x, overlay_height - fade_height + y), 
                                                (pixel[0], pixel[1], pixel[2], alpha_value))
                
                # Paste onto base image
                img.paste(overlay_img, (0, 0), overlay_img)
        
        draw = ImageDraw.Draw(img)
        
        # Load fonts
        heading_font = self.get_font('heading', bold=True)
        symbol_font = self.get_font('symbol')
        main_font = self.get_font('main_text')
        source_font = self.get_font('source', bold=True)
        
        # Calculate starting position - more space for content (no heading)
        if USE_IMAGES:
            y_pos = int(IMAGE_HEIGHT * IMAGE_HEIGHT_RATIO) + PADDING_TOP
        else:
            y_pos = PADDING_TOP
        
        # Optional heading display (configurable)
        if slide_num == 1 and SHOW_HEADING_FIRST_SLIDE:
            text_before = "Hadith of the Day"
            symbol = ""
            text_after = ":"
            
            if HEADING_ALIGNMENT == "center":
                temp_bbox = heading_font.getbbox(text_before + text_after)
                symbol_bbox = symbol_font.getbbox(symbol)
                total_width = (temp_bbox[2] - temp_bbox[0]) + (symbol_bbox[2] - symbol_bbox[0]) + 5
                heading_x = (IMAGE_WIDTH - total_width) // 2
            else:
                heading_x = CONTENT_LEFT_MARGIN
            
            self.draw_text_with_symbol(
                draw, heading_x, y_pos,
                text_before, symbol, text_after,
                heading_font, symbol_font,
                self.theme['heading_color'],
                self.theme['heading_color']
            )
            y_pos += max(heading_font.getbbox("A")[3], symbol_font.getbbox(symbol)[3]) + HEADING_TO_CONTENT_GAP
        elif slide_num > 1 and SHOW_HEADING_CONTINUATION_SLIDES:
            continuation_text = "Continuation:"
            cont_bbox = heading_font.getbbox(continuation_text)
            
            if HEADING_ALIGNMENT == "center":
                cont_width = cont_bbox[2] - cont_bbox[0]
                cont_x = (IMAGE_WIDTH - cont_width) // 2
            else:
                cont_x = CONTENT_LEFT_MARGIN
            
            draw.text((cont_x, y_pos), continuation_text, fill=self.theme['heading_color'], font=heading_font)
            y_pos += heading_font.getbbox("A")[3] + HEADING_TO_CONTENT_GAP
        
        # Draw hadith text chunk (add "..." at end if not the last slide)
        if slide_num < total_slides:
            text_to_display = text_chunk + "..."
        else:
            # Last slide: ensure text ends with fullstop
            text_to_display = text_chunk.rstrip()
            if not text_to_display.endswith(('.', '!', '?', '।')):
                text_to_display += "."
        
        # Wrap text with proper width
        wrapped_lines = self.wrap_text(text_to_display, main_font, MAX_TEXT_WIDTH)
        line_height = main_font.getbbox('A')[3] * LINE_SPACING
        total_text_height = len(wrapped_lines) * line_height
        
        # Calculate available vertical space for content
        content_start_y = y_pos  # Where content should start
        
        # Calculate where reference will be placed
        source_bbox = source_font.getbbox(f"{hadith['primary_source']} (Sahih)")
        reference_y = IMAGE_HEIGHT - PADDING_BOTTOM - source_bbox[3] - 10  # Add extra margin
        
        # If watermark exists, adjust reference position higher
        if WATERMARK:
            watermark_font = self.get_font('source', WATERMARK_SIZE)
            watermark_bbox = watermark_font.getbbox(WATERMARK)
            reference_y = IMAGE_HEIGHT - PADDING_BOTTOM - source_bbox[3] - watermark_bbox[3] - 25  # Space for watermark
        
        # Calculate available space and center content vertically
        available_height = reference_y - content_start_y
        vertical_offset = (available_height - total_text_height) // 2
        y_pos = content_start_y + max(0, vertical_offset)  # Ensure it's not negative
        
        # Draw each line with proper alignment and symbol handling
        for line in wrapped_lines:
            # Calculate x position based on alignment
            if TEXT_ALIGNMENT == "left":
                line_x = CONTENT_LEFT_MARGIN
            elif TEXT_ALIGNMENT == "right":
                line_width = self.get_text_width_with_symbols(line, main_font, symbol_font)
                line_x = IMAGE_WIDTH - CONTENT_RIGHT_MARGIN - line_width
            else:  # center
                line_width = self.get_text_width_with_symbols(line, main_font, symbol_font)
                line_x = (IMAGE_WIDTH - line_width) // 2
            
            # Draw with proper symbol handling
            if TEXT_SHADOW:
                shadow_offset = 2
                self.draw_text_with_arabic_symbols(
                    draw, line_x + shadow_offset, y_pos + shadow_offset, 
                    line, main_font, symbol_font, (0, 0, 0, 30)
                )
            
            self.draw_text_with_arabic_symbols(
                draw, line_x, y_pos, line, main_font, symbol_font, 
                self.theme['text_color']
            )
            
            y_pos += line_height
        
        # Draw reference (on all slides) - REMOVED verification line
        # Draw reference (on all slides)
        source_text = f"{hadith['primary_source']} (Sahih)"
        source_bbox = source_font.getbbox(source_text)
        source_width = source_bbox[2] - source_bbox[0]
        source_x = (IMAGE_WIDTH - source_width) // 2
        source_y = IMAGE_HEIGHT - PADDING - 90  # Moved up since we removed verification line
        
        # Calculate watermark position first to avoid overlap
        watermark_y = None
        watermark_height = 0
        if WATERMARK:
            watermark_font = self.get_font('source', WATERMARK_SIZE)
            watermark_bbox = watermark_font.getbbox(WATERMARK)
            watermark_height = watermark_bbox[3] - watermark_bbox[1]
            watermark_y = IMAGE_HEIGHT - PADDING_BOTTOM - watermark_height
        
        draw.text((source_x, source_y), source_text, fill=self.theme['source_color'], font=source_font)
        # Position reference ABOVE watermark with proper spacing
        if WATERMARK:
            source_y = watermark_y - source_bbox[3] - 20  # 20px gap between reference and watermark
        else:
            source_y = IMAGE_HEIGHT - PADDING_BOTTOM - source_bbox[3] - 10
        
        # Position based on alignment setting
        if REFERENCE_ALIGNMENT == "left":
            source_x = CONTENT_LEFT_MARGIN
        elif REFERENCE_ALIGNMENT == "right":
            source_x = IMAGE_WIDTH - CONTENT_RIGHT_MARGIN - source_width
        else:  # center
            source_x = (IMAGE_WIDTH - source_width) // 2
        
        draw.text((source_x, source_y), source_text, fill=self.theme['source_color'], font=source_font)
        
        # Watermark (draw AFTER reference)
        if WATERMARK:
            watermark_font = self.get_font('source', WATERMARK_SIZE)
            watermark_bbox = watermark_font.getbbox(WATERMARK)
            watermark_width = watermark_bbox[2] - watermark_bbox[0]
            watermark_x = (IMAGE_WIDTH - watermark_width) // 2
            
            watermark_color = self.hex_to_rgb(self.theme['source_color'])
            watermark_color = (*watermark_color[:3], WATERMARK_OPACITY)
            
            draw.text((watermark_x, watermark_y), WATERMARK, fill=watermark_color, font=watermark_font)
        
        # Add swipe indicator (except on last slide) - ADD AFTER WATERMARK
        if slide_num < total_slides:
            swipe_indicator = self.create_swipe_indicator(slide_num, total_slides)
            img = img.convert('RGBA')
            img.alpha_composite(swipe_indicator, (0, IMAGE_HEIGHT - PADDING - 20))
            img = img.convert('RGB')
        
        # Save slide
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_path}/hadith_{index}_{timestamp}_slide{slide_num}.png"
        img.save(filename, quality=95)
        
        return filename
    
    def split_text_balanced(self, text, font, max_height, max_width):
        """
        Split text into balanced chunks that fit within max_height
        Ensures no slide has too few words (min 5 words per slide)
        Based on NectarFromQuran's balanced chunking algorithm
        
        CRITICAL: max_height should be the ACTUAL available space considering:
        - Space after heading/content start
        - Space before reference (with proper margin)
        - Space for watermark if present
        """
        words = text.split()
        
        if len(words) <= 8:  # Short hadith, no need to split
            return [text]
        
        chunks = []
        current_chunk = []
        
        for word in words:
            test_chunk = ' '.join(current_chunk + [word])
            wrapped_lines = self.wrap_text(test_chunk, font, max_width)
            
            # Calculate height with proper line spacing
            line_height = font.getbbox('A')[3] * LINE_SPACING
            test_height = len(wrapped_lines) * line_height
            
            # Use 85% of max_height to ensure comfortable spacing
            if test_height <= (max_height * 0.85):
                current_chunk.append(word)
            else:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [word]
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # Balance chunks: if last chunk has very few words (<5) and there are multiple chunks,
        # redistribute words from previous chunk
        if len(chunks) >= 2:
            last_chunk_words = chunks[-1].split()
            if len(last_chunk_words) < 5:  # Too few words in last chunk
                prev_chunk_words = chunks[-2].split()
                
                if len(prev_chunk_words) >= 8:  # Previous chunk is large enough
                    # Calculate how many words to move
                    total_words = len(prev_chunk_words) + len(last_chunk_words)
                    words_to_move = (total_words // 2) - len(last_chunk_words)
                    
                    if words_to_move > 0 and words_to_move <= len(prev_chunk_words) // 2:
                        # Move words
                        moved_words = prev_chunk_words[-words_to_move:]
                        prev_chunk_words = prev_chunk_words[:-words_to_move]
                        last_chunk_words = moved_words + last_chunk_words
                        
                        # Update chunks
                        chunks[-2] = ' '.join(prev_chunk_words)
                        chunks[-1] = ' '.join(last_chunk_words)
        
        return chunks if chunks else [text]
    
    def create_swipe_indicator(self, current_slide, total_slides):
        """Create subtle 'Swipe →' text at bottom right"""
        indicator_img = Image.new('RGBA', (IMAGE_WIDTH, 50), (0, 0, 0, 0))
        draw = ImageDraw.Draw(indicator_img)
        
        # Get smaller, subtle font
        indicator_font = self.get_font('source', size=22)
        
        # Simple swipe text with right arrow
        swipe_text = "Swipe →"
        bbox = indicator_font.getbbox(swipe_text)
        text_width = bbox[2] - bbox[0]
        
        # Position at bottom right with padding
        text_x = IMAGE_WIDTH - text_width - 60
        text_y = 15
        
        # Subtle color matching theme (no outline, keep it minimal)
        text_color = self.hex_to_rgb(self.theme['source_color'])
        text_color = (*text_color, 150)  # Semi-transparent for subtlety
        
        draw.text((text_x, text_y), swipe_text, font=indicator_font, fill=text_color)
        
        return indicator_img
    
    def generate_post(self, output_path="output", specific_index=None, prefer_short=False):
        """
        Generate a hadith post (single or multi-slide carousel)
        
        Args:
            output_path: Directory to save generated images
            specific_index: Use specific hadith index (overrides prefer_short)
            prefer_short: Prefer hadiths that fit in <=10 slides (Instagram limit)
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Get hadith
        if specific_index is not None:
            index = specific_index
            hadith = self.hadiths[index]
            # Validate even for specific index
            if not validate_hadith_authenticity(hadith):
                raise ValueError(f"Hadith at index {index} is not Sahih or not properly verified!")
        else:
            hadith, index = self.get_next_hadith(prefer_short=prefer_short)
            if hadith is None:
                return None  # All hadiths posted
        
        # Create background
        img = self.create_gradient_background()
        
        draw = ImageDraw.Draw(img)
        
        # Load fonts
        heading_font = self.get_font('heading', bold=True)
        symbol_font = self.get_font('symbol')  # Special font for ﷺ
        main_font = self.get_font('main_text')
        source_font = self.get_font('source', bold=True)  # Make source bold like heading
        
        # Calculate starting position (lower if image is present)
        if USE_IMAGES:
            content_start_y = int(IMAGE_HEIGHT * IMAGE_HEIGHT_RATIO) + PADDING_TOP
        else:
            content_start_y = PADDING_TOP
        
        # Calculate where reference and watermark will be
        source_bbox = source_font.getbbox("Reference (Sahih)")
        reference_height = source_bbox[3] - source_bbox[1]
        
        watermark_height = 0
        if WATERMARK:
            watermark_font = self.get_font('source', WATERMARK_SIZE)
            watermark_bbox = watermark_font.getbbox(WATERMARK)
            watermark_height = watermark_bbox[3] - watermark_bbox[1]
        
        # Calculate bottom position (reference + watermark + spacing)
        bottom_reserved = PADDING_BOTTOM + watermark_height + reference_height + 30  # 30px spacing
        reference_top = IMAGE_HEIGHT - bottom_reserved
        
        # If showing heading on first slide, account for it
        heading_height = 0
        if SHOW_HEADING_FIRST_SLIDE:
            heading_height = max(heading_font.getbbox("A")[3], symbol_font.getbbox("ﷺ")[3]) + HEADING_TO_CONTENT_GAP
        
        # Calculate actual available height for text
        max_text_height = reference_top - content_start_y - heading_height - 40  # 40px safety margin
        
        # Ensure hadith text ends with fullstop
        hadith_text = hadith['text'].rstrip()
        if not hadith_text.endswith(('.', '!', '?', '।')):
            hadith_text += "."
        
        # Check if hadith text fits in one slide
        wrapped_lines = self.wrap_text(hadith_text, main_font, MAX_TEXT_WIDTH - 60)
        line_height = main_font.getbbox('A')[3] * LINE_SPACING
        total_text_height = len(wrapped_lines) * line_height
        
        # Determine if we need multiple slides
        needs_multiple_slides = total_text_height > max_text_height
        
        if needs_multiple_slides:
            # Split text into balanced chunks (using text with fullstop)
            text_chunks = self.split_text_balanced(hadith_text, main_font, max_text_height, MAX_TEXT_WIDTH - 60)
            
            # ⚠️ INSTAGRAM LIMIT: Max 10 slides per carousel
            if len(text_chunks) > 10:
                print(f"\n⚠️  WARNING: Hadith requires {len(text_chunks)} slides (Instagram limit: 10)")
                print(f"📏 Text length: {len(hadith['text'])} characters")
                print(f"💡 Options:")
                print(f"   1. Skip this hadith and use '--prefer-short' flag for automatic selection")
                print(f"   2. Post only first 10 slides (truncated)")
                print(f"   3. Split into 2 separate posts")
                print(f"\n⏭️  Skipping to next shorter hadith...\n")
                
                # Skip this hadith and get a shorter one
                self.posted_indices.append(index)
                return self.generate_post(output_path, specific_index=None)
            
            print(f"📖 Long hadith detected! Creating {len(text_chunks)} slides...")
            
            # Select ONE image for ALL slides in the carousel
            selected_image_path = None
            if USE_IMAGES and 'category' in hadith:
                selected_image_path = self.select_least_used_image(hadith['category'])
            
            # Generate multiple slides with the SAME image
            slide_files = []
            for slide_num, chunk in enumerate(text_chunks, 1):
                slide_img = self.generate_single_slide(
                    hadith, chunk, slide_num, len(text_chunks),
                    index, output_path, is_continuation=(slide_num > 1),
                    selected_image_path=selected_image_path
                )
                slide_files.append(slide_img)
            
            # Mark as posted
            if specific_index is None:
                self.save_posted_hadith(hadith)
            
            print(f"✅ Generated {len(slide_files)} slides for hadith {index + 1}")
            return slide_files, index, hadith
        
        else:
            # Single slide - add image overlay using the standard method
            if USE_IMAGES and 'category' in hadith:
                img = self.add_image_overlay(img, hadith['category'])
            
            # Initialize starting position for single slide
            if USE_IMAGES:
                y_pos = int(IMAGE_HEIGHT * IMAGE_HEIGHT_RATIO) + PADDING_TOP
            else:
                y_pos = PADDING_TOP
            
            # Optional: Draw heading with proper ﷺ symbol (only if enabled in config)
            if SHOW_HEADING_FIRST_SLIDE:
                text_before = "Hadith of the Day"
                symbol = ""  # Unicode symbol
                text_after = ":"
                
                # Calculate total width for centering
                temp_bbox = heading_font.getbbox(text_before + text_after)
                symbol_bbox = symbol_font.getbbox(symbol)
                total_width = (temp_bbox[2] - temp_bbox[0]) + (symbol_bbox[2] - symbol_bbox[0]) + 5
                heading_x = (IMAGE_WIDTH - total_width) // 2
                
                # Draw with special symbol handling
                self.draw_text_with_symbol(
                    draw, heading_x, y_pos,
                    text_before, symbol, text_after,
                    heading_font, symbol_font,
                    self.theme['heading_color'],
                    self.theme['heading_color']
                )
                
                y_pos += max(heading_font.getbbox("A")[3], symbol_font.getbbox(symbol)[3]) + HEADING_TO_CONTENT_GAP
            
            # Calculate where reference will be placed
            source_bbox = source_font.getbbox(f"{hadith['primary_source']} (Sahih)")
            
            # Calculate watermark position if present
            watermark_y = None
            watermark_height = 0
            if WATERMARK:
                watermark_font = self.get_font('source', WATERMARK_SIZE)
                watermark_bbox = watermark_font.getbbox(WATERMARK)
                watermark_height = watermark_bbox[3] - watermark_bbox[1]
                watermark_y = IMAGE_HEIGHT - PADDING_BOTTOM - watermark_height
            
            # Position reference ABOVE watermark with proper spacing
            if WATERMARK:
                reference_y = watermark_y - source_bbox[3] - 20  # 20px gap
            else:
                reference_y = IMAGE_HEIGHT - PADDING_BOTTOM - source_bbox[3] - 10
            
            # Calculate available space and center content vertically
            available_height = reference_y - y_pos
            vertical_offset = (available_height - total_text_height) // 2
            y_pos = y_pos + max(0, vertical_offset)
            
            # Draw text with proper alignment and symbol handling
            for line in wrapped_lines:
                # Calculate x position based on alignment
                if TEXT_ALIGNMENT == "left":
                    line_x = CONTENT_LEFT_MARGIN
                elif TEXT_ALIGNMENT == "right":
                    line_width = self.get_text_width_with_symbols(line, main_font, symbol_font)
                    line_x = IMAGE_WIDTH - CONTENT_RIGHT_MARGIN - line_width
                else:  # center
                    line_width = self.get_text_width_with_symbols(line, main_font, symbol_font)
                    line_x = (IMAGE_WIDTH - line_width) // 2
                
                # Draw with proper symbol handling
                if TEXT_SHADOW:
                    shadow_offset = 2
                    self.draw_text_with_arabic_symbols(
                        draw, line_x + shadow_offset, y_pos + shadow_offset, 
                        line, main_font, symbol_font, (0, 0, 0, 30)
                    )
                
                self.draw_text_with_arabic_symbols(
                    draw, line_x, y_pos, line, main_font, symbol_font, 
                    self.theme['text_color']
                )
                
                y_pos += line_height
            
            # Draw reference (same logic as multi-slide)
            source_text = f"{hadith['primary_source']} (Sahih)"
            source_bbox = source_font.getbbox(source_text)
            source_width = source_bbox[2] - source_bbox[0]
            
            # Position based on alignment setting
            if REFERENCE_ALIGNMENT == "left":
                source_x = CONTENT_LEFT_MARGIN
            elif REFERENCE_ALIGNMENT == "right":
                source_x = IMAGE_WIDTH - CONTENT_RIGHT_MARGIN - source_width
            else:  # center
                source_x = (IMAGE_WIDTH - source_width) // 2
            
            # Use the calculated reference_y from above
            draw.text((source_x, reference_y), source_text, fill=self.theme['source_color'], font=source_font)
            
            # Watermark (draw AFTER reference)
            if WATERMARK:
                watermark_font = self.get_font('source', WATERMARK_SIZE)
                watermark_bbox = watermark_font.getbbox(WATERMARK)
                watermark_width = watermark_bbox[2] - watermark_bbox[0]
                watermark_x = (IMAGE_WIDTH - watermark_width) // 2
                # Use the watermark_y calculated above
                
                # Create semi-transparent watermark
                watermark_color = self.hex_to_rgb(self.theme['source_color'])
                watermark_color = (*watermark_color[:3], WATERMARK_OPACITY)
                
                draw.text(
                    (watermark_x, watermark_y),
                    WATERMARK,
                    fill=watermark_color,
                    font=watermark_font
                )
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_path}/hadith_{index}_{timestamp}.png"
            img.save(filename, quality=95)
        
            # Mark as posted (if not generating sample)
            if specific_index is None:
                self.save_posted_hadith(hadith)
            
            print(f"✅ Generated: {filename}")
            print(f"📖 Hadith {index + 1}/{len(self.hadiths)}")
            print(f"📚 Book: {hadith['book']}")
            print(f"✓ Grade: {hadith['grade']} (Verified)")
            print(f"🎨 Theme: {self.theme['name']}")
            print(f"📝 Text: {hadith['text'][:50]}...")
            
            return [filename], index, hadith  # Return as list for consistency


def generate_theme_samples():
    """Generate sample posts for all themes to help you choose"""
    print("🎨 Generating theme samples...\n")
    
    os.makedirs("theme_samples", exist_ok=True)
    
    # Use the first hadith as sample for all themes
    sample_index = 0
    hadiths = get_sahih_hadiths()
    
    for theme_name, theme_config in THEMES.items():
        print(f"Creating sample for: {theme_config['name']}")
        generator = HadithPostGenerator(theme_name)
        output_path = generator.generate_post("theme_samples", specific_index=sample_index)
        print()
    
    print("✅ All theme samples generated in 'theme_samples' folder!")
    print("📂 Review them and choose your favorite theme")
    print(f"📚 Using {len(hadiths)} authenticated Sahih hadiths")


if __name__ == "__main__":
    # Uncomment ONE of the options below:
    
    # Option 1: Generate theme samples to choose from
    generate_theme_samples()
    
    # Option 2: Generate a single post with default theme
    # generator = HadithPostGenerator()
    # generator.generate_post()
    
    # Option 3: Generate with specific theme
    # generator = HadithPostGenerator("sage_green")
    # generator.generate_post()
