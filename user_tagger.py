"""
User Tagger: A system for tagging ActionKit users

Usage:
 user_tagger.py <filename>
"""
from docopt import docopt
import csv
import json


if __name__ == '__main__':
    arguments = docopt(__doc__)
    filename = arguments['<filename>']
    with open(filename, 'r') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            row_dict = {
                'id': row['id'],
                'name': row['name'],
                'value': row['value']
            }
            row_json = json.dumps(row_dict)
            