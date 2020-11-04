import requests
import json
import os
import csv

PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}

def get_ids(project_ids, months=None):
    """
    Input: List of project IDs, (optional) a list of months formatted 'YYYY-MM'
    Output: Dictionary of (key) user_ids and (value) the amount of tasks
    they've completed for the given projects
    """
    user_ids = {}
    if months:
        for m in months:
            for project_id in project_ids:
                r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                                 '&project_id={}&created={}&all=1&orderby=id&limit=100'
                                 .format(PYBOSSA_API_KEY, project_id, m),
                                 headers=headers)
                task_runs = json.loads(r.text)
                # For each task, either add the user id or incremement the id's count
                for task in task_runs:
                    if str(task['user_id']) in user_ids:
                        user_ids[str(task['user_id'])] += 1
                    else:
                        user_ids[str(task['user_id'])] = 1
    else:
        for project_id in project_ids:
            r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                         '&project_id={}&orderby=id&limit=100'
                         .format(PYBOSSA_API_KEY, project_id),
                             headers=headers)
            task_runs = json.loads(r.text)
            # For each task, either add the user id or incremement the id's count
            for task in task_runs:
                if str(task['user_id']) in user_ids:
                    user_ids[str(task['user_id'])] += 1
                else:
                    user_ids[str(task['user_id'])] = 1
    return user_ids



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
            task_dict[index] = [task_run['id'], task_run['created'], task_run['project_id'], task_run['task_id'],
            task_run['user_id'], task_run['finish_time'], task_run['info']]
    with open('task_run.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "created", "project_id", "task_id", "user_id", "finish_time", 'info'])
        for i in task_dict:
            writer.writerow([task_dict[i][0], task_dict[i][1], task_dict[i][2], task_dict[i][3], task_dict[i][4], task_dict[i][5]])



if __name__ == '__main__':
    project_names = ['Covid2_FormTriage', 'Covid2_SemanticsTriage']
    project_ids = ['253', '254']
    user_ids = get_ids(project_ids)
    taskrun_ids = fill_taskrun(user_ids, project_ids)
    print(taskrun_ids)



