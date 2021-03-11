from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from event_model.base import Base
from event_model.helper import dictmaker

# Tables in Gamify Model
from event_model.task_run import TaskRun
from event_model.task import Task
from event_model.project import Project
from event_model.user import User
from event_model.badge import Badge
from event_model.email_candidate import EmailCandidate
from python_http_client import exceptions

import sendgrid
import os
import json

def send_emails():
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))

    engine = create_engine(
      "postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard",
      echo=True,
      )
    Session = sessionmaker(bind=engine)
    session = Session()
    # Query emails that haven't been sent yet
    query_1 = session.query(EmailCandidate).filter(EmailCandidate.sent == "False").all()
    for row in query_1:
      #data = row.sendgrid_info
      data = {
        "personalizations": [
          {
            "to": [
              {
                #"email": row.sendgrid_info['personalizations'][0]['to'][0]['email']
                "email": "pe.test.db@gmail.com" # Send to my test email when testing
              }
            ],
             "dynamic_template_data":{
                  "first_name": row.sendgrid_info['personalizations'][0]['dynamic_template_data']['first_name'], 
                  "task_name": row.sendgrid_info['personalizations'][0]['dynamic_template_data']['task_name']
                }
          }
        ],
        "from": {
          "email": row.sendgrid_info['from']['email']
        },
        "template_id": row.sendgrid_info['template_id']
      }
      try:
        response = sg.client.mail.send.post(request_body=data)
        print("Email sent to: ", row.to_username)
      except exceptions.BadRequestsError as e:
        print(e.body)
        exit()
      except exceptions.ForbiddenError as e:
        print(e.body)
        exit()
      except exceptions.UnauthorizedError as e:
        print(e.body)
        exit()
      
      # Update "sent" field to True so we don't resend emails
      #session.query(EmailCandidate).filter(EmailCandidate.sent == "False").update({EmailCandidate.sent: "True"})
      #session.commit() # Uncomment this line when you're ready to send
    session.close()



if __name__ == "__main__":
    send_emails()
