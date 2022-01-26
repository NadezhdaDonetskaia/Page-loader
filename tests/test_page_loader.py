import os
import tempfile
import pytest
import requests_mock
from page_loader import download


test_dirname = os.path.dirname(__file__)
created_html = 'ru-hexlet-io-courses.html'
created_dir = 'ru-hexlet-io-courses_files'
created_img = 'ru-hexlet-io-assets-professions-nodejs.png'
expected_file = os.path.join(test_dirname, 'fixtures', created_html)
expected_dir = os.path.join(test_dirname, 'fixtures', created_dir)
expected_img = os.path.join(expected_dir, created_img)
page_url = 'https://ru.hexlet.io/courses'
image_url = 'https://ru.hexlet.io/assets/professions/nodejs.png'


parameters_mark = [
    created_html,
    created_dir,
    created_img,
]


@pytest.mark.parametrize('expected_name', parameters_mark)
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
                    print(expected_path)
                    assert os.path.exists(expected_path)

# написать параметры для фала и картинки
def test_data_is_download(expected_data):
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
