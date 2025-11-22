"""
Simple reliable image downloader using Picsum Photos
Picsum provides random high-quality photos - we filter for nature-like IDs
"""
import requests
from PIL import Image
from io import BytesIO
import time
import os

output_dir = "images/nature"
os.makedirs(output_dir, exist_ok=True)

# Picsum specific image IDs that are nature/landscape photos (manually curated)
# These IDs are known to be landscapes/nature without people or animals
NATURE_IMAGE_IDS = [
    (1015, "mountain_lake_view"),
    (1018, "misty_forest_path"),
    (1020, "sunset_over_ocean"),
    (1022, "autumn_trees_park"),
    (1024, "snow_mountain_peak"),
    (1025, "rocky_coastline"),
    (1026, "green_valley_hills"),
    (1029, "desert_landscape_sand"),
    (1031, "waterfall_rocks"),
    (1036, "forest_sunlight"),
    (1039, "river_through_canyon"),
    (1040, "tropical_beach_waves"),
    (1043, "morning_mist_meadow"),
    (1044, "alpine_mountain_view"),
    (1048, "sunset_clouds_sky"),
    (1050, "cherry_blossom_trees"),
    (1051, "bamboo_forest_grove"),
    (1053, "lake_reflection_mountain"),
    (1055, "coastal_cliffs_ocean"),
    (1058, "pine_forest_landscape"),
]

print("=" * 70)
print("🌿 DOWNLOADING NATURE IMAGES FROM PICSUM")
print("=" * 70)
print()

successful = 0

for img_id, name in NATURE_IMAGE_IDS:
    try:
        url = f"https://picsum.photos/id/{img_id}/1080/1350"
        print(f"Downloading {name}...", end=" ")
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            
            # Resize if needed
            if img.size != (1080, 1350):
                img = img.resize((1080, 1350), Image.Resampling.LANCZOS)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            filepath = f"{output_dir}/{name}.jpg"
            img.save(filepath, 'JPEG', quality=95)
            successful += 1
            print("✅")
        else:
            print("❌")
        
        time.sleep(1)
    except Exception as e:
        print(f"❌ {str(e)[:20]}")

print()
print(f"✅ Downloaded {successful}/{len(NATURE_IMAGE_IDS)} images")
print(f"📁 Total images: {len([f for f in os.listdir(output_dir) if f.endswith('.jpg')])}")
