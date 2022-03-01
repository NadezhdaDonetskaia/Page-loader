import os
from .name_getter import get_file_name
from .response import get_response
from .logger_config import logger


def download_link(page_url, download_path):
    file_name = get_file_name(page_url)
    file_path = os.path.join(download_path, file_name)
    response = get_response(page_url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    logger.debug(f'File {file_name} downloaded')
    return file_name
