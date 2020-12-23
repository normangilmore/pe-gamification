from get_people import get_ids
import requests
import json
import os
import csv

PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}


def fill_task(project_ids, write=True):
    """
    Input: user_ids dictionary (user ids: task values)
    Output: csv file with user id, name, email
    """
    tasks = {}
    for project_id in project_ids:
        r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                         '&project_id={}&orderby=id&limit=100'
                         .format(PYBOSSA_API_KEY, project_id),
                         headers=headers)
        task_runs = json.loads(r.text)
        for tr in task_runs:
            if str(tr['task_id']) not in tasks:
                tasks[str(tr['task_id'])] = {'project_id': tr['project_id'], 'state':None, 'info':tr['info']}
    if write:
        with open('task.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["id", "project_id", "state", "info"])
            for t_id in tasks:
                writer.writerow([t_id, tasks[t_id]['project_id'], tasks[t_id]['state'], tasks[t_id]['info']])
    return tr


if __name__ == '__main__':
    project_names = ['Covid2_FormTriage', 'Covid2_SemanticsTriage']
    project_ids = ['253', '254']
    emails = fill_task(project_ids, True)
    print(emails)
    #print(emails)
