import pymysql
import os
import csv
import time
import json
import random
import statistics
from functools import wraps

__license__ = 'MIT'

PATH_TO_CSVS = 'census/'


class AgeInfo:
    def __init__(self, age_data):
        #TODO off by one, only loading first district
        self.total,\
        self.male,\
        self.female,\
        self._under_5,\
        self._5_to_9,\
        self._10_to_14,\
        self._15_to_19,\
        self._20_to_24,\
        self._25_to_34,\
        self._35_to_44,\
        self._45_to_54,\
        self._55_to_59,\
        self._60_to_64,\
        self._65_to_74,\
        self._75_to_84,\
        self._85_plus,\
        self.median,\
        self._18_plus,\
        self._65_plus = age_data
        self.average = None
        self.stddev = None
        self.create_distribution()

    def create_distribution(self):
        randomized_ages = []
        randomized_ages.extend([random.randint(0, 5) for x in range(self._under_5)])
        randomized_ages.extend([random.randint(5, 10) for x in range(self._5_to_9)])
        randomized_ages.extend([random.randint(10, 15) for x in range(self._10_to_14)])
        randomized_ages.extend([random.randint(15, 20) for x in range(self._15_to_19)])
        randomized_ages.extend([random.randint(20, 25) for x in range(self._20_to_24)])
        randomized_ages.extend([random.randint(25, 35) for x in range(self._25_to_34)])
        randomized_ages.extend([random.randint(35, 45) for x in range(self._35_to_44)])
        randomized_ages.extend([random.randint(45, 55) for x in range(self._45_to_54)])
        randomized_ages.extend([random.randint(55, 60) for x in range(self._55_to_59)])
        randomized_ages.extend([random.randint(60, 65) for x in range(self._60_to_64)])
        randomized_ages.extend([random.randint(65, 75) for x in range(self._65_to_74)])
        randomized_ages.extend([random.randint(75, 85) for x in range(self._75_to_84)])
        randomized_ages.extend([random.randint(85, 95) for x in range(self._85_plus)])
        self.average = sum(randomized_ages) / len(randomized_ages)
        self.stddev = statistics.stdev(randomized_ages)

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
    def __init__(self, income_data):
        self.total,\
        self.under_10,\
        self._10_to_14,\
        self._15_to_24,\
        self._25_to_34,\
        self._35_to_49,\
        self._50_to_74,\
        self._75_to_99,\
        self._100_to_149,\
        self._150_to_199,\
        self.over_200,\
        self.median,\
        self.mean = income_data
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


def get_all_csvs():
    return os.listdir(PATH_TO_CSVS)


def timed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = time.time()
        ret = f(*args, **kwargs)
        end = time.time()
        print(end - start)
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


def create_dictionaries():
    every_csv = get_all_csvs()
    state_district_ages = {}
    state_district_incomes = {}

    for csv_filename in every_csv:
        state_name = csv_filename.split('_')[0]
        state_district_ages[state_name] = {}
        state_district_incomes[state_name] = {}
        with open(PATH_TO_CSVS + csv_filename, 'r') as opened_csv:
            state_age_data, state_income_data = get_distributions_from_csv(opened_csv)
            for i, (age, income) in enumerate(zip(state_age_data, state_income_data)):
                age_object = AgeInfo(age)
                income_object = IncomeInfo(income)
                state_district_ages[state_name][i + 1] = age_object
                state_district_incomes[state_name][i + 1] = income_object

    return state_district_ages, state_district_incomes


def most_over_200k(income_dict):
    max_over_200 = -1
    s = ''
    d = 0

    for state in income_dict.keys():
        for district in income_dict[state].keys():
            rich_people_here = income_dict[state][district].over_200
            if  rich_people_here > max_over_200:
                s = state
                d = district
                max_over_200 = rich_people_here

    print('Most over 200k', s, d, max_over_200)


def most_under_10k(income_dict):
    max_under_10 = -1
    s = ''
    d = 0

    for state in income_dict.keys():
        for district in income_dict[state].keys():
            poor_people_here = income_dict[state][district].under_10
            if poor_people_here > max_under_10:
                s = state
                d = district
                max_under_10 = poor_people_here

    print('Most under 10k', s, d, max_under_10)


def main():
    age_dict, income_dict = create_dictionaries()
    with open("age_data.json", "w") as age_output:
        json.dump(age_dict, age_output)
    with open("income_data.json", "w") as income_output:
        json.dump(income_dict, income_output)
    # income_dict = create_income_dictionary()


if __name__ == '__main__':
    main()