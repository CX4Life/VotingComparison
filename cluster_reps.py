import numpy as np
import hdbscan
import json
import argparse
from sklearn.cluster import KMeans, DBSCAN

SAVED_REP_FILE = 'rep_vectors.npy'
REP_CLASS_JSON = 'rep_class.json'


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
    parser.add_argument('-debug',
                        help='if used, will just print lables without writing to file',
                        action='store_true')
    return parser.parse_args()


def cluster_reps(args, array):
    if args.a == 'kmeans':
        return KMeans(n_clusters=args.c, random_state=0).fit(array).labels_
    elif args.a == 'dbscan':
        return DBSCAN().fit(array).labels_
    elif args.a == 'RSL':
        return hdbscan.RobustSingleLinkage().fit_predict(array)
    elif args.a == 'hdbscan':
        return hdbscan.HDBSCAN(min_cluster_size=10).fit_predict(array)

    return None


def main():
    args = get_args()
    rep_values = np.load(SAVED_REP_FILE)
    class_labels = cluster_reps(args, rep_values)
    if args.debug:
        print(class_labels)
    else:
        with open('sorted_reps.json', 'r') as sr:
            rep_id_list = json.load(sr)

        rep_id_to_class = {}
        for i, class_label in enumerate(class_labels):
            rep_id_to_class[rep_id_list[i]] = int(class_label)

        with open(REP_CLASS_JSON, 'w') as output:
            json.dump(rep_id_to_class, output, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
