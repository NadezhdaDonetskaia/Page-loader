import os
from urllib.parse import urlparse
import requests
import logging.config
from .get_correct_name import get_correct_file_name
from .progress_downloader import progress_downloader


# logging.config.fileConfig()
logger = logging.getLogger(__name__)


def get_data(page_url):
    try:
        r = requests.get(page_url, timeout=5, stream=True)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.error(errh.strerror)
    except requests.exceptions.ConnectionError as errc:
        logger.error(errc.strerror)
    except requests.exceptions.Timeout as errt:
        logger.error(errt.strerror)
    except requests.exceptions.RequestException as err:
        logger.error(err.strerror)
    else:
        logger.debug(f'Code status {r.status_code}')
        return r


def download_link(page_url, download_path):
    url_splitting = urlparse(page_url)
    file_name = get_correct_file_name(url_splitting)
    file_path = os.path.join(download_path, file_name)
    data = get_data(page_url)
    if not data:
        logger.debug(f'Failed to download file {file_name}')
    else:
        progress_downloader(file_path, data, file_name)
        logger.debug(f'File {file_name} downloaded')
        return file_name
