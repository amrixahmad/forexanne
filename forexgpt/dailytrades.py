from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sheetsauth import SheetsAuth
from dotenv import load_dotenv
import os

load_dotenv()
SCOPES=os.getenv("SCOPES")

sheetsAuth=SheetsAuth(scopes=SCOPES)
creds=sheetsAuth.get_credentials()
project_id="gtm-k4z6gpp-ngu2y"
range_name="Sheet1!A3"

ROADMAP_SPREADSHEET_ID = "1ML4O-1XEMR2OU-G_9JZ_nDo8LhmquILFImpX-pspBgI"

def update_values(creds,spreadsheet_id, range_name, value_input_option, _values):
  
  try:
    service = build("sheets", "v4", credentials=creds)
    values = _values
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


if __name__ == "__main__":
  # Pass: spreadsheet_id,  range_name, value_input_option and  _values
  _values=[["this is a test"]]
  update_values(
      creds,
      ROADMAP_SPREADSHEET_ID,
      range_name,
      "USER_ENTERED",
      _values,
  )