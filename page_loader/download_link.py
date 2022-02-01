import os
from urllib.parse import urlparse
import requests
from .get_correct_name import get_correct_file_name


def get_data(page_url):
    data = requests.Session().get(page_url)
    return data.content


def download_link(page_url, download_path):
    url_splitting = urlparse(page_url)
    file_name = get_correct_file_name(url_splitting)
    file_path = os.path.join(download_path, file_name)
    data = get_data(page_url)
    with open(file_path, 'wb') as f:
        f.write(data)
    return file_name
