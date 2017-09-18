import begin
import colorlog
from requests import post, get
from tempfile import TemporaryDirectory
from distutils.dir_util import copy_tree, remove_tree
from os import path, makedirs, remove
from uuid import uuid4
from time import sleep
import zipfile


lokalise_format_mapping = {
    'json': 'json',
    'ios': 'strings',
    'android': 'xml',
    'kotlin': 'properties'
}


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


def parse_projects_to_export(input_str):
    if not input_str or not isinstance(input_str, str):
        return []

    projects = str(input_str).split(",")

    return [entry.strip() for entry in projects]


def get_output_path(output_path: 'str'):
    out_path = path.abspath(output_path)
    makedirs(out_path, exist_ok=True)

    return out_path


def unzip_file(file, output_dir):
    with zipfile.ZipFile(file, "r") as zipped:
        zipped.extractall(output_dir)


def download_file(logger, temp_dir, file_to_download, timeout):
    download_path = path.join(temp_dir, uuid4().hex)
    logger.debug("Downloading %s in %s", file_to_download, download_path)

    download_request = get(file_to_download, stream=True, timeout=timeout)

    if download_request.status_code == 200:
        with open(download_path, 'wb') as file:
            for chunk in download_request.iter_content(1024):
                file.write(chunk)
        logger.debug("Downloaded %s in %s", file_to_download, download_path)
        return download_path

    else:
        raise RuntimeError("Error while downloading " + file_to_download + ". HTTP status "
                           + str(download_request.status_code))


def export_project(logger, temp_dir, api_key, project_id, export_type, timeout):
    logger.info("Exporting project %s", project_id)

    endpoint = "https://lokalise.co/api/project/export"
    post_params = {
        'id': project_id,
        'api_token': api_key,
        'type': lokalise_format_mapping[export_type],
        'bundle_structure': '%LANG_ISO%.%FORMAT%',
        'export_empty': 'skip'
    }

    logger.debug("Sending POST %s with data: %s", endpoint, post_params)

    response = post(endpoint, data=post_params, timeout=timeout).json()

    if response['response']['status'] == 'error':
        resp = response['response']
        raise RuntimeError("lokalise error " + str(resp['code']) + ": " + resp['message'])

    file_to_download = "https://s3-eu-west-1.amazonaws.com/lokalise-assets/" + response['bundle']['file']
    logger.debug("project %s will be exported from %s", project_id, file_to_download)

    downloaded_file = download_file(logger, temp_dir, file_to_download, timeout)
    logger.info("Project %s exported", project_id)
    return downloaded_file


def export_projects(logger, temp_dir, projects, api_key, export_format, timeout):
    exported_project_files = []

    for index, project in enumerate(projects):
        exported_project_files.append(export_project(logger, temp_dir, api_key, project, export_format, timeout))

        if not index == len(projects) - 1:
            logger.info("Waiting 5s because of the lokalise.co flood detector...")
            sleep(5)

    return exported_project_files


def unzip_exported_projects(logger, temp_dir, exported_project_files):
    unzipped_dirs = []

    for zip_file in exported_project_files:
        unzipped_dir = path.join(temp_dir, uuid4().hex)
        logger.debug("Unzipping " + zip_file + " in " + unzipped_dir)

        unzip_file(zip_file, unzipped_dir)
        remove(zip_file)
        unzipped_dirs.append(unzipped_dir)

        logger.debug("Unzipped " + zip_file + " in " + unzipped_dir)

    return unzipped_dirs


def copy_files_to_output_directory(logger, clean_output_path_before_export, temp_dir, output_path):
    if clean_output_path_before_export and path.exists(output_path):
        logger.info("Cleaning output path before export: " + output_path)
        remove_tree(output_path)

    logger.info("Copying exported files into: " + output_path)
    copy_tree(temp_dir, output_path)


@begin.start(auto_convert=True, lexical_order=True)
def main(api_key: 'lokalise.co API key',
         projects_to_export: 'comma separated list of project IDs to be exported',
         export_format: 'exported format. It can be json, ios, android or kotlin',
         output_path: 'export absolute path. It will create needed directories' = "",
         underscorize_localization_keys: 'replaces - with _ in all the localization keys' = True,
         clean_output_path_before_export: 'wipes the output path before exporting new data' = False,
         merge_strings: 'for each language, merges all the strings from all the projects, removing duplicates' = True,
         debug: 'true to enable debugging output' = False,
         timeout: 'timeout in seconds for each request' = 10):

    logger = init_logger(debug)
    projects = parse_projects_to_export(projects_to_export)

    if export_format not in lokalise_format_mapping:
        logger.error("export_format must be one of the following: %s", ",".join(lokalise_format_mapping.keys()))
        return -1

    logger.debug("Using API Key: %s", api_key)
    logger.debug("Exporting format: %s", format)
    logger.debug("Output path: %s", output_path)
    logger.debug("Projects to export: %s", projects)

    try:
        with TemporaryDirectory(prefix="lokalise-exporter") as temp_dir:
            exported_project_files = export_projects(logger, temp_dir, projects, api_key, export_format, timeout)
            project_directories = unzip_exported_projects(logger, temp_dir, exported_project_files)
            logger.info(project_directories)

            copy_files_to_output_directory(logger, clean_output_path_before_export, temp_dir, output_path)

            logger.info("Done!")

    except Exception as exc:
        logger.error("Export failed! Don't worry, output path is untouched: " + output_path)
        logger.error(exc)
        return -2
