import json
import mysql.connector

already_seen = set()
HOSTNAME = 'localhost'
USERNAME = 'root'
PASSWORD = 'aImFB83ClwKyoolJ'
DB_NAME = 'VOTING'


def insert_representative_into_table(rep):
    conn = mysql.connector.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD, db=DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT Rep_ID FROM Represenatives')
    for id in cur.fetchall():
        print(id)

    print('Done', rep)


def update_representatives_table(json_filepath):
    with open(json_filepath, 'r') as j_file:
        vote_object = json.load(j_file)

    every_vote = vote_object['votes']
    for vote_result in every_vote.keys():
        for representative in every_vote[vote_result]:
            if representative['id'] not in already_seen:
                insert_representative_into_table(representative)
                exit(0)
