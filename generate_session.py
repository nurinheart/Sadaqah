import os
import json
from getpass import getpass
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired, TwoFactorRequired, ChallengeRequired, BadPassword
)

SESSION_FILE = "session.json"

def handle_challenge(cl: Client, username: str):
    """
    Handles the Instagram security challenge.
    """
    print(f"\n⚠️  Instagram security challenge required.")
    print(f"Please log in manually through the Instagram app on your phone/browser first.")
    print(f"Then run this script again.")
    return False

def generate_session():
    """
    Logs into Instagram and saves the session data to a JSON file.
    Handles 2FA and security challenges.
    """
    import time
    
    cl = Client()
    
    # Set delay to avoid rate limiting
    cl.delay_range = [2, 5]
    
    # Load existing session if available to reuse encryption keys
    if os.path.exists(SESSION_FILE):
        try:
            print("Loading existing session data to preserve encryption keys...")
            cl.load_settings(SESSION_FILE)
        except:
            pass
    
    username = input("Enter your Instagram username: ")
    password = getpass("Enter your Instagram password: ")
    
    # Add delay before login attempt
    print("Waiting 3 seconds before login attempt...")
    time.sleep(3)

    try:
        print("\nAttempting to log in...")
        cl.login(username, password)

    except TwoFactorRequired:
        print("\nTwo-Factor Authentication is required.")
        verification_code = input("Enter the 2FA code sent to your device: ")
        try:
            cl.login(username, password, verification_code=verification_code)
        except Exception as e:
            print(f"❌ 2FA login failed: {e}")
            import traceback
            traceback.print_exc()
            return

    except ChallengeRequired:
        if not handle_challenge(cl, username):
            return
            
    except BadPassword:
        print("\n❌ Incorrect password. Please double-check your password and try again.")
        return

    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return

    # Save the session
    try:
        cl.dump_settings(SESSION_FILE)
        print(f"\n✅ Success! Session saved to '{SESSION_FILE}'.")
        print("You can now copy the contents of this file into the INSTAGRAM_SESSION_DATA secret in your GitHub repository.")
    except Exception as e:
        print(f"❌ Failed to save session file: {e}")

if __name__ == "__main__":
    if os.path.exists(SESSION_FILE):
        overwrite = input(f"'{SESSION_FILE}' already exists. Do you want to overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            print("Aborted.")
            exit()
    
    generate_session()
