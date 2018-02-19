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

#txt = doc['- id']['bioguide']


#legislators-current.yaml

def main():
    filepath = 'legislators-current.yaml'
    data = yaml_loader(filepath)

    for x in data:
        print("%s %s %s" % (x['id']['bioguide'], x['name']['first'], x['name']['last']))

if __name__ == "__main__":
    main()