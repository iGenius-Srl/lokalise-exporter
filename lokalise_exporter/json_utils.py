# Python 2.x retro-compatibility
from __future__ import unicode_literals, print_function, division, absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

# Imports
from lokalise_exporter import read_file, underscorize, write_file
import json


def read_json_file_as_dict(logger, file_path, underscorize_keys):
    with read_file(file_path) as json_file:
        data = json.load(json_file, encoding='utf-8')

    data_out = {}

    for key in data:
        value = str(data[key]).strip()

        key = underscorize(key, underscorize_keys)
        value = value.strip()

        if len(value) == 0:
            logger.error("Skipped key " + key + " from " + file_path + " because it's empty!!")
        else:
            data_out[key] = value.strip()

    return data_out


def write_dict_to_json_file(dictionary, file_path):
    with write_file(file_path) as json_file:
        json.dump(dictionary, json_file, sort_keys=True, indent=2, ensure_ascii=False)
