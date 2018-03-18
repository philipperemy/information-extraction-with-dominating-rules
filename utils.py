from __future__ import print_function

import os
import uuid

from ner.main import stanford_ner
from openie.main import stanford_ie


def text_to_file(text):
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    tmp_filename = str(uuid.uuid4()) + '.txt'
    full_tmp_filename = 'tmp/{}'.format(tmp_filename)
    with open(full_tmp_filename, 'w') as f:
        f.write(text)
    return full_tmp_filename


def release_handle(tmp_filename):
    os.remove(tmp_filename)


def call_api(text, ner=True):
    absolute_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    if os.path.isfile(text):
        full_tmp_filename = text
    else:
        full_tmp_filename = absolute_path + text_to_file(text)
    if ner:
        results = stanford_ner(full_tmp_filename, verbose=False, absolute_path=absolute_path + 'ner/')
    else:
        results = stanford_ie(full_tmp_filename, verbose=False, absolute_path=absolute_path + 'openie/')
    return results


def call_ner_api(filename_or_text):
    return call_api(filename_or_text, ner=True)


def call_openie_api(filename_or_text):
    return call_api(filename_or_text, ner=False)
