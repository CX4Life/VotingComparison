#https://github.com/unitedstates/congress-legislators

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def yaml_loader(filepath):
    with open(filepath, 'r') as current:
        return load(current, Loader=Loader)

def yaml_dump(filepath, data):
    with open(filepath, 'w') as current:
        yaml.dump(data, current)

def main():
    sample = 'rep_info/legislators-sample.yaml'
    historic = 'rep_info/legislators-historical.yaml'
    current = 'rep_info/legislators-current.yaml'

    data = yaml_loader(sample)

    for x in data:
        print("%s %s %s" % (x['id']['bioguide'], x['name']['first'], x['name']['last'],))
        for term in x['terms']:
            if term['type'] == 'rep':
                print("\t%s: %s %s %s district %s" % (term['type'], term['start'], term['end'], term['state'], term['district']))
            elif term['type'] == 'sen':
                print("\t%s: %s %s %s" % (term['type'], term['start'], term['end'], term['state']))

if __name__ == "__main__":
    main()