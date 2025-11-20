#!/bin/bash

# GitHub Actions Setup Script
# Run this once to prepare your repository for automated posting

set -e

echo "============================================================"
echo "📿 SADAQAH HADITH - GitHub Actions Setup"
echo "============================================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git branch -M main
else
    echo "✅ Git repository already initialized"
fi

# Create necessary files if they don't exist
echo "📁 Creating necessary files..."

if [ ! -f "posted_hadiths.json" ]; then
    echo "[]" > posted_hadiths.json
    echo "✅ Created posted_hadiths.json"
fi

mkdir -p output logs fonts
echo "✅ Created directories"

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Automated Daily Hadith Posts

- 5x daily automated posting via GitHub Actions
- Sahih hadiths verified from 2+ sources
- No external image dependencies (reliable)
- Cross-platform font support
- Book rotation algorithm" || echo "Nothing to commit or already committed"

echo ""
echo "============================================================"
echo "✅ REPOSITORY PREPARED!"
echo "============================================================"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1️⃣  Create a GitHub repository:"
echo "   - Go to github.com/new"
echo "   - Name: sadaqah-hadith (or your choice)"
echo "   - Public or Private"
echo "   - Don't initialize with README"
echo ""
echo "2️⃣  Push this repository:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "   git push -u origin main"
echo ""
echo "3️⃣  Add Instagram secrets in GitHub:"
echo "   - Go to Settings → Secrets and variables → Actions"
echo "   - Add: INSTAGRAM_USERNAME = your_instagram_username"
echo "   - Add: INSTAGRAM_PASSWORD = your_instagram_password"
echo ""
echo "4️⃣  Enable GitHub Actions:"
echo "   - Go to Actions tab"
echo "   - Click 'I understand my workflows, go ahead and enable them'"
echo ""
echo "5️⃣  Set workflow permissions:"
echo "   - Settings → Actions → General → Workflow permissions"
echo "   - Select 'Read and write permissions'"
echo "   - Check 'Allow GitHub Actions to create and approve pull requests'"
echo ""
echo "6️⃣  Test the workflow:"
echo "   - Go to Actions tab"
echo "   - Click 'Daily Hadith Posts' workflow"
echo "   - Click 'Run workflow' → 'Run workflow'"
echo ""
echo "============================================================"
echo "🎊 AUTOMATED 5X DAILY POSTING - READY!"
echo "============================================================"
echo ""
echo "Posts will run automatically at:"
echo "  • 4:00 AM UTC (Fajr time)"
echo "  • 11:00 AM UTC (Dhuhr time)"
echo "  • 2:00 PM UTC (Asr time)"
echo "  • 5:00 PM UTC (Maghrib time)"
echo "  • 8:00 PM UTC (Isha time)"
echo ""
echo "📖 See GITHUB_SETUP.md for complete instructions"
echo ""
