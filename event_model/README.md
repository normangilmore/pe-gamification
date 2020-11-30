# Steps 

### 1. Getting the data
   - Run `event_model/fill_db_data.py` to generate a CSV with the data to insert into our database

### 2. Inserting the data
   - Run docker
   - Set the python path 
   `export PYTHONPATH=.`
   - Run `event_model/create_tables.py` (might have to drop the tables, then run this file again if you've previously ran it)
   - Run `event_model/insert_data.py`

### 3. Querying data 
