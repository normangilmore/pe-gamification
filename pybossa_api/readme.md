### fill_db_data.py
Generates a CSV of taskruns 

### trainingupdates.py
The purpose of trainingupdates.py is to take in a list of projects (such as the training projects) and generate a CSV file for each project that contains which users did tasks in the project, their email, and how many tasks they completed.

In `__main__`, specify what projects you want to generate tasks for in `project_names`. Next, run `python3 trainingupdates.py`. The resulting CSV files will be in `pe-gamification/pybossa_api/trainingupdates_output`.


