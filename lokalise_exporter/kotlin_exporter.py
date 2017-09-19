# Python 2.x retro-compatibility
from __future__ import unicode_literals, print_function, division, absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

# Imports
from collections import OrderedDict
from os import path

from lokalise_exporter import file_len
from lokalise_exporter.properties_utils import read_properties_file_as_dict

default_kotlin_package = "com.yourcompany.yourapp"


def generate_kotlin_strings_table(logger, temp_dir, localization_files, kotlin_package, underscorize_keys):
    package = kotlin_package

    if len(package) == 0:
        package = default_kotlin_package

    max_file_len = 0
    localized_file_to_use = ''

    for kotlin_file in localization_files:
        length = file_len(kotlin_file)
        if length > max_file_len:
            max_file_len = length
            localized_file_to_use = kotlin_file

    logger.info("Generating kotlin strings table from " + localized_file_to_use + " which has "
                + str(max_file_len) + " keys")

    with open(path.join(temp_dir, 'LocalizedKeys.kt'), 'w') as kotlin_file:
        kotlin_file.writelines([
            'package ' + package + '\n',
            '\n',
            'class LocalizedKeys {\n',
            '    companion object {\n',
            '\n'
        ])

        loc_keys = read_properties_file_as_dict(localized_file_to_use, underscorize_keys)
        ordered_keys = OrderedDict(sorted(loc_keys.items()))
        kotlin_file.writelines(['        @JvmField val ' + key + ' = "' + key + '"\n' for key in ordered_keys])

        kotlin_file.writelines([
            '\n',
            '    }\n',
            '}\n'
        ])
