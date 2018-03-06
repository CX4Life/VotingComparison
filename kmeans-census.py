import numpy as np
import argparse
from matplotlib import pyplot as plt
import matplotlib
import json
import sys
import hdbscan
from sklearn.cluster import KMeans, DBSCAN

__author__ = 'Tim Woods'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2018, Tim Woods'


JSON_FILENAME = 'combined_data.json'
REP_CLASS_FILENAME = 'rep_class.json'
REP_DISTRICT_FILE = 'districts.json'

A = 'age'
I = 'income'
T1 = 'first_sixth'
T2 = 'second_sixth'
T4 = 'fourth_sixth'
T5 = 'fifth_sixth'
MD = 'median'
AV = 'average'
SD = 'stddev'



def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c',
                        type=int,
                        default=4,
                        help="Number of clusters to use for KMeans")
    parser.add_argument('-a',
                        type=str,
                        choices=['kmeans', 'dbscan', 'RSL', 'hdbscan'],
                        default='hdbscan',
                        help='Which clustering algorithm to use (choices: kmeans, dbscan, RSL, hdbscan)')
    return parser.parse_args()


def load_census_data():
    with open(JSON_FILENAME, 'r') as opened_json:
        census_data = json.load(opened_json)

    return census_data


def array_from_district(single_district):
    return [
        single_district[A][T1],
        single_district[A][T2],
        single_district[A][MD],
        single_district[A][T4],
        single_district[A][T5],
        single_district[I][T1] / 1000.0,
        single_district[I][T2] / 1000.0,
        single_district[I][MD] / 1000.0,
        single_district[I][T4] / 1000.0,
        single_district[I][T5] / 1000.0,
        single_district[A][SD],
        single_district[I][SD] / 1000.0,
    ]


def create_matrix(census_data):
    ret = []
    for state in census_data.keys():
        for district in census_data[state].keys():
            ret.append(array_from_district(census_data[state][district]))

    return np.array(ret)


def cluster_np_array(args, array):
    if args.a == 'kmeans':
        return KMeans(n_clusters=args.c, random_state=0).fit(array).labels_
    elif args.a == 'dbscan':
        return DBSCAN().fit(array).labels_
    elif args.a == 'RSL':
        return hdbscan.RobustSingleLinkage().fit_predict(array)
    elif args.a == 'hdbscan':
        return hdbscan.HDBSCAN(min_cluster_size=10).fit_predict(array)

    return None


def plot_with_labels(np_array, labels):
    def scatterplot(x_data, y_data, color_labels, x_label, y_label, title):
        _, ax = plt.subplots()
        ax.scatter(x_data, y_data, c=color_labels, s=30, alpha=0.8)
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        plt.show()

    x = [x[2] for x in np_array]
    y = [y[7] for y in np_array]
    matplotlib.rc('figure', figsize=(14, 7))
    matplotlib.rc('font', size=14)
    matplotlib.rc('axes.spines', top=False, right=False)
    matplotlib.rc('axes', grid=False)
    matplotlib.rc('axes', facecolor='white')
    scatterplot(x, y, labels, 'Average Age', 'Average Income', 'Age v Income for Districts')

def print_rep_id_from_order_dist(rep_map, dists):
    reps = [rep_map[x] for x in dists]
    print(reps)


def labels_from_rep_class_json():
    with open(REP_CLASS_FILENAME, 'r') as class_file:
        # key-val = repID - class
        rep_classes = json.load(class_file)

    with open(REP_DISTRICT_FILE, 'r') as l:
        # key-val = district-repID
        lookup = json.load(l)

    reverse_lookup = {b: a for a, b in zip(lookup.keys(), lookup.values())}
    ordered_district = sorted(list(lookup.keys()))

    output_classes = [0 for _ in range(len(lookup.keys()))]
    for rep in rep_classes:
        try:
            output_classes[ordered_district.index(reverse_lookup[rep])] = rep_classes[rep]
        except KeyError:
            continue

    print(len(output_classes))
    return output_classes


def main():
    rep_labels = labels_from_rep_class_json()

    args = get_args()
    print('loading data')
    district_census_info = load_census_data()
    print('creating numpy array')
    ready_to_cluster = create_matrix(district_census_info)
    print('clustering...')
    labels = cluster_np_array(args, ready_to_cluster)
    plot_with_labels(ready_to_cluster, labels)
    plot_with_labels(ready_to_cluster, np.array(rep_labels))


if __name__ == '__main__':
    main()
