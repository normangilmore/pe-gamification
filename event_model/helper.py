def getFirstName(first_name): 
  # Lazy fix to parse first name from string of full name (in future, use "nickname" category to address users in emails)
  return first_name.split()[0].capitalize() 

def dictmaker(email, first_name, task_name, template_id): 
    data = {
      "personalizations": [
        {
          "to": [
            {
              "email":email
            }
          ],
           "dynamic_template_data":{
                "first_name":getFirstName(first_name), 
                "task_name":task_name
              }
        }
      ],
      "from": {
        "email": "publiceditor@goodlylabs.org"
      },
      "template_id":template_id
    }
    return data

