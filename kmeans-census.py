import numpy as np
import argparse
from matplotlib import pyplot as plt
import matplotlib
import json
from sklearn.cluster import KMeans

__author__ = 'Tim Woods'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2018, Tim Woods'


JSON_FILENAME = 'combined_data.json'
ALGO_LOOKUP = {
    'kmeans': KMeans
}

A = 'age'
I = 'income'
FQ = 'first_quart'
MD = 'median'
AV = 'average'
TQ = 'third_quart'
SD = 'stddev'



def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c',
                        type=int,
                        default=4,
                        help="Number of clusters to use for KMeans")
    parser.add_argument('-a',
                        type=str,
                        choices=['kmeans'],
                        default='kmeans',
                        help='Which clustering algorithm to use (choices: KMeans)')
    return parser.parse_args()


def load_census_data():
    census_data = None
    with open(JSON_FILENAME, 'r') as opened_json:
        census_data = json.load(opened_json)

    return census_data


def array_from_district(single_district):
    return [
        single_district[A][FQ],
        single_district[A][MD],
        single_district[A][TQ],
        single_district[I][FQ],
        single_district[I][MD],
        single_district[I][TQ]
    ]


def create_matrix(census_data):
    ret = []
    for state in census_data.keys():
        for district in census_data[state].keys():
            ret.append(array_from_district(census_data[state][district]))

    return np.array(ret)


def cluster_np_array(args, array):
    cluster = ALGO_LOOKUP[args.a](n_clusters=args.c, random_state=0).fit(array)
    return cluster.labels_


def plot_with_labels(np_array, labels):
    def scatterplot(x_data, y_data, color_labels, x_label, y_label, title):
        _, ax = plt.subplots()
        ax.scatter(x_data, y_data, c=color_labels, s=30, alpha=0.8)
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        plt.show()

    x = [x[1] for x in np_array]
    y = [y[4] for y in np_array]
    matplotlib.rc('figure', figsize=(14, 7))
    matplotlib.rc('font', size=14)
    matplotlib.rc('axes.spines', top=False, right=False)
    matplotlib.rc('axes', grid=False)
    matplotlib.rc('axes', facecolor='white')
    scatterplot(x, y, labels, 'Average Age', 'Average Income', 'Age v Income for Districts')

def main():
    args = get_args()
    print('loading data')
    district_census_info = load_census_data()
    print('creating numpy array')
    ready_to_cluster = create_matrix(district_census_info)
    print('clustering...')
    labels = cluster_np_array(args, ready_to_cluster)
    plot_with_labels(ready_to_cluster, labels)


if __name__ == '__main__':
    main()
