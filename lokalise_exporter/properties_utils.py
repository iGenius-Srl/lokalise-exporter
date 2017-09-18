from collections import OrderedDict

from lokalise_exporter import underscorize


def read_properties_file_as_dict(file_path, underscorize_keys):
    properties = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.rstrip()  # removes trailing whitespace and '\n' chars

            if line.startswith("#") or "=" not in line:
                continue  # skips blanks and comments

            key, value = line.split("=", 1)
            key = underscorize(key, underscorize_keys)
            value = str(value).strip()

            properties[key] = value

    return properties


def write_dict_to_properties_file(dictionary: 'dict', file_path):
    ordered_dictionary = OrderedDict(sorted(dictionary.items()))
    with open(file_path, 'w') as file:
        file.writelines('{} = {}\n'.format(key, value) for key, value in ordered_dictionary.items())
