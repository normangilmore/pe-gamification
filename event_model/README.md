# Steps 

1. Getting the data
   - Run `event_model/fill_db_data.py` to generate a CSV with the data to insert into our database
   - `fill_db_data.py` requires a list of project names and generaters a CSV file with the following columns (added parentheses for clarification): 
      
      `id(taskrun),created(taskrun),project_id,task_id,user_id,finish_time(taskrun),task_type,project_name,name(user),email_addr(user)`

      
2. Inserting the data
   - Run docker
   - Set the python path 
   `export PYTHONPATH=.`
   - Run `event_model/create_tables.py` (might have to drop the tables, then run this file again if you've previously ran it)
   - Run `event_model/insert_data.py`

3. Querying data 
