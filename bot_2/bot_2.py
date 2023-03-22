import os
import gspread
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Authenticate with Google Sheets API
gc = gspread.service_account(filename='path/to/your/credentials.json')
sheet = gc.open('Name of your Google Sheet').sheet1

# Authenticate with Slack API
client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))

# Read the data from the Google Sheet
data = sheet.get_all_values()

# Post the message to the Slack channel
try:
    response = client.chat_postMessage(
        channel='#status',
        text='\n'.join([' | '.join(row) for row in data])
    )
    print('Message posted: {}'.format(response['ts']))
except SlackApiError as e:
    print('Error posting message: {}'.format(e))