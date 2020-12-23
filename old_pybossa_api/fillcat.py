from get_people import get_ids
import requests
import json
import os
import csv

PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}


def fill_project(category='featured', filename='user', write=True):
    """
    Input: user_ids dictionary (user ids: task values)
    Output: csv file with user id, name, email
    """
    r = requests.get('https://pe.goodlylabs.org'
                     '/project/category/{}/?api_key={}&limit=100'
                     .format(category, PYBOSSA_API_KEY), headers=headers)
    categories = json.loads(r.text)['categories']
    for c in categories:
        print(c['name'])


if __name__ == '__main__':
    project_names = ['Covid2_FormTriage', 'Covid2_SemanticsTriage']
    categories = ['covidtrainingtasks', 'covidarticles']
    project_ids = ['253', '254']
    #user_ids = get_ids(project_ids)
    emails = fill_project()
    #print(emails)
