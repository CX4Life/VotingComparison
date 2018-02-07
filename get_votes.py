"""Get all votes using the github.com/unitedstates/congress tools for
TIME_PERIOD"""

__authors__ = [
    'Alexander Lee',
    'Tim Woods'
]
__copyright__ = 'Copyright (c) 2018 Alexander Lee, Tim Woods'
__license__ = 'MIT'

import os
import insert_all_reps

USERS_HOME_DIR = os.environ['HOME']
CONGRESS_WORKING_DIR = USERS_HOME_DIR + '/CS477/congress'


def get_all_json_files(session, year):
    """Given the year for which the vote was cast, use os.walk to retrieve the
    path to every data.json file contained within any subdirectory of that year.
    Return: a list of paths to data.json files."""

    _data_directory_name = CONGRESS_WORKING_DIR + '/data/' + session + '/votes/' + year

    ret = []
    for root, dirs, filenames in os.walk(_data_directory_name):
        for name in filenames:
            if '.json' in name:
                ret.append(os.path.join(root, name))
    return ret


def main():
    session_years = [
        ('113', '2013'),
        ('110', '2008'),
        ('111', '2010'),
        ('112', '2011'),
        ('112', '2012'),
        ('111', '2009'),
        ('113', '2014'),
        ('114', '2015'),
        ('114', '2016'),
        ('115', '2017'),
        ('115', '2018')
    ]
    for sess_year in session_years:
        votes_this_year = get_all_json_files(*sess_year)
        print(len(votes_this_year))
        for json_vote_file in votes_this_year:
            insert_all_reps.update_representatives_table(json_vote_file)


if __name__ == '__main__':
    main()
