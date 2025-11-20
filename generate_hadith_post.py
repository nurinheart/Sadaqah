"""
Daily Hadith Post Generator
Creates beautiful, consistent Instagram posts with Sahih hadiths
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import os
from datetime import datetime
import textwrap
from config import *
from hadith_data import get_sahih_hadiths, validate_hadith_authenticity


class HadithPostGenerator:
    def __init__(self, theme_name=DEFAULT_THEME):
        self.theme = THEMES.get(theme_name, THEMES[DEFAULT_THEME])
        self.posted_file = "posted_hadiths.json"
        self.hadiths = get_sahih_hadiths()  # Only use validated Sahih hadiths
        self.load_posted_hadiths()
        
    def load_posted_hadiths(self):
        """Load list of already posted hadith indices to avoid repeats"""
        if os.path.exists(self.posted_file):
            with open(self.posted_file, 'r') as f:
                self.posted_indices = json.load(f)
        else:
            self.posted_indices = []
    
    def save_posted_hadith(self, index):
        """Save the index of posted hadith"""
        self.posted_indices.append(index)
        with open(self.posted_file, 'w') as f:
            json.dump(self.posted_indices, f)
    
    def get_next_hadith(self):
        """Get next unposted Sahih hadith with rotation across books"""
        available = [i for i in range(len(self.hadiths)) if i not in self.posted_indices]
        
        if not available:
            print("All hadiths have been posted! Resetting...")
            self.posted_indices = []
            available = list(range(len(self.hadiths)))
        
        # Get book distribution to ensure rotation
        posted_books = {}
        for idx in self.posted_indices:
            if idx < len(self.hadiths):
                book = self.hadiths[idx]['book']
                posted_books[book] = posted_books.get(book, 0) + 1
        
        # Try to pick from least-posted book for variety
        best_index = None
        min_count = float('inf')
        
        for idx in available:
            book = self.hadiths[idx]['book']
            count = posted_books.get(book, 0)
            if count < min_count:
                min_count = count
                best_index = idx
        
        index = best_index if best_index is not None else available[0]
        hadith = self.hadiths[index]
        
        # Double-check authenticity before posting
        if not validate_hadith_authenticity(hadith):
            print(f"⚠️  WARNING: Hadith {index} failed validation, skipping...")
            self.posted_indices.append(index)
            return self.get_next_hadith()
        
        return index, hadith
    
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
        """Get font with Product Sans priority"""
        if size is None:
            size = FONTS[font_type]['size']
        
        # Special handling for Arabic/symbol fonts
        if font_type == 'symbol':
            for font_path in ARABIC_FONTS:
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
        
        # Try Product Sans first for regular text
        product_sans_path = FONT_PATHS['product_sans_bold'] if bold else FONT_PATHS['product_sans_regular']
        try:
            if os.path.exists(product_sans_path):
                return ImageFont.truetype(product_sans_path, size)
        except:
            pass
        
        # Fallback to system fonts (modern, clean options)
        font_options = [
            '/System/Library/Fonts/Supplemental/Arial.ttf',
            '/System/Library/Fonts/SFNS.ttf',  # San Francisco
            '/System/Library/Fonts/Helvetica.ttc',
            'Arial.ttf',
            'Helvetica.ttf'
        ]
        
        for font_path in font_options:
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
        
        # Last resort: Pillow default but larger
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
        baseline_offset = text_ascent - symbol_ascent - 7  # Raise 5px
        
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
    
    def add_image_overlay(self, base_img, category):
        """Add halal nature/pattern image from LOCAL storage (no network calls)"""
        if not USE_IMAGES:
            return base_img
        
        # Get LOCAL image path for category (no URLs!)
        image_path = LOCAL_IMAGES.get(category, LOCAL_IMAGES['default'])
        
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
    
    def generate_post(self, output_path="output", specific_index=None):
        """Generate a hadith post"""
        
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
            index, hadith = self.get_next_hadith()
        
        # Create background
        img = self.create_gradient_background()
        
        # Add category image if enabled
        if USE_IMAGES and 'category' in hadith:
            img = self.add_image_overlay(img, hadith['category'])
        
        draw = ImageDraw.Draw(img)
        
        # Load fonts
        heading_font = self.get_font('heading', bold=True)
        symbol_font = self.get_font('symbol')  # Special font for ﷺ
        main_font = self.get_font('main_text')
        source_font = self.get_font('source', bold=True)  # Make source bold like heading
        
        # Calculate starting position (lower if image is present)
        if USE_IMAGES:
            y_pos = int(IMAGE_HEIGHT * IMAGE_HEIGHT_RATIO) + PADDING + 40
        else:
            y_pos = PADDING + 100
        
        # Draw heading with proper ﷺ symbol
        text_before = "The Prophet "
        symbol = "ﷺ"  # Unicode symbol
        text_after = " said:"
        
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
        
        y_pos += max(heading_font.getbbox("A")[3], symbol_font.getbbox(symbol)[3]) + 60
        
        # Draw main hadith text (wrapped and centered with better spacing)
        wrapped_lines = self.wrap_text(hadith['text'], main_font, MAX_TEXT_WIDTH - 60)
        
        # Calculate total text height with proper spacing
        line_height = main_font.getbbox('A')[3] * LINE_SPACING
        total_text_height = len(wrapped_lines) * line_height
        
        # Better vertical centering considering image and spacing
        if USE_IMAGES:
            available_height = IMAGE_HEIGHT - int(IMAGE_HEIGHT * IMAGE_HEIGHT_RATIO) - PADDING * 2 - 250
            y_pos = int(IMAGE_HEIGHT * IMAGE_HEIGHT_RATIO) + PADDING + 140 + (available_height - total_text_height) // 2
        else:
            y_pos = (IMAGE_HEIGHT - total_text_height) // 2 - 20
        
        # Draw text with subtle shadow for depth (optional)
        for line in wrapped_lines:
            bbox = main_font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_x = (IMAGE_WIDTH - line_width) // 2
            
            # Optional subtle shadow for aesthetic depth
            if TEXT_SHADOW:
                shadow_offset = 2
                draw.text(
                    (line_x + shadow_offset, y_pos + shadow_offset),
                    line,
                    fill=(0, 0, 0, 30),  # Very subtle shadow
                    font=main_font
                )
            
            # Main text
            draw.text(
                (line_x, y_pos),
                line,
                fill=self.theme['text_color'],
                font=main_font
            )
            
            y_pos += line_height
        
        # Draw source at bottom with authenticity grade
        # Primary source with (Sahih) grade
        source_text = f"{hadith['primary_source']} (Sahih)"
        source_bbox = source_font.getbbox(source_text)
        source_width = source_bbox[2] - source_bbox[0]
        source_x = (IMAGE_WIDTH - source_width) // 2
        source_y = IMAGE_HEIGHT - PADDING - 130
        
        # Draw primary source with bold styling
        draw.text(
            (source_x, source_y),
            source_text,
            fill=self.theme['source_color'],
            font=source_font
        )
        
        # Draw verification note (simplified - doesn't show specific source)
        verification_font = self.get_font('source', size=26)
        verification_text = "Verified from 2+ authentic sources"
        verif_bbox = verification_font.getbbox(verification_text)
        verif_width = verif_bbox[2] - verif_bbox[0]
        verif_x = (IMAGE_WIDTH - verif_width) // 2
        verif_y = source_y + 45
        
        draw.text(
            (verif_x, verif_y),
            verification_text,
            fill=self.theme['source_color'],
            font=verification_font
        )
        
        # Optional watermark
        if WATERMARK:
            watermark_font = self.get_font('source', WATERMARK_SIZE)
            watermark_bbox = watermark_font.getbbox(WATERMARK)
            watermark_width = watermark_bbox[2] - watermark_bbox[0]
            watermark_x = (IMAGE_WIDTH - watermark_width) // 2
            watermark_y = IMAGE_HEIGHT - PADDING - 40
            
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
            self.save_posted_hadith(index)
        
        print(f"✅ Generated: {filename}")
        print(f"📖 Hadith {index + 1}/{len(self.hadiths)}")
        print(f"📚 Book: {hadith['book']}")
        print(f"✓ Grade: {hadith['grade']} (Verified)")
        print(f"🎨 Theme: {self.theme['name']}")
        print(f"📝 Text: {hadith['text'][:50]}...")
        
        return filename, index, hadith


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
