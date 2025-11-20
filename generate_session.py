import os
from instagrapi import Client
from getpass import getpass
import json

# --- This script generates a session file for Instagram ---

SESSION_FILE = "session.json"

def generate_session():
    """
    Logs into Instagram and saves the session data to a JSON file.
    """
    cl = Client()
    
    username = input("Enter your Instagram username: ")
    password = getpass("Enter your Instagram password: ")
    
    # Instagrapi will prompt for 2FA if it's enabled
    verification_code = input("Enter 2FA code if you have it, otherwise press Enter: ")

    try:
        if verification_code:
            cl.login(username, password, verification_code=verification_code)
        else:
            cl.login(username, password)
        
        # Save the session settings to a file
        cl.dump_settings(SESSION_FILE)
        
        print(f"\n✅ Success! Session saved to '{SESSION_FILE}'.")
        print("Please follow the next steps in the guide to copy this file's content into a GitHub Secret.")

    except Exception as e:
        print(f"\n❌ An error occurred during login: {e}")
        print("Please check your credentials and try again.")

if __name__ == "__main__":
    generate_session()
