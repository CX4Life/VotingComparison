from datetime import date, datetime
from get_bill import json_loader, json_dump
import operator


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
                if term['start'] > date(2013, 1, 3).isoformat():
                    if district != term['district']:
                        district = term['district']
                        if not first:
                            print("%s %s %s changed district" % (
                                x['id']['bioguide'], x['name']['first'], x['name']['last'],))
                        first = False


def get_district(filepath, repID):
    data = json_loader(filepath)

    districts = []

    for x in data:
        id = x['id']
        if id['bioguide'] == repID:
            for term in x['terms']:
                if term['type'] == 'rep':
                    if term['start'] > date(2013, 1, 3).isoformat():
                        if term['district'] not in districts:
                            districts.append([term['start'], term['district']])
            #print(districts)
            # returns the most district for the rep
            index, last = max(enumerate(districts), key=operator.itemgetter(0))
            return last[1]


def main():
    #sample = 'rep_info/legislators-sample.json'
    historic = 'rep_info/legislators-historical.json'
    current = 'rep_info/legislators-current.json'

    print_changed_districts(current)
    #trim(current)

    get_district(current, "H001065")


if __name__ == "__main__":
    main()
