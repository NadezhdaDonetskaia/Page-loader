from urllib.parse import urlparse
from .url import is_same_domain
from .logger_config import logger


TAGS_AND_ATTRIBUTES = {
    'img': ('src', 'href'),
    'script': ('src',),
    'link': ('src', 'href'),
}


def get_links_for_download(page_data, parent_domain):
    parent_domain = urlparse(parent_domain)

    def get_link(search_tag, atr):
        tags = page_data.find_all(search_tag)
        for tag in tags:
            link = tag.get(atr)
            if is_same_domain(link, parent_domain):
                link_for_download.append((link, search_tag, atr))
    link_for_download = []
    for tag, attrs in TAGS_AND_ATTRIBUTES.items():
        for attr in attrs:
            get_link(tag, attr)
    return set(link_for_download)


def replace_links(page_data, search_tag, attr, old_link, new_link):
    tags = page_data.find_all(search_tag)
    for tag in tags:
        if tag.get(attr) == old_link:
            logger.debug(f'Link {tag[attr]} changed on {new_link}')
            tag[attr] = new_link
