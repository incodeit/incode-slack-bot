import os
import json
import httplib2
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors, discovery
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SHEET_ID = '1torhO_gjLKIYcFHe7c7PVszn8kttI5pIcl_ZlUHs7tk'
RANGE_NAME = 'Foglio1!A1:B3'  # Update according to your sheet range

def get_google_sheets_credentials():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds = google.oauth2.credentials.Credentials.from_authorized_user_info(info=json.load(token))

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def read_data_from_google_sheet(sheet_id, range_name):
    creds = get_google_sheets_credentials()
    service = discovery.build('sheets', 'v4', credentials=creds)

    try:
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()
        rows = result.get('values', [])
        return rows
    except errors.HttpError as error:
        print(f"An error occurred: {error}")
        return None

def post_message_to_slack(channel, text):
    slack_token = os.environ["SLACK_API_TOKEN"]
    client = WebClient(token=slack_token)
    try:
        response = client.chat_postMessage(channel=channel, text=text)
        print(f"Message posted: {text}")
    except SlackApiError as e:
        print(f"Error posting message: {e}")

if __name__ == '__main__':
    sheet_data = read_data_from_google_sheet(SHEET_ID, RANGE_NAME)
    if sheet_data:
        message = "Daily update:\n"
        for row in sheet_data:
            message += f"{row[0]}: {row[1]}\n"

        slack_channel = "#status"  # Update with your desired Slack channel
        post_message_to_slack(slack_channel, message)
    else:
        print("No data found.")
