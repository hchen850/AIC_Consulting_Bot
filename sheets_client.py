from __future__ import annotations

import os
import json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]


def sheets_logging_enabled() -> bool:
    return os.environ.get("SHEETS_LOGGING_ENABLED", "false").lower() == "true"


def get_credentials():
    raw = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if raw:
        info = json.loads(raw)
        return Credentials.from_service_account_info(info, scopes=SCOPES)
    return Credentials.from_service_account_file("credentials.json", scopes=SCOPES)


def get_sheets_client():
    creds = get_credentials()
    return gspread.authorize(creds)