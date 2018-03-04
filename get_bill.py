import json
import re
import os
from datetime import date, datetime

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def json_loader(filepath):
    with open(filepath, 'r') as current:
        return json.load(current)


def json_dump(filepath, data):
    with open(filepath, 'w') as current:
        json.dump(data, current, indent=4)


USER_HOME_DIR = os.path.expanduser('~')
VOTING_COMPARISON_DIR = USER_HOME_DIR + '/PycharmProjects/VotingComparison'
PATH_TO_BILLS = USER_HOME_DIR + '/PycharmProjects' + '/congress/data'

'''
  "bill": {
    "congress": 113, 
    "number": 2217, 
    "type": "hr"
  }
  '''


def get_bill(congress, num, bill_type):
    bill_text = None
    try:
        file = PATH_TO_BILLS + '/' + congress + '/bills/' + bill_type + '/' + bill_type + num + "/data.json"
        with open(file, 'r') as bill:
            bill = json.load(bill)
            if('summary' in bill
                    and bill['summary'] is not None
                    and 'text' in bill['summary']):
                bill_text = str(bill['summary']['text'])
                re.sub('/\\n/', '\n', bill_text)
                # bill["summary"]["text"] = bill_text
                #print(bill_text)
                return bill_text
    except FileNotFoundError:
        print("Could not find file %s" % file)

    return bill_text


def build_bill_json():
    d = {}

    for congress_meeting in os.listdir(PATH_TO_BILLS):
        #print(congress_meeting)
        for year in os.listdir(PATH_TO_BILLS + '/' + congress_meeting + '/votes'):
            if year > "113":
                #print(year)
                # for years in os.walk(congress):

                first = True
                for vote_folder in os.listdir(PATH_TO_BILLS + '/' + congress_meeting + '/votes/' + year):
                    #print(vote_folder)
                    with open(PATH_TO_BILLS
                              + '/'
                              + congress_meeting
                              + '/votes/'
                              + year
                              + '/'
                              + vote_folder
                              + '/data.json', 'r') as vote_file:
                        vote_data = json.load(vote_file)
                        if('bill' in vote_data):
                            #print(vote_data)
                            #if('congress' in vote_data['bill']
                            #        and 'number' in vote_data['bill']
                            #        and 'bill_type' in vote_data['bill']):
                            congress = str(vote_data['bill']['congress'])
                            number = str(vote_data['bill']['number'])
                            bill_type = vote_data['bill']['type']

                            if(congress is not None and number is not None and bill_type is not None):
                                bill_summary = get_bill(congress, number, bill_type)
                                if bill_summary is not None:
                                    bill_id = bill_type + number + '-' + congress
                                    d[bill_id] = bill_summary
                            else:
                                raise ValueError("No data for get_bill")

    json_dump(VOTING_COMPARISON_DIR + "/bill_summaries.json", d)




def main():
    congress = "113"
    bill = "2217"
    type = "hr"
    #print(get_bill(congress, bill, type))
    build_bill_json()


if __name__ == '__main__':
    main()
