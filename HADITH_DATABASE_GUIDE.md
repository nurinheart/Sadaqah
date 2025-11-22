# Hadith Database - Quick Reference Guide

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                   HADITH POSTING WORKFLOW                    │
└─────────────────────────────────────────────────────────────┘

1. CDN API (jsdelivr.net)
   ├── Contains 6 major hadith collections
   ├── Bukhari, Muslim, Tirmidhi, Abu Dawud, Nasai, Ibn Majah
   └── Free, no authentication needed
         ↓
2. hadith_api.py (API Client)
   ├── Fetches hadiths from CDN
   ├── Verifies Sahih grade
   └── Filters out incomplete hadiths
         ↓
3. fetch_authentic_hadiths.py (Database Generator)
   ├── Curated list of 50 hadith references
   ├── Fetches each one from API
   └── Saves 43 verified Sahih hadiths
         ↓
4. verified_hadiths.json (Database File)
   ├── 43 authentic hadiths
   ├── Full text with narrators
   └── Metadata (grade, collection, category)
         ↓
5. hadith_data.py (Loader)
   ├── Loads from verified_hadiths.json
   ├── Transforms to compatible format
   └── Provides get_sahih_hadiths() API
         ↓
6. create_post.py (Post Generator)
   ├── Gets hadith from database
   ├── Generates Instagram carousel
   └── Archives to GitHub
         ↓
7. GitHub Actions (Automation)
   ├── Runs 5x daily at prayer times
   ├── Auto-posts to Instagram
   └── Archives slides + metadata
```

## 📁 Key Files

### `hadith_api.py`
**Purpose**: API client for fetching hadiths
**Key Functions**:
- `HadithAPIClient()` - Main client class
- `fetch_hadith(collection, number)` - Get single hadith
- `fetch_collection_metadata(collection)` - Get collection info
- `verify_hadith_sahih(hadith)` - Check if Sahih
- `get_random_sahih_hadith(collection)` - Random selection

### `fetch_authentic_hadiths.py`
**Purpose**: Generate verified hadith database
**Usage**:
```bash
# Create/refresh database
python3 fetch_authentic_hadiths.py --refresh

# Check existing database
python3 fetch_authentic_hadiths.py
```

### `verified_hadiths.json`
**Purpose**: Verified Sahih hadith database
**Format**:
```json
{
  "metadata": {
    "created_at": "2024-11-23T...",
    "total_hadiths": 43,
    "source": "cdn.jsdelivr.net",
    "verification": "All Sahih",
    "collections": ["bukhari", "muslim", ...]
  },
  "hadiths": [
    {
      "text": "Full hadith text...",
      "reference": "Sahih al-Bukhari 1",
      "grade": "Sahih",
      "collection": "bukhari",
      "hadith_number": 1,
      "category": "Intention",
      "chapter": "...",
      "narrator": "...",
      "source": "cdn.jsdelivr.net"
    },
    ...
  ]
}
```

### `hadith_data.py`
**Purpose**: Load hadiths into application
**Key Functions**:
- `load_verified_hadiths()` - Load from JSON
- `get_sahih_hadiths()` - Get all hadiths (app API)
- `validate_hadith_authenticity(hadith)` - Verify
- `get_hadith_stats()` - Get statistics
- `HADITHS` - Global list for imports

## 🔧 Common Tasks

### Add More Hadiths
1. Edit `hadith_api.py` line ~240:
```python
hadith_references = [
    # Add new references here
    ('bukhari', 123, 'Category'),
    ...
]
```

2. Refresh database:
```bash
python3 fetch_authentic_hadiths.py --refresh
```

### Check Database Stats
```bash
python3 hadith_data.py
```

### Test API Directly
```bash
python3 hadith_api.py
```

### Generate Test Post
```bash
python3 create_post.py
```

## 🐛 Troubleshooting

### "⚠️ verified_hadiths.json not found"
**Solution**: Run `python3 fetch_authentic_hadiths.py --refresh`

### "❌ Failed to fetch hadith"
**Causes**:
- Network issue
- Invalid hadith number
- CDN down
**Solution**: Check network, verify hadith number exists

### "❌ NOT SAHIH - Skipped"
**Normal**: Not all hadiths in collections are Sahih grade
**Action**: The API automatically filters these out

### "⚠️ Hadith text too short"
**Cause**: Incomplete/empty hadith in CDN
**Action**: Replace with different hadith number

## 📊 Current Database Stats

- **Total**: 43 Sahih hadiths
- **Bukhari**: 12 (all Sahih)
- **Muslim**: 14 (all Sahih)
- **Tirmidhi**: 6 (Sahih-verified)
- **Abu Dawud**: 4 (Sahih-verified)
- **Nasai**: 3 (Sahih-verified)
- **Ibn Majah**: 4 (Sahih-verified)

## ✅ Verification Points

Every hadith in the database is:
1. ✅ Fetched from authenticated CDN API
2. ✅ Verified as Sahih (authentic) grade
3. ✅ Full text with NO summarization
4. ✅ Includes narrator chain where available
5. ✅ Minimum 50 characters length
6. ✅ Cross-referenced from major collections

## 🚀 GitHub Actions Integration

The workflow automatically:
1. Uses `verified_hadiths.json` (committed to repo)
2. Calls `create_post.py --post` to generate + post
3. Archives slides to `archive/{collection}/{hadith_number}/`
4. Commits changes back to repo

**No manual intervention needed** - runs 5x daily at prayer times.

## 💡 Best Practices

1. **Always verify Sahih grade** - Never post unverified hadiths
2. **No modification** - Use raw text as fetched from API
3. **Balanced rotation** - Include all 6 major collections
4. **Regular updates** - Refresh database monthly to add variety
5. **Test locally first** - Use `create_post.py` before auto-posting
6. **Archive everything** - Keep slides + metadata in GitHub

## 📚 Resources

- **CDN API**: https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1
- **Hadith Collections**: 
  - Sahih al-Bukhari (entirely Sahih)
  - Sahih Muslim (entirely Sahih)
  - Jami' at-Tirmidhi (mixed grades)
  - Sunan Abi Dawud (mixed grades)
  - Sunan an-Nasa'i (mixed grades)
  - Sunan Ibn Majah (mixed grades)

---

**Last Updated**: November 23, 2024
**Status**: ✅ Production Ready
