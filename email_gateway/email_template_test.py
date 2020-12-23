import sendgrid

sg = sendgrid.SendGridAPIClient('INSERT KEY')
data = {
  "personalizations": [
    {
      "to": [
        {
          "email":"norman@thusly.co"
        }
      ],
      "subject": "Sendgrid Test Email",
       "dynamic_template_data":{
            "first_name":"Norman"
          }
    }
  ],
  "from": {
    "email": "conormora@berkeley.edu"
  },
  "content": [
    {
      "type": "text/plain",
      "value": "Sending a test email!"
    }
  ],
  "template_id":"INSERT TEMPLATE ID"
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)
