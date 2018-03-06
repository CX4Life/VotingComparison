import json
import os
import numpy

REP_FILE = 'rep_sentiments.json'
OUTPUT_FILE = 'indexed_sentiments.json'
SAVE_NUMPY = 'rep_vectors.npy'

def get_entities():
    seen_ents = set()
    with open(REP_FILE, 'r') as rf:
        sentiments = json.load(rf)

    for rep in sentiments.keys():
        for ent in sentiments[rep]:
            seen_ents.add(ent)

    return sorted(list(seen_ents)), sentiments


def make_map_from_list_of_ents(ents):
    foo = {}
    for i, e in enumerate(ents):
        foo[e] = i

    return foo


def clean_map(original_dict, key_index_map):
    final = {}
    for rep in original_dict.keys():
        final[rep] = {}
        for ent in original_dict[rep].keys():
            score = original_dict[rep][ent]
            final[rep][key_index_map[ent]] = score

    return final


def num_of_ents(int_key_dict):
    ret = 0
    for rep in int_key_dict.keys():
        ids = [int(x) for x in int_key_dict[rep].keys()]
        ret = max(ret, max(ids))
    return ret


def np_array_for_rep(representative_dict, num_of_ents):
    py_list = [0 for _ in range(num_of_ents + 1)]
    for id in representative_dict.keys():
        py_list[int(id)] = float(representative_dict[id])

    return numpy.array(py_list)


def rep_lookup(int_key_dict):
    return sorted([x for x in int_key_dict.keys()])


def main():
    if not os.path.isfile(OUTPUT_FILE):
        sorted_ents, original = get_entities()
        key_to_index = make_map_from_list_of_ents(sorted_ents)
        by_index = clean_map(original, key_to_index)
        with open(OUTPUT_FILE, 'w') as givr:
            json.dump(by_index, givr, indent=2)

    with open(OUTPUT_FILE, 'r') as vect_dict:
        rep_vector_dict = json.load(vect_dict)

    n = num_of_ents(rep_vector_dict)
    list_of_reps = [0 for _ in range(len(rep_vector_dict.keys()))]
    lookup_rep_index = rep_lookup(rep_vector_dict)

    for i, single_rep in enumerate(list(rep_vector_dict.keys())):
        a = np_array_for_rep(rep_vector_dict[single_rep], n)
        list_of_reps[lookup_rep_index.index(single_rep)] = a

    rep_arrays = numpy.array(list_of_reps)
    numpy.save(SAVE_NUMPY, rep_arrays)
    with open('sorted_reps.json', 'w') as dump_reps:
        json.dump(lookup_rep_index, dump_reps, indent=2)


if __name__ == '__main__':
    main()
