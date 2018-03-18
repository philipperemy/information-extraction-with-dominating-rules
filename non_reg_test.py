from __future__ import print_function

import time

import logic
from graph import generate_graphviz_graph
from utils import *

if __name__ == '__main__':
    start_time = time.time()
    filename = '/Users/philipperemy/PycharmProjects/information-extraction/reports/bernstein_med_1.txt'
    named_entities = call_ner_api(filename)
    relations = call_openie_api(filename)

    for rel in relations:
        print(rel)

    organizations = list(set([v[0] for v in named_entities if v[1] == 'ORGANIZATION']))  # unique elements.

    print(organizations)

    filtered_relations = logic.process_entity_relations(relations, organizations)
    for rel in filtered_relations:
        print('{} - {} - {}'.format(rel[0], rel[1], rel[2]))
    print('Program took {0:.2f}s to execute.'.format(time.time() - start_time))

    # pickle.dump(filtered_relations, open('filtered_relations.pkl', 'w'))
    # pickle.dump(organizations, open('organizations.pkl', 'w'))

    check = ''
    for rel in filtered_relations:
        check += '{} - {} - {}'.format(rel[0], rel[1], rel[2])

    import pickle

    filtered_relations_before = pickle.load(open('reg.p', 'r'))
    # pickle.dump(filtered_relations, open('reg.p', 'w'))

    for i, rel in enumerate(filtered_relations):
        if filtered_relations[i] != filtered_relations_before[i]:
            print('DIFF: before = {}, after = {}'.format(filtered_relations_before[i], filtered_relations[i]))

    del relations
    generate_graphviz_graph(filtered_relations, organizations, 'reports/bernstein_med_1')
