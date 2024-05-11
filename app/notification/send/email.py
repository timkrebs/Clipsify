import json
import os
from azure.communication.email import EmailClient

def notification(message):
    try:
        # Setup for the email client using the connection string from environment variables
        connection_string = os.getenv("EMAIL_CONNECTION_STRING")
        client = EmailClient.from_connection_string(connection_string)

        # Parse the incoming message JSON
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        receiver_address = message["username"]

        html_content = f"""
        <html>
          <head>
            <style type="text/css">
              .ExternalClass, .ExternalClass div, .ExternalClass font, .ExternalClass p, .ExternalClass span, .ExternalClass td, img {{line-height: 100%;}}
              #outlook a {{padding: 0;}}
              .ExternalClass, .ReadMsgBody {{width: 100%;}}
              a, blockquote, body, li, p, table, td {{-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;}}
              table, td {{mso-table-lspace: 0; mso-table-rspace: 0;}}
              img {{-ms-interpolation-mode: bicubic; border: 0; height: auto; outline: 0; text-decoration: none;}}
              table {{border-collapse: collapse !important;}}
              #bodyCell, #bodyTable, body {{height: 100% !important; margin: 0; padding: 0; font-family: ProximaNova, sans-serif;}}
              #bodyCell {{padding: 20px;}}
              #bodyTable {{width: 600px;}}
              /* Additional Styles for FID */
              .fid-highlight {{
                font-weight: bold;
                background-color: #f2f2f2; /* Light grey background */
                padding: 10px;
                border-radius: 5px;
                display: inline-block;
              }}
            </style>
          </head>
          <body>
            <center>
              <table style='width: 600px; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin: 0; padding: 0; font-family: "ProximaNova", sans-serif; border-collapse: collapse !important; height: 100% !important;' align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
                <tr>
                  <td align="center" valign="top" id="bodyCell" style='-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin: 0; padding: 20px; font-family: "ProximaNova", sans-serif; height: 100% !important;'>
                    <div class="main">
                      <p style="text-align: center; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; margin-bottom: 30px;">
                        <img src="https://cdn.auth0.com/styleguide/2.0.9/lib/logos/img/badge.png" width="50" alt="Your logo goes here" style="-ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none;">
                      </p>
                      <h1>Welcome to Clipsify!</h1>
                      <p>Here is your Download ID: <span class="fid-highlight">{{mp3_fid}}</span>. Please click the following link to download your file:</p>
                      <p><a href="http://clipsify.net/download?fid={{mp3_fid}}">Download MP3</a></p>
                      <br />
                      Thanks!
                      <br />
                      <strong>Clipsify Team</strong>
                    </div>
                  </td>
                </tr>
              </table>
            </center>
          </body>
        </html>
        """

        mail_message = {
            "senderAddress": "DoNotReply@clipsify.net",
            "recipients": {
                "to": [{"address": receiver_address}],
            },
            "content": {
                "subject": "Your MP3 Conversion is Ready!",
                "html": html_content,
            },
        }

        # Send the email
        poller = client.begin_send(mail_message)
        result = poller.result()
        print(result)

    except Exception as ex:
        print(ex)

