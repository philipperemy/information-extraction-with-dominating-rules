from __future__ import print_function

import os
import uuid

from ner.main import stanford_ner
from openie.main import stanford_ie

TMP_DIR = '/tmp/'


def text_to_file(text):
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
    tmp_filename = str(uuid.uuid4()) + '.txt'
    full_tmp_filename = os.path.join(TMP_DIR, tmp_filename)
    with open(full_tmp_filename, 'w') as f:
        f.write(text)
    return full_tmp_filename


def release_handle(tmp_filename):
    os.remove(tmp_filename)


def call_api(text, ner=True):
    tmp_filename = text_to_file(text)
    if ner:
        absolute_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ner') + '/'
        results = stanford_ner(tmp_filename, verbose=True, absolute_path=absolute_path)
    else:
        results = stanford_ie(tmp_filename, verbose=True)
    return results


def call_ner_api(filename_or_text):
    return call_api(filename_or_text, ner=True)


def call_openie_api(filename_or_text):
    return call_api(filename_or_text, ner=False)


if __name__ == '__main__':
    print(text_to_file('Hello'))
