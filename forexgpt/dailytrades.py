from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseUpload
from sheetsauth import SheetsAuth,SCOPES
from dotenv import load_dotenv
import os
import requests
from io import BytesIO
from datetime import datetime
import pytz

load_dotenv()

ROADMAP_SPREADSHEET_ID="1ML4O-1XEMR2OU-G_9JZ_nDo8LhmquILFImpX-pspBgI"
ROADMAP_FOLDER_ID="1xB1hOkmQJ7pD__P4r7e7cC4fFfw9QH3i"
ROADMAP_DAILY_SUBMISSIONS_FOLDER_ID="1HGKuTxHK8Wn7MTKonoRCNRVBPoWI4VvQ"

channel_ids=[
        {"name":"student_trade_ideas_id","value":1197471105162694666},
        {"name":"trade_results_id","value":1203935782230822942},
        # {"name":"scalping_coach_id","value":1199171759392444547},
        {"name":"amri_test_id","value":1202207157198524486},
        {"name":"semester_1_id","value":1197470569399074826},
        {"name":"semester_2_id","value":1197470654816063538},
        {"name":"semester_3_id","value":1197470685908447262},
        {"name":"semester_4_id","value":1197470758243418113},
        {"name":"semester_5_id","value":1197470798856859738},
        {"name":"semester_6_id","value":1197470840011358288}]

class DailyTrades:
  def __init__(self,creds) -> None:
    self.creds=creds
    self.project_id="gtm-k4z6gpp-ngu2y"

  def add_student_roadmap_row(self,author,channel_id,channel_name,file_id,link,journal_entry):
    range_name = 'Sheet1!A:E'
    current_time = datetime.now(pytz.utc).astimezone(pytz.timezone('Asia/Singapore'))  # Asia/Singapore is one of the time zones in GMT+8
    time_of_upload = current_time.strftime('%H:%M:%S')
    date_of_upload = current_time.strftime('%Y-%m-%d')
    try:
      service = build("sheets", "v4", credentials=self.creds)
      values = [
                  [
                      str(author),  # Username
                      time_of_upload,  # Time of Upload
                      date_of_upload,  # Date of Upload
                      channel_id,
                      channel_name,
                      file_id,
                      link,  # Link to the uploaded file
                      journal_entry
                  ]
              ]
      body = {"values": values}
      result = (
          service.spreadsheets()
          .values()
          .append(
              spreadsheetId=ROADMAP_SPREADSHEET_ID,
              range=range_name,
              valueInputOption='USER_ENTERED',
              body=body,
          )
          .execute()
      )
      print(f"{result.get('updatedCells')} cells updated.")
      return result
    except HttpError as error:
      print(f"An error occurred: {error}")
      return error

  def create_new_roadmap_folder(self):
    try:
      # create drive api client
      service = build("drive", "v3", credentials=self.creds)
      file_metadata = {
          "name": "Roadmap Students Daily Submissions",
          "mimeType": "application/vnd.google-apps.folder",
          "parents": [ROADMAP_FOLDER_ID]
      }

      # pylint: disable=maybe-no-member
      file = service.files().create(body=file_metadata, fields="id").execute()
      print(f'Folder ID: "{file.get("id")}".')
      return file.get("id")

    except HttpError as error:
      print(f"An error occurred: {error}")
      return None
  
  def upload_image_from_url(self,img_url):
    response=requests.get(img_url)

    if response.status_code==200:
      img_content = BytesIO(response.content)
      img_filename=os.path.basename(img_url)
      # Define file metadata (including the parent folder)
      service = build("drive", "v3", credentials=self.creds)
      file_metadata = {
          'name': img_filename,
          'parents': [ROADMAP_DAILY_SUBMISSIONS_FOLDER_ID]
      }
      # Create a media upload object for the image
      media = MediaIoBaseUpload(img_content, mimetype='image/jpeg', resumable=True)
      # Upload the image
      file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
      print(f"File ID: {file.get('id')}")
      print(f"Weblink: {file.get('webViewLink')}")
      return file.get('id'), file.get('webViewLink')

    else:
      print("Failed to download the image")
      return None,None

  def upload_student_trade_image(self,file_path):
    service = build("drive", "v3", credentials=self.creds)

    # file_path = os.getcwd()+"/forexgpt/The Thriving Introvert Facebook Ad.jpeg"
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [ROADMAP_DAILY_SUBMISSIONS_FOLDER_ID]
    }
    media = MediaFileUpload(file_path, mimetype='image/jpeg') # Adjust the mimetype if necessary
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    return file.get('id')
  
  def get_shareable_link(self,file_id):
    # Make the file publicly accessible
    service=build("drive", "v3", credentials=self.creds)

    service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'},
        fields='id'
    ).execute()
    
    # Get the shareable link
    file = service.files().get(fileId=file_id, fields='webViewLink').execute()
    return file.get('webViewLink')

if __name__ == "__main__":
  test_file_id="1oTm4UMhswl8Jo-wKT4PJlnwWuR3p1mhO"
  sheetsAuth=SheetsAuth(scopes=SCOPES)
  creds=sheetsAuth.authorize()
  img_url="https://cdn.discordapp.com/attachments/1199171759392444547/1213836725458313286/The_Thriving_Introvert_Facebook_Ad.jpeg"
  
  updates=DailyTrades(creds=creds)
  # updates.upload_student_trade_image()
  print(updates.get_shareable_link(test_file_id))
  # updates.upload_image_from_url(img_url)