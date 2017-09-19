# Python 2.x retro-compatibility
from __future__ import unicode_literals, print_function, division, absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

# Imports
from collections import OrderedDict

from lokalise_exporter import underscorize


def read_properties_file_as_dict(file_path, underscorize_keys):
    properties = {}

    with open(file_path, 'r') as prop_file:
        for line in prop_file:
            line = line.rstrip()  # removes trailing whitespace and '\n' chars

            if line.startswith("#") or "=" not in line:
                continue  # skips blanks and comments

            key, value = line.split("=", 1)
            key = underscorize(key, underscorize_keys)
            value = str(value).strip()

            properties[key] = value

    return properties


def write_dict_to_properties_file(dictionary, file_path):
    ordered_dictionary = OrderedDict(sorted(dictionary.items()))
    with open(file_path, 'w') as prop_file:
        prop_file.writelines('{} = {}\n'.format(key, value) for key, value in ordered_dictionary.items())
