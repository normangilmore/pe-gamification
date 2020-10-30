import requests
import json
import os
import csv

PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}


def get_ids(project_ids):
    """
    Input: List of project IDs
    Output: Dictionary of (key) user_ids and (value) the amount of tasks
    they've completed for the given projects
    """
    user_ids = {}
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


def get_names(user_ids):
    """
    Input: user_ids dictionary
    Output: a dictionary mapping full name to task count
    """
    names = {}
    for user in user_ids:
        r = requests.get('https://pe.goodlylabs.org'
                         '/api/user/{}?api_key={}&limit=100'
                         .format(user, PYBOSSA_API_KEY), headers=headers)
        user_info = json.loads(r.text)
        names[user_info['fullname']] = user_ids[user]
    return names

def fill_user(user_ids):
    """
    Input: user_ids dictionary (user ids: task values)
    Output: csv file with user id, name, email
    """
    emails = {}
    for user in user_ids:
        r = requests.get('https://pe.goodlylabs.org'
                         '/api/user/{}?api_key={}&limit=100'
                         .format(user, PYBOSSA_API_KEY), headers=headers)
        user_info = json.loads(r.text)
        emails[user] = [user_info['fullname'], user_info['email_addr']]
    with open('user.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "name", "email"])
        for i in emails:
            writer.writerow([i, emails[i][0], emails[i][1]])



if __name__ == '__main__':
    project_names = ['Covid2_FormTriage', 'Covid2_SemanticsTriage']
    project_ids = ['253', '254']
    user_ids = get_ids(project_ids)

    emails = fill_user(user_ids)
    print(emails)
    #names_dict = get_names(user_ids)
"""
    with open('hi.csv', 'w') as f:
        for key in names_dict.keys():
            f.write("%s, %s\n" % (key, names_dict[key]))"""
