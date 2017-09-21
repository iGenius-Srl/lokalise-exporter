# Python 2.x retro-compatibility
from __future__ import unicode_literals, print_function, division, absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

# Imports
from collections import OrderedDict
import xmltodict

from lokalise_exporter import underscorize, read_file, write_file


def read_xml_strings_file_as_dict(logger, file_path, underscorize_keys):
    with read_file(file_path) as xml_file:
        xml = xmltodict.parse(xml_file.read())
        strings = xml['resources']['string']

        dictionary = {}

        for string in strings:
            key = underscorize(string['@name'], underscorize_keys)

            if '#text' not in string:
                logger.error("Skipped key " + key + " from " + file_path + " because it's empty!!")
            else:
                value = string['#text'].strip()
                if len(value) == 0:
                    logger.error("Skipped key " + key + " from " + file_path + " because it's empty!!")
                else:
                    dictionary[key] = escape_xml_value(value)

        return dictionary


def write_dict_to_xml_strings_file(dictionary, file_path):
    ordered_dictionary = OrderedDict(sorted(dictionary.items()))
    with write_file(file_path) as xml_file:
        xml_file.writelines([
            '<?xml version="1.0" encoding="UTF-8"?>\n',
            '<resources>\n'
        ])

        xml_file.writelines('  <string name="{}">{}</string>\n'.format(key, value)
                        for key, value in ordered_dictionary.items())

        xml_file.writelines('</resources>\n')


def escape_xml_value(text):
    if "&" in text:
        text = text.replace("&", "&amp;")
    if "<" in text:
        text = text.replace("<", "&lt;")
    if ">" in text:
        text = text.replace(">", "&gt;")
    if "\"" in text:
        text = text.replace("\"", "&quot;")
    elif "'" in text:
        text = text.replace("'", "&quot;")
    if "\n" in text:
        text = text.replace("\n", "&#10;")
    return text.encode('utf-8', "xmlcharrefreplace").decode('utf-8')
