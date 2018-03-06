from datetime import date, datetime
from get_bill import json_loader, json_dump
import operator

historic = 'rep_info/legislators-historical.json'
current = 'rep_info/legislators-current.json'

file = current


def print_districts():
    data = json_loader(file)

    for x in data:
        print("%s %s %s" % (x['id']['bioguide'], x['name']['first'], x['name']['last'],))
        for term in x['terms']:
            if term['type'] == 'rep':
                print("\t%s: %s %s %s district %s" % (
                    term['type'], term['start'], term['end'], term['state'], term['district']))
            elif term['type'] == 'sen':
                print("\t%s: %s %s %s" % (term['type'], term['start'], term['end'], term['state']))


def print_changed_districts():
    data = json_loader(file)

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



def get_districts():
    data = json_loader(file)

    districts = {}

    for x in data:
        id = x['id']
        repID = id['bioguide']
        state, district = get_district(repID)
        if district is not None:
            district = str(district).rjust(2, '0')
            districts[repID] = state + district
    json_dump('districts.json', districts)


def get_district(repID):
    data = json_loader(file)

    districts = []

    for x in data:
        id = x['id']
        if id['bioguide'] == repID:
            for term in x['terms']:
                if term['type'] == 'rep':
                    if term['start'] > date(2013, 1, 3).isoformat():
                        if term['district'] not in districts:
                            districts.append([term['start'], term['state'], term['district']])
            # returns the most district for the rep
            if districts:
                index, last = max(enumerate(districts), key=operator.itemgetter(0))
                return last[1], last[2]
            else:
                #print("Error: shouldn't reach here")
                return None, None


def main():
    #print_changed_districts()
    #trim(current)

    #get_district("L000560")
    get_districts()


if __name__ == "__main__":
    main()
