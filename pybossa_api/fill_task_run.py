
from get_people import get_ids
import requests
import json
import os
import csv

PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}

def fill_taskrun(user_ids, project_ids):
    '''
    Input: taskrun_dict dictionary (user id: task values)
    Output: csv file with taskrun id, timestamp, project id, task id,
    and user id
    '''
    task_dict = {}
    for project_id in project_ids:
        r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                         '&project_id={}&orderby=id&limit=100'
                         .format(PYBOSSA_API_KEY, project_id),
                         headers=headers)
        task_runs = json.loads(r.text)
        index = 0
        for task_run in task_runs:
            index += 1
            task_dict[index] = [task_run['id'], task_run['created'],
            task_run['project_id'], task_run['task_id'], task_run['user_id'],
            task_run['finish_time'], task_run['info']]
    with open('task_run.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "created", "project_id", "task_id",
        "user_id", "finish_time", 'info'])
        for i in task_dict:
            writer.writerow([task_dict[i][0], task_dict[i][1], 
                task_dict[i][2], task_dict[i][3], task_dict[i][4],
                task_dict[i][5]])


if __name__ == '__main__':
    project_names = ['Covid2_FormTriage', 'Covid2_SemanticsTriage']
    project_ids = ['253', '254']
    user_ids = get_ids(project_ids)
    taskrun_ids = fill_taskrun(user_ids, project_ids)
    print(taskrun_ids)



