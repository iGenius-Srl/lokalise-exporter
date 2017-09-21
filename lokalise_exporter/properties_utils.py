# Python 2.x retro-compatibility
from __future__ import unicode_literals, print_function, division, absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

# Imports
from collections import OrderedDict

from lokalise_exporter import underscorize, read_file, write_file


def read_properties_file_as_dict(logger, file_path, underscorize_keys):
    properties = {}

    with read_file(file_path) as prop_file:
        for line in prop_file:
            line = line.rstrip()  # removes trailing whitespace and '\n' chars

            if line.startswith("#") or "=" not in line:
                continue  # skips blanks and comments

            key, value = line.split("=", 1)
            key = underscorize(key, underscorize_keys)
            value = value.strip()

            if len(value) == 0:
                logger.error("Skipped key " + key + " from " + file_path + " because it's empty!!")
            else:
                properties[key] = value

    return properties


def write_dict_to_properties_file(dictionary, file_path):
    ordered_dictionary = OrderedDict(sorted(dictionary.items()))
    with write_file(file_path) as prop_file:
        prop_file.writelines('{} = {}\n'.format(key, value) for key, value in ordered_dictionary.items())
