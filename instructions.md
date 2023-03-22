To create a Slack bot that reads lines from a Google Sheet and posts a message on a channel every day, you need to set up a Python script using the Slack and Google Sheets API. You will also need a scheduler like Heroku or cron jobs to run the script daily.

Prerequisites:

Create a Slack bot and obtain a Slack API token (SLACK_API_TOKEN).
Enable Google Sheets API for your project and obtain credentials JSON file (credentials.json).
Here's a Python script to achieve this:

```py
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
SHEET_ID = 'YOUR_GOOGLE_SHEET_ID'
RANGE_NAME = 'Sheet1!A1:B'  # Update according to your sheet range

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

        slack_channel = "#your-slack-channel"  # Update with your desired Slack channel
        post_message_to_slack(slack_channel, message)
    else:
        print("No data found.")

```

Replace YOUR_GOOGLE_SHEET_ID with your Google Sheet's ID and update the RANGE_NAME and slack_channel variables according to your needs.

To run this script daily, you can use a task scheduler like cron on Unix-based systems, or Task Scheduler on Windows. Alternatively, you can deploy your script on a platform like Heroku and use their scheduler add-on.



How to obtain 'SHEET_ID'

Look into the url of spredsheet and bring the value after '/d/'
Example:
    https://docs.google.com/spreadsheets/d/1torhO_gjLKIYcFHe7c7PVszn8kttI5pIcl_ZlUHs7tk/edit#gid=0

    'SHEET_ID' is 1torhO_gjLKIYcFHe7c7PVszn8kttI5pIcl_ZlUHs7tk



What credentials.json file should contain:

The credentials.json file should contain the credentials for accessing the Google Sheets API. Here's how you can obtain the credentials:

-Go to the Google Cloud Console and create a new project.
- Enable the Google Sheets API for your project.
- Create credentials for your project by clicking on "Create credentials" and selecting "Service account key".
-Fill out the form to create a new service account, selecting the role "Project" > "Editor" and choosing JSON as the key type.
- Download the JSON file containing your credentials, and save it as credentials.json in a secure location on your computer or server.

Make sure to keep the credentials.json file safe and secure, as it contains sensitive information that should not be shared with others. In the Python script, you can load the credentials using the service_account method of the gspread library, like this:

```py
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file('path/to/your/credentials.json')
gc = gspread.authorize(creds)
```


How to obtain 'SLACK_BOT_TOKEN'

To obtain the SLACK_BOT_TOKEN for your Slack bot, you will need to create a new Slack App and add a bot user to it. Here's how:

- Go to the Slack API website and click "Create New App".
- Give your app a name and select the workspace where you want to install it.
- Click "Bot Users" in the navigation menu and then click "Add a Bot User" to add a bot user to your app.
- Customize your bot user's display name and other settings as desired.
- Click "OAuth & Permissions" in the navigation menu and then click "Install App" to install your app to your workspace.
- Grant your app the necessary permissions to access the channels and conversations where you want to post messages.
- Copy the "Bot User OAuth Access Token" from the "OAuth & Permissions" page. This is the token that you will use to authenticate your bot in your code.

Once you have obtained the SLACK_BOT_TOKEN, you can store it as an environment variable in your script, like this:

```py
import os

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_BOT_TOKEN)
```

Note that you should keep your SLACK_BOT_TOKEN safe and secure, as it allows anyone who has it to authenticate with your Slack bot and post messages on your behalf.