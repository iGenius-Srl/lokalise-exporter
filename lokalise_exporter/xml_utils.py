# Python 2.x retro-compatibility
from __future__ import unicode_literals, print_function, division, absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

# Imports
from collections import OrderedDict
import xmltodict

from lokalise_exporter import underscorize


def read_xml_strings_file_as_dict(file_path, underscorize_keys):
    with open(file_path, 'r') as xml_file:
        xml = xmltodict.parse(xml_file.read())
        strings = xml['resources']['string']

        dictionary = {}

        for string in strings:
            key = underscorize(string['@name'], underscorize_keys)
            dictionary[key] = string['#text']

        return dictionary


def write_dict_to_xml_strings_file(dictionary, file_path):
    ordered_dictionary = OrderedDict(sorted(dictionary.items()))
    with open(file_path, 'w') as xml_file:
        xml_file.writelines([
            '<?xml version="1.0" encoding="UTF-8"?>\n',
            '<resources>\n'
        ])

        xml_file.writelines('  <string name="{}">{}</string>\n'.format(key, value)
                        for key, value in ordered_dictionary.items())

        xml_file.writelines('</resources>\n')
