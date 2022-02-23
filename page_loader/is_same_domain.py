from urllib.parse import urlparse


def is_same_domain(url, parent_domain):
    if not url:
        return False
    url_netloc = urlparse(url).netloc
    parent_domain_netloc = parent_domain.netloc
    if url_netloc == parent_domain_netloc:
        return True
    if f'.{url_netloc}' == parent_domain_netloc:
        return True
    if not url_netloc:
        return True
    return False
