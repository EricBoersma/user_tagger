"""
User Tagger: A system for tagging ActionKit users

Usage:
 user_tagger.py <filename>
"""
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__)
    filename = arguments['<filename>']
