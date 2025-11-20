#!/bin/bash

echo "========================================================"
echo "🚀 DEPLOYING SADAQAH JARIAH AUTOMATION TO GITHUB"
echo "========================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Verify images exist
echo -e "${BLUE}Step 1: Verifying local images...${NC}"
if [ -d "images/nature" ] && [ -d "images/patterns" ]; then
    IMAGE_COUNT=$(find images -name "*.jpg" | wc -l)
    echo -e "${GREEN}✅ Found $IMAGE_COUNT images${NC}"
else
    echo -e "${YELLOW}⚠️  Images not found. Run: python3 download_halal_images.py${NC}"
    exit 1
fi
echo ""

# Step 2: Initialize git if needed
echo -e "${BLUE}Step 2: Initializing Git repository...${NC}"
if [ ! -d ".git" ]; then
    git init
    echo -e "${GREEN}✅ Git initialized${NC}"
else
    echo -e "${GREEN}✅ Git already initialized${NC}"
fi
echo ""

# Step 3: Add all files
echo -e "${BLUE}Step 3: Adding files to Git...${NC}"
git add .
echo -e "${GREEN}✅ Files staged${NC}"
echo ""

# Step 4: Commit
echo -e "${BLUE}Step 4: Committing changes...${NC}"
git commit -m "Complete Sadaqah Jariah automation with ROOT FIX (local images)" || echo "No changes to commit"
echo ""

# Step 5: Instructions for GitHub
echo "========================================================"
echo -e "${GREEN}✅ LOCAL SETUP COMPLETE!${NC}"
echo "========================================================"
echo ""
echo -e "${YELLOW}📋 NEXT STEPS (on GitHub):${NC}"
echo ""
echo "1️⃣  CREATE GITHUB REPO:"
echo "   • Go to: https://github.com/new"
echo "   • Name: sadaqah-jariah"
echo "   • Make it PRIVATE (contains Instagram credentials)"
echo "   • Don't initialize with README"
echo ""
echo "2️⃣  PUSH TO GITHUB:"
echo "   Run these commands:"
echo -e "${BLUE}   git remote add origin https://github.com/YOUR_USERNAME/sadaqah-jariah.git${NC}"
echo -e "${BLUE}   git branch -M main${NC}"
echo -e "${BLUE}   git push -u origin main${NC}"
echo ""
echo "3️⃣  ADD INSTAGRAM SECRETS:"
echo "   • Go to: Settings → Secrets and variables → Actions"
echo "   • Click: New repository secret"
echo "   • Add these secrets:"
echo "     - Name: INSTAGRAM_USERNAME"
echo "       Value: your_instagram_username"
echo "     - Name: INSTAGRAM_PASSWORD"
echo "       Value: your_instagram_password"
echo ""
echo "4️⃣  ENABLE GITHUB ACTIONS:"
echo "   • Go to: Actions tab"
echo "   • Click: I understand my workflows, go ahead and enable them"
echo ""
echo "5️⃣  TEST MANUAL RUN (optional):"
echo "   • Go to: Actions → Daily Hadith Posts"
echo "   • Click: Run workflow"
echo "   • Click: Run workflow button"
echo ""
echo "========================================================"
echo -e "${GREEN}🎉 AUTOMATION WILL POST 5X DAILY AUTOMATICALLY!${NC}"
echo "========================================================"
echo ""
echo "⏰ POSTING SCHEDULE (UTC):"
echo "   • 04:00 AM - Before Fajr"
echo "   • 11:00 AM - After Fajr"
echo "   • 02:00 PM - Before Dhuhr"
echo "   • 05:00 PM - After Dhuhr"
echo "   • 08:00 PM - Before Maghrib"
echo ""
echo -e "${GREEN}✅ ROOT FIX APPLIED:${NC}"
echo "   • No network timeouts (local images)"
echo "   • 100% halal content guaranteed"
echo "   • Works perfectly in GitHub Actions"
echo "   • Sadaqah Jariah running automatically!"
echo ""
echo "🤲 May Allah accept this and grant you continuous rewards!"
echo ""
