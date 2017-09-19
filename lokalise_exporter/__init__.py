# Python 2.x retro-compatibility
from __future__ import unicode_literals, print_function, division, absolute_import

from builtins import *
from future import standard_library
standard_library.install_aliases()

try:
    from os import scandir
except:
    import scandir as scandir

# Imports
import zipfile
from collections import namedtuple
from distutils.dir_util import remove_tree, copy_tree
from requests import get
from os import path
from uuid import uuid4
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
        return stripped.replace('-', '_').replace('.', '_')

    return stripped


def list_files_in_dir(dir_path):
    return [f.name for f in scandir(dir_path) if f.is_file()]


def intersect_dict(dict_a, dict_b):
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
    return [entry.strip() for entry in input_str.split(",")]


def download_file(logger, temp_dir, file_to_download, timeout):
    download_path = path.join(temp_dir, uuid4().hex)
    logger.debug("Downloading %s in %s", file_to_download, download_path)

    download_request = get(file_to_download, stream=True, timeout=timeout)

    if download_request.status_code == 200:
        with open(download_path, 'wb') as output_file:
            for chunk in download_request.iter_content(1024):
                output_file.write(chunk)
        logger.debug("Downloaded %s in %s", file_to_download, download_path)
        return download_path

    else:
        raise RuntimeError("Error while downloading " + file_to_download + ". HTTP status "
                           + str(download_request.status_code))


def unzip_file(file, output_dir):
    with zipfile.ZipFile(file, "r") as zipped:
        zipped.extractall(output_dir)


def file_len(fname):
    i = 0
    with open(fname, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i + 1
