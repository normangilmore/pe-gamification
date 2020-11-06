import requests
import json
import os
import csv
from get_people import get_projectIDs

PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}


def fill_taskrun(project_ids, write=True):
    '''
    Input: List of project_ids
    Output: csv file with taskrun info
    '''
    task_dict = {}
    for project_id in project_ids:
        r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                         '&project_id={}&orderby=id&limit=100'
                         .format(PYBOSSA_API_KEY, project_id),
                         headers=headers)
        task_runs = json.loads(r.text)
        print(len(task_runs))
        last = len(task_runs) - 1
        for i in range(len(task_runs)):
            task_run = task_runs[i]
            task_dict[task_run['id']] = [task_run['created'],
                                         task_run['project_id'],
                                         task_run['task_id'],
                                         task_run['user_id'],
                                         task_run['finish_time'],
                                         task_run['info']]
            if i == last:
                lastID = task_run['id']
        # Since we can only retrieve 100 tasks at a time...
        while len(task_runs) == 100:
            r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                             '&project_id={}&last_id={}&orderby=id&limit=100'
                             .format(PYBOSSA_API_KEY, project_id, lastID),
                             headers=headers)
            task_runs = json.loads(r.text)
            print(len(task_runs))
            last = len(task_runs) - 1
            for i in range(len(task_runs)):
                task_run = task_runs[i]
                task_dict[task_run['id']] = [task_run['created'],
                                             task_run['project_id'],
                                             task_run['task_id'],
                                             task_run['user_id'],
                                             task_run['finish_time'],
                                             task_run['info']]
                if i == last:
                    lastID = task_run['id']
    if write:
        with open('taskrun.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["id", "created", "project_id", "task_id",
                             "user_id", "finish_time", 'task'])
            for i in task_dict:
                tr = task_dict[i]
                if type(tr[5]) is dict and tr[3]:
                    writer.writerow([i, tr[0], tr[1], tr[2],
                                     tr[3], tr[4],
                                     tr[5]['highlight_group']['topic_name']])
    else:
        return task_dict


if __name__ == '__main__':
    project_names = ['Covid_SourceRelevancev1', 'Covid_Semantics1.0',
                     "Covid_Reasoningv1", "Covid_Probabilityv1",
                     "Covid_Languagev1.1", "Covid_Holisiticv1.2",
                     "Covid_Form1.0", "Covid_Evidencev1",
                     "Covid_ArgumentRelevancev1.2"]
    project_ids = get_projectIDs(project_names).values()
    taskruns = fill_taskrun(project_ids, write=False)
