import sendgrid
import os

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": "conormora@berkeley.edu"
        },
        {
            "email": "norman@thusly.co"
        },
        {
            "email": "sumana.nukala@berkeley.edu"
        }
      ],
      "subject": "Sendgrid Test Email"
    }
  ],
  "from": {
    "email": "publiceditor@goodlylabs.org"
  },
  "content": [
    {
      "type": "text/plain",
      "value": "Sending a test email"
    }
  ]
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)
