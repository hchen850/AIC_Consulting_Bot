from __future__ import annotations

from datetime import datetime
import gspread

from sheets_client import get_sheets_client, sheets_logging_enabled

def log_business_summary(collected: dict):
    """Appends a completed business intake summary to its own tab in the shared sheet."""
    if not sheets_logging_enabled():
        return
    try:
        client_sheets = get_sheets_client()
        sheet = client_sheets.open("BEACH_Global_Activity_Log")

        try:
            worksheet = sheet.worksheet("Business Summaries")
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Business Summaries", rows=1000, cols=10)
            worksheet.append_row(
                ["Timestamp", "Name", "Problem", "Stage", "Urgency", "Funding Status", "Team Size"]
            )

        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            collected.get("name", ""),
            collected.get("problem", ""),
            collected.get("stage", ""),
            collected.get("urgency", ""),
            collected.get("funding_status", ""),
            collected.get("team_size", ""),
        ]
        worksheet.append_row(row)
    except Exception as e:
        print(f"[INTERNAL LOG ERROR] Failed to log business summary: {e}")