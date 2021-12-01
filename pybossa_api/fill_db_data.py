import requests
import json
import os
import csv
from utils import get_projectIDs, get_categoryIDs, get_category

PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}


def fill_taskrun(project_dict, category_ids, category_dict, write=True):
    '''
    Input: List of project_ids
    Output: csv file with taskrun info
    '''
    task_dict = {}
    emails = {}
    for project_name in project_dict:
        project_id = project_dict[project_name]
        r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                         '&project_id={}&orderby=id&limit=100'
                         .format(PYBOSSA_API_KEY, project_id),
                         headers=headers)
        task_runs = json.loads(r.text)
        last = len(task_runs) - 1
        for i in range(len(task_runs)):
            task_run = task_runs[i]
            user = task_run['user_id']
            if user not in emails and user is not None:
                print("adding user:", user)
                req = requests.get('https://pe.goodlylabs.org'
                                   '/api/user/{}'
                                   '?api_key={}&limit=100'
                                   .format(user, PYBOSSA_API_KEY),
                                   headers=headers)
                user_info = json.loads(req.text)
                emails[user] = user_info
            elif user is not None:
                user_info = emails[user]
            if 'fullname' in user_info:
                task_dict[task_run['id']] = [task_run['created'],
                                             task_run['project_id'],
                                             task_run['task_id'],
                                             task_run['user_id'],
                                             task_run['finish_time'],
                                             task_run['info'],
                                             project_name,
                                             user_info['fullname'],
                                             user_info['email_addr'],
                                             #"pe.test.db@gmail.com",
                                             category_ids[project_name],
                                             category_dict[category_ids[project_name]]]
            if i == last:
                lastID = task_run['id']
        # Since we can only retrieve 100 tasks at a time...
        while len(task_runs) == 100:
            r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                             '&project_id={}&last_id={}&orderby=id&limit=100'
                             .format(PYBOSSA_API_KEY, project_id, lastID),
                             headers=headers)
            task_runs = json.loads(r.text)
            last = len(task_runs) - 1
            for i in range(len(task_runs)):
                task_run = task_runs[i]
                user = task_run['user_id']
                if user not in emails and user is not None:
                    print("adding user:", user)
                    req = requests.get('https://pe.goodlylabs.org'
                                       '/api/user/{}?api_key={}&limit=100'
                                       .format(user, PYBOSSA_API_KEY),
                                       headers=headers)
                    user_info = json.loads(req.text)
                    emails[user] = user_info
                elif user is not None:
                    user_info = emails[user]
                if 'fullname' in user_info:
                    task_dict[task_run['id']] = [task_run['created'],
                                                 task_run['project_id'],
                                                 task_run['task_id'],
                                                 task_run['user_id'],
                                                 task_run['finish_time'],
                                                 task_run['info'],
                                                 project_name,
                                                 user_info['fullname'],
                                                 user_info['email_addr'],
                                                 #"pe.test.db@gmail.com",
                                                 category_ids[project_name],
                                                 category_dict[category_ids[project_name]]]
                if i == last:
                    lastID = task_run['id']
    if write:
        with open('taskRuns_42121.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["id", "created", "project_id", "task_id",
                             "user_id", "finish_time", 'task_type',
                             'project_name', 'name', 'email_addr',
                             'category', 'category_name'])
            for i in task_dict:
                tr = task_dict[i]
                if type(tr[5]) is dict and tr[3]:
                    if tr[5]['highlight_group']['topic_name'] == 'Show Entire Document':
                        writer.writerow([i, tr[0], tr[1], tr[2],
                                         tr[3], tr[4],
                                         'form', tr[6], tr[7], tr[8], tr[9], tr[10]])
                    else:
                        writer.writerow([i, tr[0], tr[1], tr[2],
                                         tr[3], tr[4],
                                         tr[5]['highlight_group']['topic_name'].lower(),
                                         tr[6], tr[7], tr[8], tr[9], tr[10]])
    else:
        return task_dict


if __name__ == '__main__':
    categories = ["covidarticles", "covidtrainingtasks"]
    project_names = ['Covid_SourceRelevancev1', 'Covid_Semantics1.0',
                     "Covid_Reasoningv1", "Covid_Probabilityv1",
                     "Covid_Languagev1.1", "Covid_Holisiticv1.2",
                     "Covid_Form1.0", "Covid_Evidencev1",
                     "Covid_ArgumentRelevancev1.2",
                     "Covid2_FormTriage", "Covid2_SemanticsTriage",
                     "Covid2.1_Sources", "Covid2.1_Holistic",
                     "Covid2.1_Probability", "Covid2.1_Reasoning",
                     "Covid2.1_Arguments", "Covid2.1_Language",
                     "Covid2.1_Evidence"]
    category_ids = get_categoryIDs(project_names)
    category_dict = get_category(category_ids)
    project_dict = get_projectIDs(project_names)
    taskruns = fill_taskrun(project_dict, category_ids, category_dict, write=True)
