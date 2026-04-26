import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def test_google_sheets_connection():
    print("⏳ Step 1: Loading credentials...")
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        # Make sure credentials.json is in the exact same folder as this script
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)
        print("✅ Credentials loaded successfully!")
    except FileNotFoundError:
        print("❌ ERROR: Could not find 'credentials.json'. Is it in this folder?")
        return
    except Exception as e:
        print(f"❌ ERROR loading credentials: {e}")
        return

    print("⏳ Step 2: Looking for the Google Sheet...")
    sheet_name = "BEACH_Global_Activity_Log"
    try:
        sheet = client.open(sheet_name).sheet1
        print(f"✅ Found spreadsheet: '{sheet_name}'")
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ ERROR: Could not find a sheet named '{sheet_name}'.")
        print("   -> Fix: Did you share the Google Sheet with the email address inside your credentials.json file?")
        return
    except Exception as e:
        print(f"❌ ERROR opening sheet: {e}")
        return

    print("⏳ Step 3: Attempting to write test data...")
    try:
        test_row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "TEST_PROJECT",
            "TEST_CATEGORY",
            "This is a test to see if the API works.",
            "Test Rationale",
            "100%"
        ]
        sheet.append_row(test_row)
        print("🎉 SUCCESS! Check your Google Sheet, a new row should be there.")
    except Exception as e:
        print(f"❌ ERROR writing to sheet: {e}")

if __name__ == "__main__":
    test_google_sheets_connection()