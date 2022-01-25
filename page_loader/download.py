import os
import re
import requests


def get_url_without_scheme(url):
    return url.split('//')[1]


def get_correct_name_and_ext(page_url):
    file_name, ext = os.path.splitext(page_url)
    file_name = re.sub("[^A-Za-z0-9]", "-", file_name)
    return file_name, ext


def get_data(page_url):
    data = requests.Session().get(page_url)
    return data.text


# надо ли проверять, что такой файл создан?
# что делать, если страница уже загружена?
def write_file(path, data):
    with open(path, 'w+') as f:
        f.write(data)


def download(page_url, download_path):
    url_without_scheme = get_url_without_scheme(page_url)
    file_name, _ = get_correct_name_and_ext(url_without_scheme)
    if not download_path:
        download_path = os.getcwd()
    # запись страница в файл
    file_path = os.path.join(download_path, file_name + '.html')
    data = get_data(page_url)
    write_file(file_path, data)
    # создание папки для картинок
    download_folder = os.path.join(download_path, file_name + '_files')
    os.mkdir(download_folder)
    return file_name
