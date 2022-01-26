import os
import tempfile
import pytest
import requests_mock
from page_loader import download


test_dirname = os.path.dirname(__file__)
created_html = 'ru-hexlet-io-courses.html'
created_dir = 'ru-hexlet-io-courses_files'
created_img = os.path.join(created_dir, 'ru-hexlet-io-assets-professions-nodejs.png')
expected_file = os.path.join(test_dirname, 'fixtures', created_html)
expected_dir = os.path.join(test_dirname, 'fixtures', created_dir)
expected_img = os.path.join(test_dirname, 'fixtures', created_img)
page_url = 'https://ru.hexlet.io/courses'
image_url = 'https://ru.hexlet.io/assets/professions/nodejs.png'


parameters_exists = [
    created_html,
    created_dir,
    created_img,
]


@pytest.mark.parametrize('expected_name', parameters_exists)
def test_new_file_is_created(expected_name):
    with open(expected_file) as f:
        exp_data = f.read()
        with open(expected_img, 'rb') as image:
            exp_img = image.read()
            with requests_mock.Mocker() as mock:
                mock.get(page_url, text=exp_data)
                mock.get(image_url, content=exp_img)
                with tempfile.TemporaryDirectory() as directory:
                    download(page_url, directory)
                    expected_path = os.path.join(directory, expected_name)
                    assert os.path.exists(expected_path)


def test_page_is_download():
    with open(expected_file) as f:
        exp_data = f.read()
        with open(expected_img, 'rb') as image:
            exp_img = image.read()
            with requests_mock.Mocker() as mock:
                mock.get(page_url, text=exp_data)
                mock.get(image_url, content=exp_img)
                with tempfile.TemporaryDirectory() as directory:
                    download(page_url, directory)
                    expected_path = os.path.join(directory, created_html)
                    with open(expected_path) as f:
                        assert exp_data == f.read()


def test_images_is_download():
    with open(expected_file) as f:
        exp_data = f.read()
        with open(expected_img, 'rb') as image:
            exp_img = image.read()
            with requests_mock.Mocker() as mock:
                mock.get(page_url, text=exp_data)
                mock.get(image_url, content=exp_img)
                with tempfile.TemporaryDirectory() as directory:
                    download(page_url, directory)
                    expected_path = os.path.join(directory, created_img)
                    with open(expected_path, 'rb') as f:
                        assert exp_img == f.read()
