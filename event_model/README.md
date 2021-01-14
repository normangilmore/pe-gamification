# Steps 

1. Retrieving data
   - Run `pybossa_api/fill_db_data.py` to generate a CSV with the data to insert into our database
   - `fill_db_data.py` requires a list of project names and generates a CSV file with the following columns (added parentheses for clarification): 
   
      `id(taskrun),created(taskrun),project_id,task_id,user_id,finish_time(taskrun),task_type,project_name,name(user),email_addr(user),category,category_name`

      
2. Inserting the data
   - Run docker
   - Set the python path 
   `export PYTHONPATH=.`
   - Run `event_model/create_tables.py` (might have to drop the tables, then run this file again if you've previously ran it)
   - Run `event_model/insert_data.py`. This will add all taskrun information (the fields listed above), badge names from `badge_list.csv`, and email candidates. See `event_model/insert_data.py`, `event_model/insert_badges.py`, and `event_model/query_badge.py` for more information. 


