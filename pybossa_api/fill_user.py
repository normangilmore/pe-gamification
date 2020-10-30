from get_people import get_ids
import requests
import json
import os
import csv

PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}


def fill_user(user_ids, write=True):
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
    if write:
        with open('user.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["id", "name", "email"])
            for i in emails:
                writer.writerow([i, emails[i][0], emails[i][1]])
    return emails


if __name__ == '__main__':
    project_names = ['Covid2_FormTriage', 'Covid2_SemanticsTriage']
    project_ids = ['253', '254']
    user_ids = get_ids(project_ids)
    emails = fill_user(user_ids, False)
    print(emails)
