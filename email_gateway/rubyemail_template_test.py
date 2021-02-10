import sendgrid
import os

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
data = {
  "personalizations": [
    {
      "to": [
        {
          "email":email
        }
      ],
       "dynamic_template_data":{
            "first_name":first_name, 
            "task_name":task_name
          }
    }
  ],
  "from": {
    "email": "publiceditor@goodlylabs.org"
  },
  "template_id":"d-915ae8191de2421eaa16c43790719632"
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)
