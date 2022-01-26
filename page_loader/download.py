import os
import re
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


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


def get_base_url(url):
    url = urlparse(url)
    return os.path.join(f'{url.scheme}://', url.netloc)


def get_images_link(data, base_url):
    soup = BeautifulSoup(data, 'html.parser')
    images = soup.find_all('img')
    images_links = []
    for image in images:
        src = image.get('src')
        if not src.startswith('http'):
            src = urljoin(base_url, src)
            images_links.append(src)
    return images_links


def download_images(images_links, dir_path):
    for link in images_links:
        images_name = get_url_without_scheme(link)
        images_name, exp = get_correct_name_and_ext(images_name)
        images_name = images_name + exp
        image_path = os.path.join(dir_path, images_name)
        image = requests.Session().get(link)
        with open(image_path, 'wb') as f:
            f.write(image.content)


def set_scr():
    pass


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
    # узнаем базовую url
    base_url = get_base_url(page_url)
    # записываем файлы в папку
    images_link = get_images_link(data, base_url)
    download_images(images_link, download_folder)
    # заменяем ссылки в новом html
    return file_name
