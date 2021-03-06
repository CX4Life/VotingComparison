import json
import re
import os

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def json_loader(filepath):
    with open(filepath, 'r') as current:
        return json.load(current)


def json_dump(filepath, data):
    with open(filepath, 'w') as current:
        json.dump(data, current, indent=4, sort_keys=True)


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

# Returns bill text
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
                return bill_text
    except FileNotFoundError:
        print("Could not find file %s" % file)

    return bill_text


# creates a JSON of all house bill texts
def build_bill_json():
    d = {}

    senate_ty = ['s', 'sconres', 'sjres', 'sres']

    for congress_meeting in os.listdir(PATH_TO_BILLS):
        if congress_meeting >= "113":
            for year in os.listdir(PATH_TO_BILLS + '/' + congress_meeting + '/votes'):
                for vote_folder in os.listdir(PATH_TO_BILLS + '/' + congress_meeting + '/votes/' + year):
                    vote_data = json_loader(PATH_TO_BILLS
                                            + '/'
                                            + congress_meeting
                                            + '/votes/'
                                            + year
                                            + '/'
                                            + vote_folder
                                            + '/data.json')
                    if 'bill' in vote_data:
                        congress = str(vote_data['bill']['congress'])
                        number = str(vote_data['bill']['number'])
                        bill_type = vote_data['bill']['type']

                        if congress is not None and number is not None and bill_type is not None:
                            if bill_type not in senate_ty:
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
