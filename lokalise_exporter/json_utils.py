# Python 2.x retro-compatibility
from __future__ import unicode_literals, print_function, division, absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

# Imports
from lokalise_exporter import underscorize
import json


def read_json_file_as_dict(file_path, underscorize_keys):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file, encoding='utf-8')

    data_out = {}

    for key in data:
        value = str(data[key]).strip()

        key = underscorize(key, underscorize_keys)
        data_out[key] = value

    return data_out


def write_dict_to_json_file(dictionary, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(dictionary, json_file, sort_keys=True, indent=2, encoding='utf-8')
