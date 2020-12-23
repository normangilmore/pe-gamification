import os
import requests

ZAPIER_WEBHOOK_URL = "INSERT WEBHOOK"
response = requests.post(ZAPIER_WEBHOOK_URL, json={"email": "emilyzeng@berkeley.edu", "first_name":"Emily", "message":"You won a badge for completing 25 tasks!"})
print(response.status_code)
