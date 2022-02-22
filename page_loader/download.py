import os
from urllib.parse import urlparse
from .get_correct_name.get_correct_file_name import get_correct_file_name
from .page_parse import page_parse
from .get_correct_name.get_correct_folder_name import get_correct_folder_name
from .get_response import get_response
from .logger_config import logger


def download(page_url, download_path):
    if not os.path.exists(download_path):
        logger.debug(f'Folder {download_path} is not exist')
        raise OSError(f'Folder {download_path} is not exist, try again')
    page_response = get_response(page_url)
    file_name = get_correct_file_name(page_url)
    file_path = os.path.join(download_path, file_name)
    folder_name = get_correct_folder_name(file_name)
    download_folder = os.path.join(download_path, folder_name)
    try:
        os.mkdir(download_folder)
        logger.debug(f'Folder {download_folder} created')
    except FileExistsError:
        logger.debug(f'Folder {download_folder} exist')
    except Exception as err:
        raise err
    page_data = page_parse(page_response, download_folder, urlparse(page_url))
    with open(file_path, 'w') as f:
        f.write(page_data)
    return file_path
