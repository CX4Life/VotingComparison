import numpy as np
import hdbscan
import argparse
from sklearn.cluster import KMeans, DBSCAN

SAVED_REP_FILE = 'rep_vectors.npy'


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
    print(cluster_reps(args, rep_values))


if __name__ == '__main__':
    main()
