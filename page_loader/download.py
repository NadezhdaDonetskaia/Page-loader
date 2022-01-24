import os
import re
import requests


def get_file_name(page_url):
    file_name, ext = os.path.splitext(page_url.split('//')[1])
    file_name = re.sub("[^A-Za-z0-9]", "-", file_name) + '.html'
    return file_name


def get_data(page_url):
    data = requests.Session().get(page_url)
    return data.text


# надо ли проверять, что такой файл создан?
# что делать, если страница уже загружена?
def write_file(path, data):
    with open(path, 'w+') as f:
        f.write(data)


def download(page_url, download_path):
    file_name = get_file_name(page_url)
    if not download_path:
        download_path = os.getcwd()
    file_path = os.path.join(download_path, file_name)
    data = get_data(page_url)
    write_file(file_path, data)
    return file_name
