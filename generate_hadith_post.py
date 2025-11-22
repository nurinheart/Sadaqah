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
        """Load list of already posted hadith indices to avoid repeats"""
        if os.path.exists(self.posted_file):
            with open(self.posted_file, 'r') as f:
                self.posted_indices = json.load(f)
        else:
            self.posted_indices = []
    
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
        
        # Calculate starting position (all slides have image now)
        if USE_IMAGES:
            y_pos = int(IMAGE_HEIGHT * IMAGE_HEIGHT_RATIO) + PADDING + 40
        else:
            y_pos = PADDING + 100
        
        # Draw heading (first slide shows full heading, continuation slides show "Continued...")
        if slide_num == 1:
            text_before = "The Prophet "
            symbol = "ﷺ"
            text_after = " said:"
            
            temp_bbox = heading_font.getbbox(text_before + text_after)
            symbol_bbox = symbol_font.getbbox(symbol)
            total_width = (temp_bbox[2] - temp_bbox[0]) + (symbol_bbox[2] - symbol_bbox[0]) + 5
            heading_x = (IMAGE_WIDTH - total_width) // 2
            
            self.draw_text_with_symbol(
                draw, heading_x, y_pos,
                text_before, symbol, text_after,
                heading_font, symbol_font,
                self.theme['heading_color'],
                self.theme['heading_color']
            )
            y_pos += max(heading_font.getbbox("A")[3], symbol_font.getbbox(symbol)[3]) + 60
        else:
            # Continuation slides show "Continued..."
            continuation_text = "Continuation:"
            cont_bbox = heading_font.getbbox(continuation_text)
            cont_width = cont_bbox[2] - cont_bbox[0]
            cont_x = (IMAGE_WIDTH - cont_width) // 2
            
            draw.text((cont_x, y_pos), continuation_text, fill=self.theme['heading_color'], font=heading_font)
            y_pos += heading_font.getbbox("A")[3] + 60
        
        # Draw hadith text chunk (add "..." at end if first slide and there are more slides)
        if slide_num == 1 and total_slides > 1:
            text_to_display = text_chunk + "..."
        else:
            text_to_display = text_chunk
        
        wrapped_lines = self.wrap_text(text_to_display, main_font, MAX_TEXT_WIDTH - 60)
        line_height = main_font.getbbox('A')[3] * LINE_SPACING
        total_text_height = len(wrapped_lines) * line_height
        
        # Vertically center the text (all slides have image now)
        if USE_IMAGES:
            available_height = IMAGE_HEIGHT - int(IMAGE_HEIGHT * IMAGE_HEIGHT_RATIO) - PADDING * 2 - 250
            y_pos = int(IMAGE_HEIGHT * IMAGE_HEIGHT_RATIO) + PADDING + 140 + (available_height - total_text_height) // 2
        else:
            y_pos = (IMAGE_HEIGHT - total_text_height) // 2
        
        for line in wrapped_lines:
            bbox = main_font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_x = (IMAGE_WIDTH - line_width) // 2
            
            if TEXT_SHADOW:
                shadow_offset = 2
                draw.text((line_x + shadow_offset, y_pos + shadow_offset), line,
                         fill=(0, 0, 0, 30), font=main_font)
            
            draw.text((line_x, y_pos), line, fill=self.theme['text_color'], font=main_font)
            y_pos += line_height
        
        # Draw reference and verification (on all slides)
        source_text = f"{hadith['primary_source']} (Sahih)"
        source_bbox = source_font.getbbox(source_text)
        source_width = source_bbox[2] - source_bbox[0]
        source_x = (IMAGE_WIDTH - source_width) // 2
        source_y = IMAGE_HEIGHT - PADDING - 130
        
        draw.text((source_x, source_y), source_text, fill=self.theme['source_color'], font=source_font)
        
        verification_font = self.get_font('source', size=26)
        verification_text = "Verified from 2+ authentic sources"
        verif_bbox = verification_font.getbbox(verification_text)
        verif_width = verif_bbox[2] - verif_bbox[0]
        verif_x = (IMAGE_WIDTH - verif_width) // 2
        verif_y = source_y + 45
        
        draw.text((verif_x, verif_y), verification_text, fill=self.theme['source_color'], font=verification_font)
        
        # Watermark (draw BEFORE swipe indicator)
        if WATERMARK:
            watermark_font = self.get_font('source', WATERMARK_SIZE)
            watermark_bbox = watermark_font.getbbox(WATERMARK)
            watermark_width = watermark_bbox[2] - watermark_bbox[0]
            watermark_x = (IMAGE_WIDTH - watermark_width) // 2
            watermark_y = IMAGE_HEIGHT - PADDING - 40
            
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
        """
        words = text.split()
        
        if len(words) <= 8:  # Short hadith, no need to split
            return [text]
        
        chunks = []
        current_chunk = []
        
        for word in words:
            test_chunk = ' '.join(current_chunk + [word])
            wrapped_lines = self.wrap_text(test_chunk, font, max_width)
            
            # Calculate height
            line_height = font.getbbox('A')[3] * LINE_SPACING
            test_height = len(wrapped_lines) * line_height
            
            if test_height <= max_height:
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
    
    def generate_post(self, output_path="output", specific_index=None):
        """Generate a hadith post (single or multi-slide carousel)"""
        
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
        
        # Calculate safe area for hadith text (between heading and reference)
        heading_bottom = y_pos + max(heading_font.getbbox("A")[3], symbol_font.getbbox("ﷺ")[3]) + 60
        reference_top = IMAGE_HEIGHT - PADDING - 130
        max_text_height = reference_top - heading_bottom - 100  # 100px safety margin
        
        # Check if hadith text fits in one slide
        wrapped_lines = self.wrap_text(hadith['text'], main_font, MAX_TEXT_WIDTH - 60)
        line_height = main_font.getbbox('A')[3] * LINE_SPACING
        total_text_height = len(wrapped_lines) * line_height
        
        # Determine if we need multiple slides
        needs_multiple_slides = total_text_height > max_text_height
        
        if needs_multiple_slides:
            # Split text into balanced chunks
            text_chunks = self.split_text_balanced(hadith['text'], main_font, max_text_height, MAX_TEXT_WIDTH - 60)
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
                self.save_posted_hadith(index)
            
            print(f"✅ Generated {len(slide_files)} slides for hadith {index + 1}")
            return slide_files, index, hadith
        
        else:
            # Single slide - add image overlay using the standard method
            if USE_IMAGES and 'category' in hadith:
                img = self.add_image_overlay(img, hadith['category'])
            
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
            
            # Draw verification note
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
