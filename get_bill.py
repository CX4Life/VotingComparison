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
    bill_text = None
    try:
        file = PATH_TO_BILLS + '/' + congress + '/bills/' + type + '/' + type + num + "/data.json"
        with open(file, 'r') as bill:
            bill = json.load(bill)
            bill_text = str(bill["summary"]["text"])
            re.sub('/\\n/', '\n', bill_text)
            # bill["summary"]["text"] = bill_text
            # print(bill["summary"]["text"])
            return bill_text
    except FileNotFoundError:
        print("Could not find file %s" % file)

    return bill_text

def main():
    congress = "113"
    bill = "2217"
    type = "hr"
    bill_json = get_bill(congress, bill, type)


if __name__ == '__main__':
    main()
