import json
from datetime import datetime
import pymysql

already_seen = set()
HOSTNAME = 'localhost'
USERNAME = 'root'
PASSWORD = 'aImFB83ClwKyoolJ'
DB_NAME = 'VOTING'
LOG_FILE = 'updated_id.txt'


def clean_fetched_ID(id):
    """Remove MySQL artifacts from fetched IDs"""
    return ''.join([x for x in id if x not in "',"])


def select_existing_representatives(connection):
    """From the existing MySQL database, select all the existing representative IDs,
    and return them as a set."""
    cur = connection.cursor()
    cur.execute("SELECT Rep_ID FROM Representative;")
    rep_ids_punc = set(cur.fetchall())
    rep_ids = set([clean_fetched_ID(x) for x in rep_ids_punc])
    return rep_ids


def insert_representative_into_table(rep, conn):
    cur = conn.cursor()
    updated = cur.execute(
        "INSERT IGNORE INTO Representative VALUES (%s, %s, %s, %s);",
        (rep['id'], rep['display_name'], rep['party'], rep['state']))
    with open(LOG_FILE, 'r') as log:
        log.write('{}: Added {}'.format(datetime.now(), rep['id']))

def return_representatives(json_file):
    ret = []

    vote_object = json.load(json_file)
    every_vote = vote_object['votes']
    for vote_type in every_vote.keys():
        ret.extend([x for x in every_vote[vote_type]])
    return ret


def update_representatives_table(json_filepath, set_of_representatives=None):
    global already_seen
    conn = pymysql.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD, db=DB_NAME)
    already_seen = select_existing_representatives(conn)

    # if this method is called with a collection of representatives,
    # do the insert using that set of representatives instead of collecting those representatives
    # from the JSON file.
    if set_of_representatives is not None:
        for representative in set_of_representatives:
            insert_representative_into_table(representative)
        return

    with open(json_filepath, 'r') as j_file:
        every_representative = return_representatives(j_file)

    for representative in every_representative:
        try:
            if representative['id'] not in already_seen:
                insert_representative_into_table(representative, conn)
        except TypeError:
            print('error on rep id')
            print(representative)
            raise ValueError


    conn.commit()
    conn.close()


def main():
    with open('sample_data.json', 'r') as jfile:
        reps = return_representatives(jfile)
        for r in reps:
            print(r['id'])

if __name__ == '__main__':
    main()
