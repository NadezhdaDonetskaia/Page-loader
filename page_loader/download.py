import os
from urllib.parse import urlparse
from .download_link import download_link
from .page_parse import page_parse
from .get_correct_name import get_correct_folder_name

import logging.config


# logging.config.fileConfig()
logger = logging.getLogger(__name__)


def download(page_url, download_path):
    if not os.path.exists(download_path):
        logger.error(f'Folder {download_path} is not exist, try again')
        raise OSError(f'Folder {download_path} is not exist, try again')
    file_name = download_link(page_url, download_path)
    if not isinstance(file_name, str):
        logger.error(f'Failed to download page {page_url}')
        raise file_name
    file_path = os.path.join(download_path, file_name)
    folder_name = get_correct_folder_name(file_name)
    download_folder = os.path.join(download_path, folder_name)
    try:
        os.mkdir(download_folder)
        logger.debug(f'Folder {download_folder} created')
    except FileExistsError:
        logger.debug(f'Folder {download_folder} exist')
    with open(file_path, 'r') as f:
        data = f.read()
    data = page_parse(data, download_folder, urlparse(page_url))
    with open(file_path, 'w') as f:
        f.write(data)
    print(file_path)
    return file_path
