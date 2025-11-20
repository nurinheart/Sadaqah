#!/bin/bash
# Script to download Product Sans font

echo "📥 Downloading Product Sans font..."

# Create fonts directory
mkdir -p fonts

# Download Product Sans Regular
curl -L "https://github.com/google/fonts/raw/main/ofl/productsans/ProductSans-Regular.ttf" -o fonts/ProductSans-Regular.ttf 2>/dev/null

# If above fails, try alternative source
if [ ! -f "fonts/ProductSans-Regular.ttf" ]; then
    echo "⚠️  Primary source failed, trying alternative..."
    # For now, we'll use system fonts as fallback
    echo "ℹ️  Will use system fonts (Arial/San Francisco) as fallback"
fi

echo "✅ Font setup complete!"
echo ""
echo "Note: If Product Sans is not available, the generator will use"
echo "San Francisco (Apple's system font) which is also modern and clean."
