from __future__ import print_function

import numpy as np


# BSX has finally turned ---- corner
# BSX has finally turned from ---- perspective
# BSX has finally turned corner from ---- perspective
def layer_filter_domination(entity_relations, known_entities):
    altered_count = 0
    domination_dict = dict()
    last_rel_dict = dict()
    relations_to_discard = []
    # domination of order 1. keys match.
    for i, rel in enumerate(entity_relations):
        key = ''.join(rel[0] + rel[1])
        if key in domination_dict:
            max_len = len(domination_dict[key])
            cur_len = len(rel[2])
            if cur_len > max_len:
                relations_to_discard.append(last_rel_dict[key])
                last_rel_dict[key] = i
                domination_dict[key] = rel[2]
            else:
                relations_to_discard.append(i)
        else:
            last_rel_dict[key] = i
            domination_dict[key] = rel[2]

    new_entity_relations = []
    for i, rel in enumerate(entity_relations):
        if i not in relations_to_discard:
            new_entity_relations.append(rel)
        else:
            altered_count += 1

    entity_relations = new_entity_relations
    domination_dict = dict()
    for rel in entity_relations:
        key = ''.join(rel[0] + rel[1])
        domination_dict[key] = rel[1] + ' ' + rel[2]

    # domination of order 2. subset match.
    keys = list(domination_dict.keys())
    indexes_to_discard = []
    for rel in entity_relations:
        key = ''.join(rel[0] + rel[1])
        indexes = np.where(np.array([(key in v) for v in keys]) > 0)[0]
        max_len = []
        for idx in indexes:
            max_len.append(len(domination_dict[keys[idx]]))

        index_to_keep = indexes[np.array(max_len).argmax()]
        indexes_to_discard.extend(set(indexes) - {index_to_keep})

    for i in np.unique(np.array(indexes_to_discard)):
        del domination_dict[keys[i]]
        altered_count += 1

    new_entity_relations = []
    for i, rel in enumerate(entity_relations):
        key = ''.join(rel[0] + rel[1])
        if key in domination_dict:
            new_entity_relations.append(rel)

    return new_entity_relations, altered_count


def layer_resolve_nouns(entity_relations, known_entities):
    keywords = ['company', 'division']
    exact_match_keywords = ['it']
    last_known_entity_stack = []
    altered_count = 0
    for rel in entity_relations:
        entity = rel[0]
        lower_entity = entity.lower()
        if 'our' in lower_entity.split():
            new_rel = [last_known_entity_stack[-1], lower_entity.split('our', 1)[1], rel[1] + ' ' + rel[2]]
            rel[0] = new_rel[0]
            rel[1] = new_rel[1]
            rel[2] = new_rel[2]
            altered_count += 1
        for keyword in keywords:
            if keyword in entity:
                rel[0] = last_known_entity_stack[-1]
                altered_count += 1
            if keyword in rel[2]:
                rel[2] = rel[2].replace(keyword, last_known_entity_stack[-1])
                altered_count += 1
        for exact_match_keyword in exact_match_keywords:
            if exact_match_keyword == rel[0]:
                rel[0] = last_known_entity_stack[-1]
            if exact_match_keyword == rel[2]:
                rel[2] = last_known_entity_stack[-1]
        if entity in known_entities:
            last_known_entity_stack.append(entity)

    return entity_relations, altered_count


def match_entity(initial_candidate, known_entities):
    candidate = initial_candidate
    first_letters = [v[0] if v.upper() != v else v for v in candidate.split()]
    all_chars = ''.join(first_letters)
    if len(set(all_chars) - set(all_chars.lower())) > 1:
        for sub_entity in candidate.split():
            if sub_entity in known_entities:
                return sub_entity
        acronym = filter(str.isupper, candidate)
        dict_acronyms = [[i, filter(str.isupper, v)] for i, v in enumerate(known_entities) if
                         len(v.split()) > 1 or v.upper() == v]
        for key, val in dict(dict_acronyms).items():
            if val == acronym:
                return known_entities[key]

    if initial_candidate == candidate:
        # no changes.
        for known_entity in known_entities:
            if known_entity in candidate:
                return known_entity
    return candidate


def layer_process_entities(entity_relations, known_entities):
    altered_count = 0
    for rel in entity_relations:
        new_entities = []
        for entity in [rel[0], rel[2]]:
            new_entity = match_entity(entity, known_entities)
            altered = entity != new_entity
            altered_count += int(altered)
            if altered:
                print('{} -> {}'.format(entity, new_entity))
            new_entities.append(new_entity)
        rel[0], rel[2] = new_entities
    return entity_relations, altered_count


def layer_clean_spaces(entity_relations, known_entities):
    for rel in entity_relations:
        rel[0] = rel[0].strip()
        rel[1] = rel[1].strip().lower()
        rel[2] = rel[2].strip()
    return entity_relations, 0


def layer_clean_simple_rules(entity_relations, known_entities):
    relations_to_discard = []
    short_words_to_discard = ['of', 'to']
    redundant_words_to_discard = ['also', 'thus']

    redundant_dict = dict()
    for i, rel in enumerate(entity_relations):
        key = ''.join(rel[0] + rel[1])
        redundant_dict[key] = i

    # Remove relations of the form
    # American Medical Systems -  makes -
    # American Medical Systems -  also makes -
    # American Medical Systems -  thus makes -
    # American Medical Systems - of -
    for i, rel in enumerate(entity_relations):
        if rel[2].startswith(rel[1]):
            relations_to_discard.append(i)
        elif rel[1] in short_words_to_discard:
            relations_to_discard.append(i)
        else:
            redundant_words_in_rel = [redundant_word for redundant_word in redundant_words_to_discard if
                                      redundant_word in rel[1].split()]
            if len(redundant_words_in_rel) > 0:
                str_relation = rel[1]
                for w in redundant_words_in_rel:
                    str_relation = str_relation.replace(w, '').replace('  ', ' ')
                prev_key = ''.join(rel[0] + str_relation.strip())
                if prev_key in redundant_dict and entity_relations[redundant_dict[prev_key]][2] == rel[2]:
                    relations_to_discard.append(i)

    # if e[0] == e[1]
    for i, rel in enumerate(entity_relations):
        if rel[0].lower() == rel[1].lower():
            relations_to_discard.append(i)

    # discard small e[1]
    for i, rel in enumerate(entity_relations):
        if len(rel[1]) < 2:
            relations_to_discard.append(i)

    # remove circular relations
    for i, rel in enumerate(entity_relations):
        if rel[2].lower() == rel[0].lower():
            relations_to_discard.append(i)

    # discard them here.
    new_entity_relations = []
    for i, rel in enumerate(entity_relations):
        if i not in relations_to_discard:
            new_entity_relations.append(rel)

    return new_entity_relations, len(relations_to_discard)


def filter_weird_entities(entity_relations, known_entities):
    # could be improved
    weird_entities = ['current']
    relations_to_discard = []
    for i, rel in enumerate(entity_relations):
        for weird_entity in weird_entities:
            if weird_entity == rel[0].lower():
                relations_to_discard.append(i)

    # discard them here.
    new_entity_relations = []
    for i, rel in enumerate(entity_relations):
        if i not in relations_to_discard:
            new_entity_relations.append(rel)
    return new_entity_relations, len(relations_to_discard)


LAYERS = [layer_clean_spaces, layer_process_entities, layer_resolve_nouns, layer_filter_domination,
          layer_clean_spaces, layer_clean_simple_rules, filter_weird_entities]


def process_entity_relations(entity_relations, entities, apply_domination=True):
    entity_relations, altered_count = layer_clean_spaces(entity_relations, entities)
    for layer_ptr in LAYERS:
        if apply_domination:
            entity_relations, altered_count = layer_ptr(entity_relations, entities)
            print('{} relations were altered by the layer <{}(..)>'.format(altered_count, layer_ptr.__name__))
    return entity_relations
