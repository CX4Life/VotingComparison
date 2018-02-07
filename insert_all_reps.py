import json
import pymysql

already_seen = set()
HOSTNAME = 'localhost'
USERNAME = 'root'
PASSWORD = 'aImFB83ClwKyoolJ'
DB_NAME = 'VOTING'


def insert_representative_into_table(rep):
    global conn
    cur = conn.cursor()
    updated = cur.execute(
        "INSERT IGNORE INTO Representative VALUES (%s, %s, %s, %s);",
        (rep['id'], rep['display_name'], rep['party'], rep['state']))
    print('Done', rep['id'], updated)


def update_representatives_table(json_filepath):
    with open(json_filepath, 'r') as j_file:
        vote_object = json.load(j_file)

    every_vote = vote_object['votes']
    for vote_result in every_vote.keys():
        for representative in every_vote[vote_result]:
            if representative['id'] not in already_seen:
                insert_representative_into_table(representative)


def main():
    global conn
    conn = pymysql.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD, db=DB_NAME)
    update_representatives_table('sample_data.json')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()