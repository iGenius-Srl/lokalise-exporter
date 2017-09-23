# Python 2.x retro-compatibility
from __future__ import unicode_literals, print_function, division, absolute_import
from builtins import *
from future import standard_library
from string import Template

standard_library.install_aliases()

# Imports
from collections import OrderedDict
from os import path, makedirs

from lokalise_exporter import file_len, write_file, read_template
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

    package_dir = package.replace('.', path.sep)
    out_dir = path.join(temp_dir, 'kotlin', package_dir)
    makedirs(out_dir)

    generated_file_name = 'LocalizedKeys.kt'

    with write_file(path.join(out_dir, generated_file_name)) as kotlin_file:
        template = read_template(generated_file_name).replace('$package', package)
        kotlin_file.write(template)

        kotlin_file.writelines([
            '\nclass LocalizedKeys {\n',
            '    companion object {\n',
            '\n'
        ])

        loc_keys = read_properties_file_as_dict(logger, localized_file_to_use, underscorize_keys)
        ordered_keys = OrderedDict(sorted(loc_keys.items()))
        kotlin_file.writelines(['        @JvmField val ' + key + ' = "' + key + '"\n' for key in ordered_keys])

        kotlin_file.writelines([
            '\n',
            '    }\n',
            '}\n'
        ])
