# https://github.com/unitedstates/congress-legislators

'''
TERMS
repid
type
start
end
state
district (null if sen)
'''

from yaml import load, dump
import json
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

def print_districts(filepath):
    data = json_loader(filepath)

    for x in data:
        print("%s %s %s" % (x['id']['bioguide'], x['name']['first'], x['name']['last'],))
        for term in x['terms']:
            if term['type'] == 'rep':
                print("\t%s: %s %s %s district %s" % (
                    term['type'], term['start'], term['end'], term['state'], term['district']))
            elif term['type'] == 'sen':
                print("\t%s: %s %s %s" % (term['type'], term['start'], term['end'], term['state']))

def print_changed_districts(filepath):
    data = json_loader(filepath)

    for x in data:
        district = 0
        first = True
        for term in x['terms']:
            if term['type'] == 'rep':
                if first:
                    district = term['district']
                    first = False
                elif district != term['district']:
                    district = term['district']
                    if term['start'] > date(2007, 12, 5).isoformat():
                        print("%s %s %s changed district" % (
                            x['id']['bioguide'], x['name']['first'], x['name']['last'],))

def print_recent_districts(filepath):
    data = json_loader(filepath)

    for x in data:
        print("%s %s %s" % (x['id']['bioguide'], x['name']['first'], x['name']['last'],))
        for term in x['terms']:
            if term['type'] == 'rep':
                if term['start'] > date(2007, 12, 5).isoformat():
                    print("\t%s: %s %s %s district %s" % (
                        term['type'], term['start'], term['end'], term['state'], term['district']))

#not deleting terms
def trim(filepath):
    data = json_loader(filepath)

    for rep in data:
        # district = 0
        # first = True
        terms = rep['terms']
        for term in terms:
            # if term['type'] == 'rep':
            '''
            if first:
                district = term['district']
                first = False
            elif district != term['district']:
                district = term['district']
            '''
            date = datetime.strptime(term['start'], "%Y-%m-%d")
            if date < datetime(2007, 12, 5):
                #print ("start %s" % term['start'])
                del term

    json_dump("dumpfile.json", data)

def main():
    #sample = 'rep_info/legislators-sample.json'
    historic = 'rep_info/legislators-historical.json'
    current = 'rep_info/legislators-current.json'

    #print_changed_districts(current)
    trim(current)



if __name__ == "__main__":
    main()
