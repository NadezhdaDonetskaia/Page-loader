import os
import sys
from urllib.parse import urlparse
from .download_link import download_link
from .page_parse import page_parse
from .get_correct_name import get_correct_folder_name

import logging.config


# logging.config.fileConfig()
logger = logging.getLogger(__name__)


def download_page(page_url, download_path):
    if not download_path:
        download_path = os.getcwd()
    if not os.path.exists(download_path):
        logger.error(f'Folder {download_path} is not exist, try again')
        sys.exit(1)
    file_name = download_link(page_url, download_path)
    if not file_name:
        logger.error(f'Failed to download page {page_url}')
        sys.exit(1)
    file_path = os.path.join(download_path, file_name)
    folder_name = get_correct_folder_name(file_name)
    download_folder = os.path.join(download_path, folder_name)
    try:
        os.mkdir(download_folder)
        logger.info(f'Folder {download_folder} created')
    except FileExistsError:
        logger.info(f'Folder {download_folder} exist')
    with open(file_path, 'r') as f:
        data = f.read()
    data = page_parse(data, download_folder, urlparse(page_url))
    with open(file_path, 'w') as f:
        f.write(data)
    return file_name


def download(page_url, download_path):
    return download_page(page_url, download_path)
