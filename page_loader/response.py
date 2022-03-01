import requests
from .logger_config import logger


def get_response(page_url):
    try:
        r = requests.get(page_url, timeout=3, stream=True)
        r.raise_for_status()
    except requests.exceptions.Timeout as errt:
        logger.debug(str(errt))
        raise requests.exceptions.Timeout('Connect or Read Timeout!')
    except requests.exceptions.TooManyRedirects as errr:
        logger.debug(str(errr))
        raise requests.exceptions.TooManyRedirects('Too many redirects')
    except requests.exceptions.ConnectionError as errc:
        logger.debug(str(errc))
        raise requests.exceptions.ConnectionError('A Connection error occurred')
    except requests.exceptions.HTTPError as errh:
        logger.debug(str(errh))
        raise requests.exceptions.HTTPError('HTTP Error occurred')
    except requests.exceptions.RequestException as err:
        logger.exception(str(err))
        raise requests.exceptions.RequestException('Other request exceptions occurred')
    else:
        logger.debug(f'Code status {r.status_code} for {page_url}')
        return r
