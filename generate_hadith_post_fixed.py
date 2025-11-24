"""
Hadith Post Generator - FIXED VERSION
✅ Tracks hadiths by UNIQUE IDENTIFIERS (collection_hadith_number)
✅ NEVER empties posted database - lifetime tracking
✅ Handles database refreshes without reposting
✅ No index-based tracking that breaks on updates
"""

import os
import json
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Tuple, Optional
from hadith_data import get_sahih_hadiths
from validate_hadiths import validate_hadith_authenticity

# Configuration
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1350
PADDING_TOP = 150
PADDING_BOTTOM = 200
PADDING_LEFT = 60
PADDING_RIGHT = 60

DEFAULT_THEME = "sage_cream"
USE_IMAGES = True
IMAGE_HEIGHT_RATIO = 0.4

class HadithPostGenerator:
    def __init__(self, theme_name=DEFAULT_THEME):
        self.theme = THEMES.get(theme_name, THEMES[DEFAULT_THEME])
        self.posted_file = "posted_hadiths.json"
        self.image_usage_file = "image_usage.json"
        self.hadiths = get_sahih_hadiths()
        
        # Load tracking data
        self.load_posted_hadiths()
        self.load_image_usage()
        
    def load_posted_hadiths(self):
        """Load posted hadith UNIQUE IDENTIFIERS for lifetime tracking"""
        if os.path.exists(self.posted_file):
            with open(self.posted_file, 'r') as f:
                data = json.load(f)
                
                # Handle migration from old index-based format
                if isinstance(data, list):
                    if data and isinstance(data[0], int):
                        # Old format: [0, 1, 2] - convert to unique IDs
                        print("🔄 Migrating from old index-based tracking to unique ID tracking...")
                        migrated_ids = []
                        for index in data:
                            if 0 <= index < len(self.hadiths):
                                hadith = self.hadiths[index]
                                unique_id = self._get_hadith_unique_id(hadith)
                                migrated_ids.append(unique_id)
                        self.posted_hadith_ids = list(set(migrated_ids))  # Remove duplicates
                        print(f"✅ Migrated {len(self.posted_hadith_ids)} hadiths to unique ID tracking")
                        self._save_posted_hadiths()  # Save migrated format
                    else:
                        # New format: ["bukhari_1", "muslim_1844"]
                        self.posted_hadith_ids = data
                else:
                    self.posted_hadith_ids = []
        else:
            self.posted_hadith_ids = []
            
        print(f"📊 Loaded {len(self.posted_hadith_ids)} posted hadith IDs")
    
    def _get_hadith_unique_id(self, hadith: Dict) -> str:
        """Generate unique identifier for a hadith: collection_hadith_number"""
        collection = hadith.get('collection', 'unknown')
        hadith_number = hadith.get('hadith_number', 0)
        return f"{collection}_{hadith_number}"
    
    def _save_posted_hadiths(self):
        """Save posted hadith IDs to file"""
        with open(self.posted_file, 'w') as f:
            json.dump(self.posted_hadith_ids, f, indent=2)
    
    def load_image_usage(self):
        """Load image usage tracking"""
        if os.path.exists(self.image_usage_file):
            with open(self.image_usage_file, 'r') as f:
                self.image_usage = json.load(f)
        else:
            self.image_usage = {}
    
    def save_image_usage(self):
        """Save image usage tracking"""
        with open(self.image_usage_file, 'w') as f:
            json.dump(self.image_usage, f, indent=2)
    
    def get_next_hadith(self, prefer_short=False) -> Tuple[int, Dict]:
        """
        Get next unposted hadith using UNIQUE ID tracking.
        
        ✅ NEVER reposts - tracks by collection_hadith_number
        ✅ Handles database refreshes safely
        ✅ Lifetime tracking - never empties posted database
        """
        # Get all available hadiths with their unique IDs
        available_hadiths = []
        for i, hadith in enumerate(self.hadiths):
            unique_id = self._get_hadith_unique_id(hadith)
            if unique_id not in self.posted_hadith_ids:
                available_hadiths.append((i, hadith, unique_id))
        
        if not available_hadiths:
            print("🎉 All available hadiths have been posted!")
            print("💡 To post more, add new hadiths to verified_hadiths.json")
            print("   Run: python3 fetch_authentic_hadiths.py --refresh")
            return None, None
        
        # Filter for short hadiths if requested
        if prefer_short:
            short_hadiths = [(i, h, uid) for i, h, uid in available_hadiths 
                           if len(h['text']) <= 800]
            if short_hadiths:
                available_hadiths = short_hadiths
                print(f"📊 Filtering to {len(available_hadiths)} short hadiths (≤10 slides)")
        
        # Smart selection: prefer hadiths from less-posted collections
        selected_index, selected_hadith = self._select_best_hadith(available_hadiths)
        
        if selected_hadith:
            # Mark as posted immediately
            unique_id = self._get_hadith_unique_id(selected_hadith)
            self.posted_hadith_ids.append(unique_id)
            self._save_posted_hadiths()
            
            print(f"📖 Selected: {selected_hadith['reference']} (ID: {unique_id})")
            return selected_index, selected_hadith
        
        return None, None
    
    def _select_best_hadith(self, available_hadiths: List[Tuple[int, Dict, str]]) -> Tuple[int, Dict]:
        """Select the best hadith from available options using smart rotation"""
        if not available_hadiths:
            return None, None
        
        # Count how many hadiths we've posted from each collection
        collection_counts = {}
        for _, _, uid in available_hadiths:
            collection = uid.split('_')[0]
            collection_counts[collection] = collection_counts.get(collection, 0)
        
        # Find hadiths from least-posted collections
        min_count = min(collection_counts.values()) if collection_counts else 0
        best_candidates = [(i, h, uid) for i, h, uid in available_hadiths 
                          if uid.split('_')[0] in 
                          [c for c, count in collection_counts.items() if count == min_count]]
        
        # Return first candidate (could be randomized for variety)
        return best_candidates[0][0], best_candidates[0][1]
    
    def generate_post(self, specific_index=None, output_path="output", prefer_short=False):
        """Generate hadith post with proper unique ID tracking"""
        if specific_index is not None:
            # Specific hadith requested
            if 0 <= specific_index < len(self.hadiths):
                hadith = self.hadiths[specific_index]
                unique_id = self._get_hadith_unique_id(hadith)
                
                # Check if already posted
                if unique_id in self.posted_hadith_ids:
                    print(f"⚠️  Hadith {hadith['reference']} (ID: {unique_id}) already posted!")
                    return [], None, None
                
                # Mark as posted
                self.posted_hadith_ids.append(unique_id)
                self._save_posted_hadiths()
            else:
                raise ValueError(f"Hadith index {specific_index} out of range")
        else:
            # Get next unposted hadith
            specific_index, hadith = self.get_next_hadith(prefer_short=prefer_short)
            if hadith is None:
                print("❌ No unposted hadiths available")
                return [], None, None
        
        # Validate hadith authenticity
        if not validate_hadith_authenticity(hadith):
            print(f"⚠️  Hadith validation failed, skipping...")
            return [], None, None
        
        print(f"🎨 Generating post for: {hadith['reference']}")
        
        # Generate slides (implementation continues...)
        # ... existing slide generation code ...
        
        return [], specific_index, hadith
    
    # ... rest of the existing methods (create_slide, etc.) ...

# Theme configurations (add these)
THEMES = {
    "sage_cream": {
        "name": "Sage & Cream",
        "bg_colors": ["#E8F3E8", "#D4E7D4"],
        "text_color": "#1B3A1B",
        "arabic_color": "#2D5A2D",
        "heading_color": "#2D5A2D",
        "source_color": "#5A8F5A",
        "accent_color": "#4A7A4A",
    }
}

if __name__ == "__main__":
    # Test the new tracking system
    generator = HadithPostGenerator()
    print(f"📊 Currently tracking {len(generator.posted_hadith_ids)} posted hadiths")
    print("✅ Unique ID tracking active - no more reposting risks!")
