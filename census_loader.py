import os
import sys
import csv
import time
import json
import random
import statistics
import threading
from functools import wraps
from get_votes import printProgressBar

__license__ = 'MIT'

PATH_TO_CSVS = 'census/'

STATE_LOOKUP = {
    'ALABAMA': 'AL',
    'ALASKA': 'AK',
    'ARIZONA': 'AZ',
    'ARKANSAS': 'AR',
    'CALIFORNIA': 'CA',
    'COLORADO': 'CO',
    'CONNECTICUT': 'CT',
    'DELAWARE': 'DE',
    'DISTRICT OF COLUMBIA': 'DC',
    'FLORIDA': 'FL',
    'GEORGIA': 'GA',
    'HAWAII': 'HI',
    'IDAHO': 'ID',
    'ILLINOIS': 'IL',
    'INDIANA': 'IN',
    'IOWA': 'IA',
    'KANSAS': 'KS',
    'KENTUCKY': 'KY',
    'LOUISIANA': 'LA',
    'MAINE': 'ME',
    'MARYLAND': 'MD',
    'MASSACHUSETTS': 'MA',
    'MICHIGAN': 'MI',
    'MINNESOTA': 'MN',
    'MISSISSIPPI': 'MS',
    'MISSOURI': 'MO',
    'MONTANA': 'MT',
    'NEBRASKA': 'NE',
    'NEVADA': 'NV',
    'NEW HAMPSHIRE': 'NH',
    'NEW JERSEY': 'NJ',
    'NEW MEXICO': 'NM',
    'NEW YORK': 'NY',
    'NORTH CAROLINA': 'NC',
    'NORTH DAKOTA': 'ND',
    'OHIO': 'OH',
    'OKLAHOMA': 'OK',
    'OREGON': 'OR',
    'PENNSYLVANIA': 'PA',
    'RHODE ISLAND': 'RI',
    'SOUTH CAROLINA': 'SC',
    'SOUTH DAKOTA': 'SD',
    'TENNESSEE': 'TN',
    'TEXAS': 'TX',
    'UTAH': 'UT',
    'VERMONT': 'VT',
    'VIRGINIA': 'VA',
    'WASHINGTON': 'WA',
    'WEST VIRGINIA': 'WV',
    'WISCONSIN': 'WI',
    'WYOMING': 'WY'
}


class Encoder (json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, AgeInfo) or isinstance(obj, IncomeInfo):
            return {'name': obj.name,
                    'average': obj.average,
                    'stddev': obj.stddev,
                    'first_quart': obj.first_quart,
                    'median': obj.median,
                    'third_quart': obj.third_quart
                    }

        return json.JSONEncoder.default(self, obj)


class AgeInfo:
    def __init__(self, age_data, name):
        self.name = name
        self.total, \
            self.male, \
            self.female, \
            self._under_5, \
            self._5_to_9, \
            self._10_to_14, \
            self._15_to_19, \
            self._20_to_24, \
            self._25_to_34, \
            self._35_to_44, \
            self._45_to_54, \
            self._55_to_59, \
            self._60_to_64, \
            self._65_to_74, \
            self._75_to_84, \
            self._85_plus, \
            self.median, \
            self._18_plus, \
            self._65_plus = age_data
        self.average = None
        self.stddev = None
        self.first_sixth = None
        self.second_sixth = None
        self.fourth_sixth = None
        self.fifth_sixth = None
        self.create_distribution()

    def create_distribution(self):
        randomized_ages = []
        randomized_ages.extend([random.randint(0, 5) for _ in range(self._under_5)])
        randomized_ages.extend([random.randint(5, 10) for _ in range(self._5_to_9)])
        randomized_ages.extend([random.randint(10, 15) for _ in range(self._10_to_14)])
        randomized_ages.extend([random.randint(15, 20) for _ in range(self._15_to_19)])
        randomized_ages.extend([random.randint(20, 25) for _ in range(self._20_to_24)])
        randomized_ages.extend([random.randint(25, 35) for _ in range(self._25_to_34)])
        randomized_ages.extend([random.randint(35, 45) for _ in range(self._35_to_44)])
        randomized_ages.extend([random.randint(45, 55) for _ in range(self._45_to_54)])
        randomized_ages.extend([random.randint(55, 60) for _ in range(self._55_to_59)])
        randomized_ages.extend([random.randint(60, 65) for _ in range(self._60_to_64)])
        randomized_ages.extend([random.randint(65, 75) for _ in range(self._65_to_74)])
        randomized_ages.extend([random.randint(75, 85) for _ in range(self._75_to_84)])
        randomized_ages.extend([random.randint(85, 95) for _ in range(self._85_plus)])
        self.average = sum(randomized_ages) / len(randomized_ages)
        self.stddev = statistics.stdev(randomized_ages, xbar=self.average)
        randomized_ages = sorted(randomized_ages)
        l = len(randomized_ages)
        self.first_sixth = randomized_ages[int(l / 6)]
        self.second_sixth = randomized_ages[int(l / 3)]
        self.fourth_sixth = randomized_ages[int(2 * l / 3)]
        self.fifth_sixth = randomized_ages[int((5 * l) / 6)]


    def show_stuff(self):
        print(self.total)
        print(self.male)
        print(self.female)
        print(self._under_5)
        print(self._5_to_9)
        print(self._10_to_14)
        print(self._15_to_19)
        print(self._20_to_24)
        print(self._25_to_34)
        print(self._35_to_44)
        print(self._45_to_54)
        print(self._55_to_59)
        print(self._60_to_64)
        print(self._65_to_74)
        print(self._75_to_84)
        print(self._85_plus)
        print('median', self.median)
        print(self._18_plus)
        print(self._65_plus)


class IncomeInfo:
    def __init__(self, income_data, name):
        self.total, \
            self.under_10, \
            self._10_to_14, \
            self._15_to_24, \
            self._25_to_34, \
            self._35_to_49, \
            self._50_to_74, \
            self._75_to_99, \
            self._100_to_149, \
            self._150_to_199, \
            self.over_200, \
            self.median, \
            self.mean = income_data
        self.name = name
        self.average = None
        self.stddev = None
        self.first_sixth = None
        self.second_sixth = None
        self.fourth_sixth = None
        self.fifth_sixth = None
        self.create_distribution()

    def create_distribution(self):
        incomes = []
        incomes.extend([random.randint(0, 10000) for _ in range(self.under_10)])
        incomes.extend([random.randint(10000, 15000) for _ in range(self.under_10)])
        incomes.extend([random.randint(15000, 25000) for _ in range(self._10_to_14)])
        incomes.extend([random.randint(25000, 35000) for _ in range(self._25_to_34)])
        incomes.extend([random.randint(35000, 50000) for _ in range(self._35_to_49)])
        incomes.extend([random.randint(50000, 75000) for _ in range(self._50_to_74)])
        incomes.extend([random.randint(75000, 100000) for _ in range(self._75_to_99)])
        incomes.extend([random.randint(100000, 150000) for _ in range(self._100_to_149)])
        incomes.extend([random.randint(150000, 200000) for _ in range(self._150_to_199)])
        incomes.extend([random.randint(200000, 300000) for _ in range(self.over_200)])
        self.average = statistics.mean(incomes)
        self.stddev = statistics.stdev(incomes)
        incomes = sorted(incomes)
        l = len(incomes)
        self.first_sixth = incomes[int(l / 6)]
        self.second_sixth = incomes[int(l / 3)]
        self.fourth_sixth = incomes[int(2 * l / 3)]
        self.fifth_sixth = incomes[int((5 * l) / 6)]


def get_all_csv_file_names():
    return os.listdir(PATH_TO_CSVS)


def timed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = time.time()
        ret = f(*args, **kwargs)
        end = time.time()
        print('that took', end - start, 'seconds')
        return ret
    return decorated_function


def row_has_age_data(row):
    return row and row[0] == 'People' and row[1] == 'Sex and Age'


def row_has_income_data(row):
    return row and row[0] == 'Socioeconomic' and row[1][:19] == 'Income and Benefits'


def district_values_from_row(row):
    """Get the values from every district from a given row."""
    ret = []
    last_col = len(row)
    for i in range(3, last_col, 2):
        try:
            ret.append(int(row[i]))
        except ValueError:
            ret.append(float(row[i]))
    return ret


def convert_to_list_of_districts(age_data):
    districts = []

    for i in range(len(age_data[0])):
        district = []
        for row in age_data:
            district.append(row[i])
        districts.append(district)

    return districts


def get_distributions_from_csv(opened_csv):
    """Get every row of the csv concerning the age distribution for every district in
    the state. Returns a list of lists, which is metric-major and district-minor"""
    census_reader = csv.reader(opened_csv)
    age_data = []
    income_data = []

    for row in census_reader:
        if row_has_age_data(row):
            age_data.append(district_values_from_row(row))
        elif row_has_income_data(row):
            income_data.append(district_values_from_row(row))
    assert age_data and income_data
    return convert_to_list_of_districts(age_data), \
        convert_to_list_of_districts(income_data)


def get_state_abbreviation_from_filename(filename):
    before_district = filename.split('_District')[0]
    before_all = before_district.split('_All')[0]
    key = ' '.join(before_all.split('_')).upper()
    return STATE_LOOKUP[key]


def update_dicts_by_thread(combined_dict, state, num, age, income, name):
    combined_dict[state][num] = {}
    combined_dict[state][num]['age'] = AgeInfo(age, name)
    combined_dict[state][num]['income'] = IncomeInfo(income, num)


def create_dictionaries():
    every_csv = get_all_csv_file_names()
    state_district = {}
    thread_pool = []

    for count, csv_filename in enumerate(every_csv):

        state_name = get_state_abbreviation_from_filename(csv_filename)
        state_district[state_name] = {}
        with open(PATH_TO_CSVS + csv_filename, 'r') as opened_csv:
            state_age_data, state_income_data = get_distributions_from_csv(opened_csv)
            for i, (age, income) in enumerate(zip(state_age_data, state_income_data)):
                pb_len = max(len(state_age_data) - 1, 1)
                printProgressBar(i, pb_len, 'Processing ' + state_name)
                num_string = str(i + 1).zfill(2)
                district_name = state_name + num_string
                update_dicts_by_thread(state_district, state_name, num_string, age, income, district_name)
        print()

    return state_district


def pretty_dump_to_json_file(obj, openfile):
    json.dump(obj, openfile, sort_keys=True, indent=2, cls=Encoder)


def main():
    combined_dict = create_dictionaries()
    with open("combined_data.json", "w") as output:
        pretty_dump_to_json_file(combined_dict, output)


if __name__ == '__main__':
    main()
