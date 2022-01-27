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


def write_file(path, data):
    with open(path, 'w+') as f:
        f.write(data)


def get_base_url(url):
    url = urlparse(url)
    return os.path.join(f'{url.scheme}://', url.netloc)


def get_images_path(data, base_url):
    soup = BeautifulSoup(data, 'html.parser')
    images = soup.find_all('img')
    images_paths = []
    for image in images:
        src = image.get('src')
        if not src.startswith('http'):
            src = urljoin(base_url, src)
            images_paths.append(src)
    return images_paths


def download_images(images_paths, dir_path):
    new_path = []
    for path in images_paths:
        images_name = get_url_without_scheme(path)
        images_name, exp = get_correct_name_and_ext(images_name)
        images_name = images_name + exp
        image_path = os.path.join(dir_path, images_name)
        image = requests.Session().get(path)
        with open(image_path, 'wb') as f:
            f.write(image.content)
        new_path.append(image_path)
    return new_path


def changed_path(file, new_path, download_path):
    with open(file, 'r') as fp:
        f = fp.read()
    soup = BeautifulSoup(f, features="html.parser")
    for image in soup.find_all('img'):
        for path in new_path:
            print(download_path)
            print(path)
            image['src'] = os.path.relpath(path, download_path)
    soup = soup.prettify()
    with open(file, 'w') as f:
        f.write(soup)


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
    images_path = get_images_path(data, base_url)
    new_image_path = download_images(images_path, download_folder)
    # заменяем ссылки в новом html
    changed_path(file_path, new_image_path, download_path)
    return file_name
