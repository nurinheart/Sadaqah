"""
Archive generated hadith slides to GitHub repository
Organizes by book and hadith number for easy retrieval
"""
import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import re

def get_hadith_info(index, hadith_data):
    """Get hadith information from the data"""
    from hadith_data import HADITHS
    if 0 <= index < len(HADITHS):
        hadith = HADITHS[index]
        return {
            'index': index,
            'book': hadith['book'],
            'source': hadith['primary_source'],
            'category': hadith['category']
        }
    return None

def extract_hadith_number(source):
    """Extract hadith number from source like 'Sahih al-Bukhari 6464'"""
    match = re.search(r'\d+', source)
    return match.group() if match else "unknown"

def sanitize_filename(name):
    """Create filesystem-safe name"""
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

def archive_hadith_slides(output_dir="output", archive_base="archive"):
    """
    Archive all generated slides from output directory
    Organized as: archive/{book}/{hadith_number}/
    """
    print("=" * 70)
    print("📁 ARCHIVING HADITH SLIDES")
    print("=" * 70)
    print()
    
    # Get list of generated images
    if not os.path.exists(output_dir):
        print("⚠️  No output directory found")
        return 0
    
    image_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
    
    if not image_files:
        print("⚠️  No images to archive")
        return 0
    
    # Load hadith data
    from hadith_data import HADITHS
    
    archived_count = 0
    
    # Group files by hadith index
    hadith_groups = {}
    for filename in image_files:
        # Extract hadith index from filename: hadith_{index}_timestamp.png or hadith_{index}_timestamp_slide{n}.png
        match = re.match(r'hadith_(\d+)_', filename)
        if match:
            index = int(match.group(1))
            if index not in hadith_groups:
                hadith_groups[index] = []
            hadith_groups[index].append(filename)
    
    # Archive each hadith group
    for hadith_index, files in hadith_groups.items():
        if hadith_index >= len(HADITHS):
            print(f"⚠️  Skipping invalid index: {hadith_index}")
            continue
        
        hadith = HADITHS[hadith_index]
        book = hadith['book']
        source = hadith['primary_source']
        category = hadith['category']
        
        # Extract hadith number from source
        hadith_num = extract_hadith_number(source)
        
        # Create archive path: archive/{book}/{hadith_number}/
        book_safe = sanitize_filename(book)
        archive_path = os.path.join(archive_base, book_safe, f"hadith_{hadith_num}")
        os.makedirs(archive_path, exist_ok=True)
        
        # Sort files (to maintain slide order)
        files.sort()
        
        # Copy each file
        for i, filename in enumerate(files, 1):
            src = os.path.join(output_dir, filename)
            
            # Create descriptive filename
            if len(files) > 1:
                # Multi-slide: slide_1.png, slide_2.png, etc.
                dst_filename = f"slide_{i}.png"
            else:
                # Single slide
                dst_filename = "image.png"
            
            dst = os.path.join(archive_path, dst_filename)
            
            # Copy file
            shutil.copy2(src, dst)
            archived_count += 1
            
            print(f"✅ Archived: {book_safe}/hadith_{hadith_num}/{dst_filename}")
        
        # Create metadata file
        metadata = {
            'hadith_index': hadith_index,
            'book': book,
            'source': source,
            'verification': hadith['verification_source'],
            'category': category,
            'grade': hadith['grade'],
            'text': hadith['text'],
            'archived_date': datetime.now().isoformat(),
            'slide_count': len(files)
        }
        
        metadata_path = os.path.join(archive_path, 'metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"   📝 Metadata saved")
    
    print()
    print("=" * 70)
    print(f"✅ ARCHIVED {archived_count} slides from {len(hadith_groups)} hadiths")
    print("=" * 70)
    
    return archived_count

if __name__ == "__main__":
    archived = archive_hadith_slides()
    
    if archived > 0:
        print()
        print("📂 Archive structure:")
        print("   archive/")
        print("   ├── Sahih_al_Bukhari/")
        print("   │   ├── hadith_1/")
        print("   │   │   ├── image.png")
        print("   │   │   └── metadata.json")
        print("   │   └── hadith_6464/")
        print("   │       ├── slide_1.png")
        print("   │       ├── slide_2.png")
        print("   │       └── metadata.json")
        print("   └── Sahih_Muslim/")
        print("       └── ...")
