import pymysql
import os
import csv
import time

__license__ = 'MIT'

PATH_TO_CSVS = 'census/'


class AgeInfo:
    def __init__(self, age_data):
        #TODO off by one, only loading first district
        self.total = age_data[0][3]
        self.male = age_data[1][3]
        self.female = age_data[2][3]
        self._under_5 = age_data[3][3]
        self._5_to_9 = age_data[4][3]
        self._10_to_14 = age_data[5][3]
        self._15_to_19 = age_data[6][3]
        self._20_to_24 = age_data[7][3]
        self._25_to_34 = age_data[8][3]
        self._35_to_44 = age_data[9][3]
        self._45_to_54 = age_data[10][3]
        self._55_to_64 = age_data[11][3]
        self._65_to_74 = age_data[12][3]
        self._75_to_84 = age_data[13][3]
        self._85_plus = age_data[14][3]
        self.median = age_data[15][3]
        self._18_plus = age_data[16][3]
        self._65_plus = age_data[17][3]

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
        print(self._55_to_64)
        print(self._65_to_74)
        print(self._75_to_84)
        print(self._85_plus)
        print('median', self.median)
        print(self._18_plus)
        print(self._65_plus)



def get_all_csvs():
    return os.listdir(PATH_TO_CSVS)


def get_age_distribution_from_csv(opened_csv):
    census_reader = csv.reader(opened_csv)
    age_data = []

    for row in census_reader:
        if row and row[0] == 'People' and row[1] == 'Sex and Age':
            age_data.append(row)

    assert age_data
    return age_data


def main():
    every_csv = get_all_csvs()
    for csv_filename in every_csv:
        with open(PATH_TO_CSVS + csv_filename, 'r') as opened_csv:
            print(csv_filename)

            this_age_data = get_age_distribution_from_csv(opened_csv)
            new_age_object = AgeInfo(this_age_data)
            new_age_object.show_stuff()
            exit(0)


if __name__ == '__main__':
    main()