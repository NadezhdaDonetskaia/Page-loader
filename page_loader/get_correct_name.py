import os
from slugify import slugify


def get_correct_file_name(url_splitting):
    file_name = ''.join([url_splitting.netloc, url_splitting.path])
    file_name, ext = os.path.splitext(file_name)
    name = slugify(file_name)
    if not ext:
        ext = '.html'
    return name + ext


def get_correct_folder_name(name):
    file_name, ext = os.path.splitext(name)
    return file_name + '_files'
