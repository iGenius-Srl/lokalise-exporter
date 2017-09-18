from os import scandir
import colorlog


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


def underscorize_key(value, underscorize_keys):
    stripped = str(value).strip()

    if underscorize_keys:
        return stripped.replace('-', '_')

    return stripped


def list_files_in_dir(dir_path):
    return [f.name for f in scandir(dir_path) if f.is_file()]
