To create a Slack bot that reads lines from a Google Sheet and posts a message on a channel every day, you can follow these steps:

- Create a Google Sheet and add the data that you want to post on your Slack channel. Make sure that you have set the sharing settings to allow access to the sheet.
- Create a new Slack App in your workspace by going to the Slack API website and clicking "Create New App".
- Under "Bot Users", click "Add a Bot User" to create a new bot user for your app.
- Install your app to your workspace by clicking "Install App" and granting it the necessary permissions.
- Copy the "Bot User OAuth Access Token" from your app's "OAuth & Permissions" page. You will need this token to authenticate your bot in your code.
- In your preferred programming language, write a script that uses the Google Sheets API to read the data from your Google Sheet and the Slack API to post a message to your desired channel. You can use a scheduler like Cron to run your script every day at a specific time.
- Test your script to make sure it is working as expected.
- Deploy your script to a cloud-based platform or a server that is always running, so that your script can run every day without interruption.
Here's an example script in Python using the gspread and slack-sdk libraries:

```py
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
        channel='#your-channel-name',
        text='\n'.join([' | '.join(row) for row in data])
    )
    print('Message posted: {}'.format(response['ts']))
except SlackApiError as e:
    print('Error posting message: {}'.format(e))

```

Note that this is just a sample script and will need to be customized based on your specific needs. Additionally, you will need to set up environment variables to store your Google Sheets API credentials and your Slack Bot User OAuth Access Token.



what credentials.json file should contain:

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