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
        r = requests.get(page_url, timeout=3, stream=True)
        r.raise_for_status()
    except requests.exceptions.Timeout as errt:
        logger.debug(errt)
        return errt
    except requests.exceptions.TooManyRedirects as errr:
        logger.debug(errr)
        return errr
    except requests.exceptions.HTTPError as errh:
        logger.debug(errh)
        return errh
    except requests.exceptions.ConnectionError as errc:
        logger.debug(errc)
        return errc
    except requests.exceptions.RequestException as err:
        logger.debug(err)
        return err
    else:
        logger.debug(f'Code status {r.status_code}')
        return r


def download_link(page_url, download_path):
    url_splitting = urlparse(page_url)
    file_name = get_correct_file_name(url_splitting)
    file_path = os.path.join(download_path, file_name)
    data = get_data(page_url)
    if not isinstance(data, requests.models.Response):
        logger.debug(f'Failed to download file {file_name}')
        return data
    else:
        progress_downloader(file_path, data, file_name)
        logger.debug(f'File {file_name} downloaded')
        return file_name
