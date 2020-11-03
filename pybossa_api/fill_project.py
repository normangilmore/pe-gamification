import requests
import json
import os
import csv


PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}


def fill_project(project_names, filename='project', write=True):
    """
    Input: user_ids dictionary (user ids: task values)
    Output: csv file with user id, name, email
    """
    projects = {}
    for project_name in project_names:
        r = requests.get('https://pe.goodlylabs.org/api/project?api_key={}'
                         '&short_name={}&orderby=id&limit=100'
                         .format(PYBOSSA_API_KEY, project_name),
                         headers=headers)
        project_ids = json.loads(r.text)[0]
        projects[project_ids['id']] = [project_ids['name'],
                                       project_ids['short_name'],
                                       project_ids['category_id']]
    if write:
        with open('{}.csv'.format(filename), 'w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["id", "name", "short_name", "category_id"])
            for i in projects:
                writer.writerow([i, projects[i][0], projects[i][1],
                                 projects[i][2]])
    return projects


if __name__ == '__main__':
    project_names = ['Covid_SourceRelevancev1', 'Covid_Semantics1.0',
                     "Covid_Reasoningv1", "Covid_Probabilityv1",
                     "Covid_Languagev1.1", "Covid_Holisiticv1.2",
                     "Covid_Form1.0", "Covid_Evidencev1",
                     "Covid_ArgumentRelevancev1.2"]
    fill_project(project_names)
