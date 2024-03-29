import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os

load_dotenv()

# The ID and range of a sample spreadsheet.
ROADMAP_SPREADSHEET_ID = "1ML4O-1XEMR2OU-G_9JZ_nDo8LhmquILFImpX-pspBgI"
SAMPLE_RANGE_NAME = "Sheet1!A1:D1"

SCOPES=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

class SheetsAuth:
  def __init__(self,scopes) -> None:  
    self.scopes=scopes
    self.ROADMAP_SPREADSHEET_ID=ROADMAP_SPREADSHEET_ID
    self.SAMPLE_RANGE_NAME=SAMPLE_RANGE_NAME

  def get_credentials(self):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("forexgpt/gdrive/token.json"):
      return Credentials.from_authorized_user_file("forexgpt/gdrive/token.json", self.scopes)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "forexgpt/gdrive/credentials.json", self.scopes
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("forexgpt/gdrive/token.json", "w") as token:
        token.write(creds.to_json())
    
  def authorize(self):
    if os.path.exists("forexgpt/gdrive/token.json"):
      return Credentials.from_authorized_user_file("forexgpt/gdrive/token.json", self.scopes)

def main():
  sheetAuth=SheetsAuth(scopes=SCOPES)
  sheetAuth.get_credentials()
  try:
      service = build("sheets", "v4", credentials=sheetAuth.authorize())

      # Call the Sheets API
      sheet = service.spreadsheets()
      result = (
          sheet.values()
          .get(spreadsheetId=ROADMAP_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
          .execute()
      )
      values = result.get("values", [])

      if not values:
        print("No data found.")
        return

      print("Name, Major:")
      for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        # print(f"{row[0]}, {row[4]}")
        print(row)

  except HttpError as err:
    print(err)


if __name__ == "__main__":
  # creds=SheetsAuth(scopes=SCOPES).get_credentials()
  # main()
  # print(get_scopes())
  # print(os.path.abspath(os.getcwd()))
  pass
  