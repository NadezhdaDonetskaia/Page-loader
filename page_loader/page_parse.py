from urllib.parse import urlparse
from .is_same_domain import is_same_domain
from .logger_config import logger


TAGS_AND_ATTRIBUTES = {
    'img': ('src', 'href'),
    'script': ('src',),
    'link': ('src', 'href'),
}


def get_link_for_download(page_data, parent_domain):
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
    return link_for_download


def changed_link(data, search_tag, atr, old_link, new_link):
    tags = data.find_all(search_tag)
    for tag in tags:
        if tag.get(atr) == old_link:
            logger.debug(f'Link {tag[atr]} changed on {new_link}')
            tag[atr] = new_link
