import os
from urllib.parse import urlparse
from .get_correct_name.get_correct_file_name import get_correct_file_name
from .get_response import get_response
from .logger_config import logger


def download_link(page_url, download_path):
    url_splitting = urlparse(page_url)
    file_name = get_correct_file_name(url_splitting)
    file_path = os.path.join(download_path, file_name)
    response = get_response(page_url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    logger.debug(f'File {file_name} downloaded')
    return file_name
