from matplotlib import pyplot as plt
import matplotlib
import json

SAMPLE_DATA = 'sample_plot.json'
REAL_DATA = 'combined_data.json'

def dict_from_json(filename):
    dict = None
    with open(filename, 'r') as open_json:
        dict = json.load(open_json)
    return dict


def x_y_from_json(filename):
    dict = dict_from_json(filename)
    assert dict is not None
    x_data = []
    y_data = []
    for state in dict.keys():
        districts_this_state = dict[state]
        for district_num in districts_this_state:
            district = dict[state][district_num]
            x_data.append(district['age']['average'])
            y_data.append(district['income']['average'])

    return x_data, y_data


def scatterplot(x_data, y_data, x_label, y_label, title):
    _, ax = plt.subplots()
    ax.scatter(x_data, y_data, s=30, color='red', alpha=0.8)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()


def main():
    """Plot sample JSON data for age and income of districts"""
    x, y = x_y_from_json(REAL_DATA)
    matplotlib.rc('figure', figsize= (14, 7))
    matplotlib.rc('font', size=14)
    matplotlib.rc('axes.spines', top=False, right=False)
    matplotlib.rc('axes', grid=False)
    matplotlib.rc('axes', facecolor='white')
    scatterplot(x, y, 'Average Age', 'Average Income', 'Age v Income for Districts')


if __name__ == '__main__':
    main()
