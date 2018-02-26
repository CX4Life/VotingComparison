import json
import re


PATH_TO_BILLS = '../congress/data'

'''
  "bill": {
    "congress": 113, 
    "number": 2217, 
    "type": "hr"
  }
  '''
def get_bill(congress, num, type):
    ret = None
    try:
        file = PATH_TO_BILLS + '/' + congress + '/bills/' + type + '/' + type + num + "/data.json"
        with open(file, 'r') as bill:
            ret = json.load(bill)
    except FileNotFoundError:
        print("Could not find file %s" % file)

    return ret

def main():
    congress = "113"
    bill = "2217"
    type = "hr"
    bill_json = get_bill(congress, bill, type)
    if bill_json["summary"]:
        summary = str(bill_json["summary"]["text"])
        # convert "\n" to '\n'
        re.sub('/\\n/', '\n', summary)
        print(summary)


if __name__ == '__main__':
    main()
