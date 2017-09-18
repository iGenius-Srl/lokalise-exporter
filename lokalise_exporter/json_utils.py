from lokalise_exporter import underscorize
import json


def read_json_file_as_dict(file_path, underscorize_keys):
    with open(file_path) as json_file:
        data = json.load(json_file)

    data_out = {}

    for key in data:
        value = str(data[key]).strip()

        key = underscorize(key, underscorize_keys)
        data_out[key] = value

    return data_out


def write_dict_to_json_file(dictionary: 'dict', file_path):
    with open(file_path, 'w') as output:
        json.dump(dictionary, output, sort_keys=True, indent=2)
