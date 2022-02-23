from urllib.parse import urlparse, urljoin


def add_scheme(url, parent_domain):
    url = urlparse(url)
    parent_domain = urlparse(parent_domain)
    if not url.scheme:
        url = urljoin(parent_domain.geturl(), url.path)
        return url
    return url.geturl()
