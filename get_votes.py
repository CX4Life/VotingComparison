"""Get all votes using the github.com/unitedstates/congress tools for
TIME_PERIOD"""

__authors__ = [
    'Alexander Lee',
    'Tim Woods'
]
__copyright__ = 'Copyright (c) 2018 Alexander Lee, Tim Woods'
__license__ = 'MIT'

import os
import json
# import insert_all_reps

USERS_HOME_DIR = 'placeholder'#os.environ['HOME']
CONGRESS_WORKING_DIR = USERS_HOME_DIR + '/CS477/congress'
PARAM_FILENAME = 'sess_years.json'
REWRITE_ERRORS = True


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


def write_params_if_not_present():
    """If the parameter file isn't present, create it."""
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
    if PARAM_FILENAME not in os.listdir(os.getcwd()):
        with open(PARAM_FILENAME, 'w') as params:
            json.dump(session_years, params)


def write_params_after_db_update(remaining, errors):
    if errors and REWRITE_ERRORS:
        remaining.extend(errors)
    with open(PARAM_FILENAME, 'w') as params:
        json.dump(remaining, params)


def load_params():
    ret = None
    with open(PARAM_FILENAME, 'r') as params:
        ret = json.load(params)
    return ret


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 60, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def main():
    write_params_if_not_present()
    session_years = load_params()
    assert session_years is not None

    errors = []
    sess_year = []

    while session_years:
        sess_year = session_years[-1]
        session_years = session_years[:-1]
        votes_this_year = get_all_json_files(*sess_year)
        total_votes = len(votes_this_year)
        for i, json_vote_file in enumerate(votes_this_year):
            printProgressBar(i, total_votes, str(sess_year[0]) + ' ' + str(sess_year[1]))
            try:
                insert_all_reps.update_representatives_table(json_vote_file)
            except ValueError:
                errors.append(sess_year)
                continue

        if errors:
            print('sessions in error:')
            print(errors)
        write_params_after_db_update(session_years, errors)


if __name__ == '__main__':
    main()
