"""
User Tagger: A system for tagging ActionKit users

Usage:
 user_tagger.py <filename> <ak_username> <ak_password>
"""
from docopt import docopt
import csv
import json
from progressbar import ProgressBar
import requests
from requests.auth import HTTPBasicAuth
from multiprocessing import Process

headers = {
    'Content-type': 'application/json'
}

arguments = docopt(__doc__)
filename = arguments['<filename>']
username = arguments['<ak_username>']
password = arguments['<ak_password>']


def post_accepted_name(name):
    allowed_dict = {
        'name': name
    }
    allowed_data = json.dumps(allowed_dict)
    requests.post('https://act.sumofus.org/rest/v1/alloweduserfield/',
                  auth=HTTPBasicAuth(username, password),
                  headers=headers,
                  data=allowed_data)


def tag_userfield(entry):
    row_dict = {
        'user': ''.join(['/rest/v1/user/', entry['id'], '/']),
        'name': entry['name'],
        'value': entry['value']
    }
    requests.post('https://act.sumofus.org/rest/v1/alloweduserfield/',
                  auth=HTTPBasicAuth(username, password),
                  headers=headers,
                  data=json.dumps(row_dict))


if __name__ == '__main__':

    with open(filename, 'r') as csvfile:
        rows = csv.DictReader(csvfile)
        progress = ProgressBar(maxval=sum(1 for _ in rows))
        progress.start()
        csvfile.seek(0)  # reset the file index to iterate over the file again
        rows.next()  # slice off the titles since we reset to zero
        row = rows.next()
        post_accepted_name(row['name'])
        tag_userfield(row)
        i = 1
        progress.update(i)
        for row in rows:
            p = Process(target=post_accepted_name, args=(row, ))
            p.start()
            p.join()
            i += 1
            progress.update(i)
