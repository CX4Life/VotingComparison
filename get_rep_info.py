from datetime import date, datetime
from get_bill import json_loader, json_dump
import operator

historic = 'rep_info/legislators-historical.json'
current = 'rep_info/legislators-current.json'

file = current

nonVoting = ('AS', 'DC', 'GU', 'MP', 'PR', 'VI', 'UM')


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


# Print a list of all reps that changed their districts in 113th congress and later
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

# Write all repIDs and a string containing state and district (Ex: 'WA02')
def get_districts():
    data = json_loader(file)

    districts = {}

    for x in data:
        id = x['id']
        repID = id['bioguide']
        state, district = get_district(repID)
        if district is not None:
            if district not in districts:
                district = str(district).rjust(2, '0')
                districts[repID] = state + district
            else:
                print(rep + " " + district)

    districts = {district: rep for rep, district in districts.items()}

    json_dump('districts.json', districts)


# return state (ex: 'WA') and district number
def get_district(repID):
    data = json_loader(file)

    for x in data:
        id = x['id']
        if id['bioguide'] == repID:
            for term in x['terms']:
                if term['type'] == 'rep' and term['state'] not in nonVoting:
                    if term['end'] >= date(2018, 3, 5).isoformat():
                        #print(str(repID) + term['state'] + str(term['district']))
                        return term['state'], term['district']
            else:
                return None, None

def main():
    #print_changed_districts()
    #print(get_district("L000560"))
    get_districts()


if __name__ == "__main__":
    main()
