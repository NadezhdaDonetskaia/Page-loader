import os
from urllib.parse import urlparse
import requests
from .get_correct_name import get_correct_file_name
import logging.config


# logging.config.fileConfig()
logger = logging.getLogger(__name__)


def get_data(page_url):
    try:
        r = requests.get(page_url, timeout=3)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.info(f'Code status {r.status_code}\n"Http Error:"', errh)
        logger.error(errh, exc_info=True)
    except requests.exceptions.ConnectionError as errc:
        logger.info(f'Code status {r.status_code}\n"Http Error:"', errc)
        logger.error(errc, exc_info=True)
    except requests.exceptions.Timeout as errt:
        logger.info(f'Code status {r.status_code}\n"Http Error:"', errt)
        logger.error(errt, exc_info=True)
    except requests.exceptions.RequestException as err:
        logger.info(f'Code status {r.status_code}\n"Http Error:"', err)
        logger.error(err, exc_info=True)
    else:
        logger.debug(f'Code status {r.status_code}')
        return r.content


def download_link(page_url, download_path):
    url_splitting = urlparse(page_url)
    file_name = get_correct_file_name(url_splitting)
    file_path = os.path.join(download_path, file_name)
    data = get_data(page_url)
    if not data:
        logger.info(f'Failed to download file {file_name}')
    else:
        with open(file_path, 'wb') as f:
            f.write(data)
        logger.info(f'File {file_name} downloaded')
        return file_name
