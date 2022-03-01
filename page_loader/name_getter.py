import os
from urllib.parse import urlparse
from slugify import slugify


def get_file_name(url):
    url = urlparse(url)
    file_name = ''.join([url.netloc, url.path])
    file_name, ext = os.path.splitext(file_name)
    name = slugify(file_name)
    if not ext:
        ext = '.html'
    return name + ext


def get_folder_name(name):
    file_name, ext = os.path.splitext(name)
    return file_name + '_files'
