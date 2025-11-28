"""
Alternative Session Generator - Uses existing Instagram login
This approach reuses your Instagram app session instead of creating a new one
"""

import os
import json

SESSION_FILE = "session.json"

def create_manual_session():
    """
    Creates a session file manually from Instagram app session data.
    This bypasses login issues and rate limiting.
    """
    print("=" * 60)
    print("MANUAL SESSION GENERATOR")
    print("=" * 60)
    print("\nThis tool helps you create a session.json from your Instagram app.")
    print("\nOption 1: If you already have session.json from NectarFromQuran:")
    print("  - Copy the session.json file from NectarFromQuran to this directory")
    print("  - It should work for both projects")
    print("\nOption 2: Generate new session using instagram_private_api:")
    print("  - Install: pip install instagram-private-api")
    print("  - Run the script below")
    
    print("\n" + "=" * 60)
    print("COPY THIS SCRIPT AND RUN IT:")
    print("=" * 60)
    
    script = '''
import json
from instagram_private_api import Client

username = input("Instagram username: ")
password = input("Instagram password: ")

api = Client(username, password)
settings = api.settings

# Convert to instagrapi format
session_data = {
    "uuids": settings.get("uuids", {}),
    "mid": settings.get("mid"),
    "ig_u_rur": settings.get("ig_u_rur"),
    "ig_www_claim": settings.get("ig_www_claim"),
    "authorization_data": {
        "ds_user_id": settings.get("ds_user_id"),
        "sessionid": settings.get("sessionid")
    },
    "cookies": settings.get("cookies", {}),
    "last_login": settings.get("last_login"),
    "device_settings": settings.get("device_settings", {}),
    "user_agent": settings.get("user_agent"),
    "country": settings.get("country", "US"),
    "country_code": settings.get("country_code", 1),
    "locale": settings.get("locale", "en_US"),
    "timezone_offset": settings.get("timezone_offset", -14400)
}

with open("session.json", "w") as f:
    json.dump(session_data, f, indent=4)

print("✅ Session saved to session.json")
'''
    
    print(script)
    print("=" * 60)
    
    print("\nOption 3: Wait 24 hours and try generate_session.py again")
    print("  - Instagram has rate limited your IP")
    print("  - Try from a different network (mobile hotspot)")
    
    print("\n" + "=" * 60)
    print("QUICK FIX - Use environment variables directly:")
    print("=" * 60)
    print("\nInstead of session data, you can just use username/password:")
    print("1. Set these in GitHub Secrets:")
    print("   - INSTAGRAM_USERNAME")
    print("   - INSTAGRAM_PASSWORD")
    print("2. Remove INSTAGRAM_SESSION_DATA secret (or leave it empty)")
    print("3. The code will login fresh each time")
    print("\nNote: This works but may trigger Instagram security checks more often")

if __name__ == "__main__":
    create_manual_session()
