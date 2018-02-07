import json
import pymysql

already_seen = set()
HOSTNAME = 'localhost'
USERNAME = 'root'
PASSWORD = 'aImFB83ClwKyoolJ'
DB_NAME = 'VOTING'


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
    print('Done', rep['id'], updated)


def update_representatives_table(json_filepath):
    global already_seen
    conn = pymysql.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD, db=DB_NAME)
    already_seen = select_existing_representatives(conn)

    with open(json_filepath, 'r') as j_file:
        vote_object = json.load(j_file)

    every_vote = vote_object['votes']
    for vote_result in every_vote.keys():
        for representative in every_vote[vote_result]:
            if representative['id'] not in already_seen:
                insert_representative_into_table(representative, conn)

    conn.commit()
    conn.close()
