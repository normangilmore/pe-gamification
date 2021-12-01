def dictmake(email, first_name, task_name, template_id): 
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
      "template_id":template_id
    }
    return data
