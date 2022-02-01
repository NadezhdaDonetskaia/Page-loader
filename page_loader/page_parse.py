import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import logging.config
from .is_same_domain import is_same_domain
from .download_link import download_link


TAGS_AND_ATTRIBUTES = {
    'img': ('src', 'href'),
    'script': ('src',),
    'link': ('src', 'href'),
}


logging.config.fileConfig(fname='logger_config.cnf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def add_scheme(url, parent_domain):
    url = urlparse(url)
    if not url.scheme:
        url = urljoin(parent_domain.geturl(), url.path)
        return url
    return url.geturl()


def page_parse(data, download_folder, parent_domain):

    def get_link(search_tag, atr):
        tags = page_data.find_all(search_tag)
        for tag in tags:
            link = tag.get(atr)
            if is_same_domain(link, parent_domain):
                link = add_scheme(link, parent_domain)
                new_name = download_link(link, download_folder)
                name_download_folder = os.path.basename(download_folder)
                tag[atr] = os.path.join(name_download_folder, new_name)

    page_data = BeautifulSoup(data, 'html.parser')
    for tag, attrs in TAGS_AND_ATTRIBUTES.items():
        for attr in attrs:
            get_link(tag, attr)
    page_data = page_data.prettify()
    return page_data
