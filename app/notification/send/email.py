import json
import os

from azure.communication.email import EmailClient

#ENV_FILE = find_dotenv()
#if ENV_FILE:
#    load_dotenv(ENV_FILE)


def notification(message):
    try:
        # Setup for the email client using the connection string from environment variables
        connection_string = os.getenv("EMAIL_CONNECTION_STRING")
        client = EmailClient.from_connection_string(connection_string)

        # Parse the incoming message JSON
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        receiver_address = message["username"]

        # Construct the mail message content
        mail_message = {
            "senderAddress": "DoNotReply@clipsify.net",
            "recipients": {
                "to": [{"address": receiver_address}],
            },
            "content": {
                "subject": "Test Email",
                "plainText": "Here is your Donwload ID:  " + mp3_fid,
            },
        }

        # Send the email
        poller = client.begin_send(mail_message)
        result = poller.result()
        print(result)

    except Exception as ex:
        print(ex)
