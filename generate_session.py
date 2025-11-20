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
    challenge_path = cl.challenge_get_path(username)
    if not challenge_path:
        print("Could not find a challenge path. Please try again.")
        return False

    print(f"Instagram has sent a security challenge. Please choose a verification method:")
    print(f"1: SMS")
    print(f"2: Email")
    
    choice = input("Enter your choice (1 or 2): ")
    if choice not in ["1", "2"]:
        print("Invalid choice.")
        return False

    try:
        cl.challenge_select_path(challenge_path, int(choice))
        code = input("Enter the 6-digit code you received: ")
        cl.challenge_send_code(challenge_path, code)
        cl.challenge_relogin(challenge_path)
        print("✅ Challenge passed successfully.")
        return True
    except Exception as e:
        print(f"❌ An error occurred during the challenge: {e}")
        return False

def generate_session():
    """
    Logs into Instagram and saves the session data to a JSON file.
    Handles 2FA and security challenges.
    """
    cl = Client()
    username = input("Enter your Instagram username: ")
    password = getpass("Enter your Instagram password: ")

    try:
        print("\nAttempting to log in...")
        cl.login(username, password)

    except TwoFactorRequired:
        print("\nTwo-Factor Authentication is required.")
        verification_code = input("Enter the 2FA code sent to your device: ")
        try:
            cl.two_factor_login(verification_code)
        except Exception as e:
            print(f"❌ 2FA login failed: {e}")
            return

    except ChallengeRequired:
        if not handle_challenge(cl, username):
            return
            
    except BadPassword:
        print("\n❌ Incorrect password. Please double-check your password and try again.")
        return

    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
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
