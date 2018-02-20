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
from datetime import date, datetime

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def yaml_loader(filepath):
    with open(filepath, 'r') as current:
        return load(current, Loader=Loader)


def yaml_dump(filepath, data):
    with open(filepath, 'w') as current:
        dump(data, current, default_flow_style=False)

def print_districts(filepath):
    data = yaml_loader(filepath)

    for x in data:
        print("%s %s %s" % (x['id']['bioguide'], x['name']['first'], x['name']['last'],))
        for term in x['terms']:
            if term['type'] == 'rep':
                print("\t%s: %s %s %s district %s" % (
                    term['type'], term['start'], term['end'], term['state'], term['district']))
            elif term['type'] == 'sen':
                print("\t%s: %s %s %s" % (term['type'], term['start'], term['end'], term['state']))

def print_changed_districts(filepath):
    data = yaml_loader(filepath)

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
    data = yaml_loader(filepath)

    for x in data:
        print("%s %s %s" % (x['id']['bioguide'], x['name']['first'], x['name']['last'],))
        for term in x['terms']:
            if term['type'] == 'rep':
                if term['start'] > date(2007, 12, 5).isoformat():
                    print("\t%s: %s %s %s district %s" % (
                        term['type'], term['start'], term['end'], term['state'], term['district']))

#not deleting terms
def trim(filepath):
    data = yaml_loader(filepath)

    for x in data:
        # district = 0
        # first = True
        for term in x['terms']:
            # if term['type'] == 'rep':
            '''
            if first:
                district = term['district']
                first = False
            elif district != term['district']:
                district = term['district']
            '''
        if datetime.strptime(term['start'], "%Y-%m-%d") <= datetime(2007, 12, 5):
            del term

    yaml_dump("dumpfile.yaml", data)

def main():
    sample = 'rep_info/legislators-sample.yaml'
    historic = 'rep_info/legislators-historical.yaml'
    current = 'rep_info/legislators-current.yaml'

    #print_changed_districts(current)
    trim(current)



if __name__ == "__main__":
    main()
