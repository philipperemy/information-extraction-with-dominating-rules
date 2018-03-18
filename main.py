from __future__ import print_function

import time

import logic
from graph import generate_graphviz_graph
from utils import *


def run(text, apply_domination=True):
    start_time = time.time()
    named_entities = call_ner_api(text)
    relations = call_openie_api(text)

    for rel in relations:
        print(rel)

    organizations = list(set([v[0] for v in named_entities if v[1] == 'ORGANIZATION']))  # unique elements.

    print(organizations)

    filtered_relations = logic.process_entity_relations(relations, organizations, apply_domination)
    for rel in filtered_relations:
        print('{} - {} - {}'.format(rel[0], rel[1], rel[2]))
    print('Program took {0:.2f}s to execute.'.format(time.time() - start_time))

    del relations
    import uuid
    output_filename_png = 'reports/{}'.format(str(uuid.uuid4()))
    generate_graphviz_graph(filtered_relations, organizations, output_filename_png)

    import os
    return os.path.dirname(os.path.realpath(__file__)) + '/' + output_filename_png + '.png'  # dirty but okay.


if __name__ == '__main__':
    filename = '/Users/philipperemy/PycharmProjects/information-extraction/reports/business_insider_google_buys_moodstocks.txt'
    print(run(filename))
