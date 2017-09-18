import zipfile
from collections import namedtuple
from distutils.dir_util import remove_tree, copy_tree
from os import scandir, path
import colorlog


# Custom data types

LokaliseProject = namedtuple('LokaliseProject', ['projectID', 'zippedFileName'])


# Utility functions

def init_logger(debug):
    logger = colorlog.getLogger()

    if debug:
        logger.setLevel(colorlog.colorlog.logging.DEBUG)
    else:
        logger.setLevel(colorlog.colorlog.logging.INFO)

    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(fmt="%(log_color)s%(levelname)s %(message)s"))
    logger.addHandler(handler)

    return logger


def underscorize(value, underscorize_keys):
    stripped = str(value).strip()

    if underscorize_keys:
        return stripped.replace('-', '_')

    return stripped


def list_files_in_dir(dir_path):
    return [f.name for f in scandir(dir_path) if f.is_file()]


def intersect_dict(dict_a: 'dict', dict_b: 'dict'):
    keys_a = set(dict_a.keys())
    keys_b = set(dict_b.keys())
    return keys_a & keys_b


def copy_files_to_output_directory(logger, clean_output_path_before_export, temp_dir, output_path):
    if clean_output_path_before_export and path.exists(output_path):
        logger.info("Cleaning output path before export: " + output_path)
        remove_tree(output_path)

    logger.info("Copying exported files into: " + output_path)
    copy_tree(temp_dir, output_path)


def parse_projects_to_export(input_str):
    if not input_str or not isinstance(input_str, str):
        return []

    projects = str(input_str).split(",")

    return [entry.strip() for entry in projects]


def unzip_file(file, output_dir):
    with zipfile.ZipFile(file, "r") as zipped:
        zipped.extractall(output_dir)
