import requests
import json

headers = {
  'Content-Type': 'application/json',
  'X-API-KEY': '',
}
api_key = ''
project_names = ["Covid2_FormTriage", "Covid2_SemanticsTriage"]
project_ids = ['253', '254']
user_ids = {}


def get_ids(project_ids):
    """
    Input: List of project IDs
    Output: Dictionary of (key) user_ids and (value) the amount of tasks
    they've completed for the given projects
    """
    for project_id in project_ids:
        r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key='
                         + api_key + '&project_id=' + project_id +
                         '&orderby=id', headers=headers)
        task_runs = json.loads(r.text)
        # For each task, either add the user id or incremement the id's count
        for task in task_runs:
            if str(task["user_id"]) in user_ids:
                user_ids[str(task["user_id"])] += 1
            else:
                user_ids[str(task["user_id"])] = 1
    return user_ids


def get_names(user_ids):
    """
    Given the user_ids dictionary (as returned from get_ids(), r
    eturns a dictionary mapping full name to task count
    """
    names = {}
    for user in user_ids:
        r = requests.get('https://pe.goodlylabs.org/api/user/'
                         + user + '?api_key=' + api_key, headers=headers)
        user_info = json.loads(r.text)
        names[user_info['fullname']] = user_ids[user]
    return names


if __name__ == "__main__":
    # Write dictionary to CSV file
    names_dict = get_names(get_ids(project_ids))
    with open('people.csv', 'w') as f:
        for key in names_dict.keys():
            f.write("%s, %s\n" % (key, names_dict[key]))
