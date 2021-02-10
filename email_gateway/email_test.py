import sendgrid
import os
sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": "rubywerman@gmail.com"
        }
      ],
      "subject": "Sendgrid Test Email"
    }
  ],
  "from": {
    "email": "rubywerman@berkeley.edu"
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
