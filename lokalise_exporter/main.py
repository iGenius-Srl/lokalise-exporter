# Python 2.x retro-compatibility
from __future__ import unicode_literals, print_function, division, absolute_import
from future import standard_library

standard_library.install_aliases()

try:
    from tempfile import TemporaryDirectory
except:
    from backports.tempfile import TemporaryDirectory

# Imports
import begin
from requests import post
from os import makedirs, remove
from time import sleep
from lokalise_exporter import *
from lokalise_exporter.json_utils import *
from lokalise_exporter.kotlin_exporter import *
from lokalise_exporter.properties_utils import *
from lokalise_exporter.xml_utils import *


def get_output_localization_file(temp_dir, localization_file):
    return path.join(temp_dir, localization_file)


def get_ios_output_localization_file(temp_dir, localization_file):
    localizable_strings_dir = path.join(temp_dir, localization_file.replace('.strings', '.lproj'))
    makedirs(localizable_strings_dir)
    return path.join(localizable_strings_dir, 'Localizable.strings')


def get_android_output_localization_file(temp_dir, localization_file):
    locale_name = localization_file.replace('.xml', '').replace('_', '-r')

    if locale_name == 'en':
        localizable_strings_dir = path.join(temp_dir, 'values')
    else:
        localizable_strings_dir = path.join(temp_dir, 'values-' + locale_name)

    makedirs(localizable_strings_dir)
    return path.join(localizable_strings_dir, 'strings.xml')


export_types = {

    'json': {
        'lokalise_type': 'json',
        'file_reader_fn': read_json_file_as_dict,
        'output_localization_file_path_fn': get_output_localization_file,
        'file_writer_fn': write_dict_to_json_file
    },

    'ios': {
        'lokalise_type': 'strings',
        'file_reader_fn': read_properties_file_as_dict,
        'output_localization_file_path_fn': get_ios_output_localization_file,
        'file_writer_fn': write_dict_to_properties_file
    },

    'kotlin': {
        'lokalise_type': 'properties',
        'file_reader_fn': read_properties_file_as_dict,
        'output_localization_file_path_fn': get_output_localization_file,
        'file_writer_fn': write_dict_to_properties_file
    },

    'android': {
        'lokalise_type': 'xml',
        'file_reader_fn': read_xml_strings_file_as_dict,
        'output_localization_file_path_fn': get_android_output_localization_file,
        'file_writer_fn': write_dict_to_xml_strings_file
    }

}


def export_project(logger, temp_dir, api_key, project_id, export_type, timeout):
    logger.info("Exporting project %s", project_id)

    endpoint = "https://lokalise.co/api/project/export"
    post_params = {
        'id': project_id,
        'api_token': api_key,
        'type': export_types[export_type]['lokalise_type'],
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

    return LokaliseProject(projectID=project_id, zippedFileName=downloaded_file)


def export_projects(logger, temp_dir, projects, api_key, export_type, timeout):
    exported_project_files = []

    for index, project in enumerate(projects):
        exported_project = export_project(logger, temp_dir, api_key, project, export_type, timeout)
        exported_project_files.append(exported_project)

        if not index == len(projects) - 1:
            logger.info("Waiting 5s because of the lokalise.co flood detector, please be patient ...")
            sleep(5)

    return exported_project_files


def unzip_exported_projects(logger, temp_dir, exported_projects):
    unzipped_dirs = []

    for project in exported_projects:
        unzipped_dir = path.join(temp_dir, project.projectID)
        logger.debug("Unzipping " + project.projectID + " in " + unzipped_dir)

        unzip_file(project.zippedFileName, unzipped_dir)
        remove(project.zippedFileName)
        unzipped_dirs.append(project.projectID)

        logger.debug("Unzipped " + project.zippedFileName + " in " + unzipped_dir)

    return unzipped_dirs


def get_localization_files_to_merge(logger, temp_dir, project_directories):
    """
    Groups files to merge for each language.
    :param logger:
    :param temp_dir:
    :param project_directories:
    :return: a dictionary like this:
    {
      'file1': ['projectA', 'projectB'],
      'file2': ['projectA']
    }
    """

    localization_files_to_merge = {}

    for project_dir in project_directories:
        logger.debug("Searching for localization files in " + project_dir)

        for localized_file in list_files_in_dir(path.join(temp_dir, project_dir)):
            logger.debug("  ->  Found " + localized_file)

            if localized_file in localization_files_to_merge:
                localization_files_to_merge[localized_file].append(project_dir)
            else:
                localization_files_to_merge[localized_file] = [project_dir]

    return localization_files_to_merge


def log_duplicated_keys(logger, localization_file, dict_a, dict_b):
    duplicated_keys = intersect_dict(dict_a, dict_b)
    if duplicated_keys:
        for duplicated_key in duplicated_keys:
            logger.error("Found duplicated localization key in " + localization_file + ": " + duplicated_key
                         + ". Using value from last project ID")


def merge_localizations(logger, temp_dir, export_type, localization_files_to_merge, underscorize_localization_keys,
                        kotlin_package):
    logger.info("Merging " + export_type + " localization files")

    localization_files = []

    for localization_file in localization_files_to_merge:
        localization_keys = {}

        for project_dir in localization_files_to_merge[localization_file]:
            file_path = path.join(temp_dir, project_dir, localization_file)
            logger.debug("Reading localization keys from " + file_path)
            new_keys = export_types[export_type]['file_reader_fn'](logger, file_path, underscorize_localization_keys)
            log_duplicated_keys(logger, localization_file, localization_keys, new_keys)
            localization_keys.update(new_keys)
            logger.debug("Removing " + file_path)
            remove(file_path)

        localization_path = export_types[export_type]['output_localization_file_path_fn'](temp_dir, localization_file)
        export_types[export_type]['file_writer_fn'](localization_keys, localization_path)
        localization_files.append(localization_path)

    if export_type == 'kotlin':
        generate_kotlin_strings_table(logger, temp_dir, localization_files, kotlin_package,
                                      underscorize_localization_keys)


def remove_temp_project_dirs(logger, temp_dir, project_directories):
    logger.debug("Removing temp project directories")

    for project in project_directories:
        project_path = path.join(temp_dir, project)
        logger.debug("Removing directory: " + project_path)
        remove_tree(project_path)


@begin.start(auto_convert=True, lexical_order=True)
def main(api_key,  # lokalise.co API key
         projects_to_export,  # comma separated list of project IDs to be exported
         export_type,  # exported format. It can be json, ios, android or kotlin
         output_path="",  # export absolute path. It will create needed directories
         underscorize_localization_keys=True,  # replaces - and . with _ in all the localization keys
         clean_output_path_before_export=False,  # wipes the output path before exporting new data
         debug=False,  # true to enable debugging output
         timeout=10,  # timeout in seconds for each request
         kotlin_package=default_kotlin_package):  # package of the generated localization keys file

    logger = init_logger(debug)
    projects = parse_projects_to_export(projects_to_export)

    if export_type not in export_types:
        logger.error("export_type must be one of the following: %s", ",".join(export_types.keys()))
        return -1

    logger.debug("Using API Key: %s", api_key)
    logger.debug("Exporting type: %s", export_type)
    logger.debug("Output path: %s", output_path)
    logger.debug("Projects to export: %s", projects)

    try:
        with TemporaryDirectory(prefix="lokalise-exporter") as temp_dir:
            exported_project_files = export_projects(logger, temp_dir, projects, api_key, export_type, timeout)
            project_directories = unzip_exported_projects(logger, temp_dir, exported_project_files)
            localization_files_to_merge = get_localization_files_to_merge(logger, temp_dir, project_directories)

            merge_localizations(logger, temp_dir, export_type, localization_files_to_merge,
                                underscorize_localization_keys, kotlin_package)

            remove_temp_project_dirs(logger, temp_dir, project_directories)

            copy_files_to_output_directory(logger, clean_output_path_before_export, temp_dir, output_path)

            logger.info("Done!")

    except Exception as exc:
        logger.error("Export failed! Don't worry, output path is untouched: " + output_path)
        logger.exception(exc)
        return -2
