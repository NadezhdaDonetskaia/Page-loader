import os
import tempfile
import pytest
import requests_mock
from page_loader import download


test_dirname = os.path.dirname(__file__)
file_for_download = os.path.join(test_dirname, 'fixtures', 'for_download', 'ru-hexlet-io-courses.html')
created_html_file = 'ru-hexlet-io-courses.html'
created_dir = 'ru-hexlet-io-courses_files'
page_url = 'https://ru.hexlet.io/courses'
image_url = 'https://ru.hexlet.io/assets/professions/nodejs.png'
css_url = 'https://ru.hexlet.io/assets/application.css'
script_url = 'https://ru.hexlet.io/packs/js/runtime.js'
created_css = os.path.join(created_dir, 'ru-hexlet-io-assets-application.css')
created_png = os.path.join(created_dir, 'ru-hexlet-io-assets-professions-nodejs.png')
created_js = os.path.join(created_dir, 'ru-hexlet-io-packs-js-runtime.js')
created_html = os.path.join(created_dir, 'ru-hexlet-io-courses.html')
expected_file = os.path.join(test_dirname, 'fixtures', 'must_be', created_html_file)
expected_dir = os.path.join(test_dirname, 'fixtures', 'must_be', created_dir)
expected_png = os.path.join(test_dirname, 'fixtures', 'must_be', created_png)
expected_js = os.path.join(expected_dir, 'ru-hexlet-io-packs-js-runtime.js')
expected_css = os.path.join(expected_dir, 'ru-hexlet-io-assets-application.css')
expected_html = os.path.join(expected_dir, created_html_file)


def read_file(file):
    with open(file, 'rb') as f:
        return f.read()


parameters_exists = [
    created_html_file,
    created_dir,
    created_png,
    created_js,
    created_css,
    created_html,
]


@pytest.mark.parametrize('expected_name', parameters_exists)
def test_new_file_is_created(expected_name):
    with requests_mock.Mocker() as mock:
        mock.get(page_url, content=read_file(file_for_download))
        mock.get(image_url, content=read_file(expected_png))
        mock.get(script_url, content=read_file(expected_js))
        mock.get(css_url, content=read_file(expected_css))
        with tempfile.TemporaryDirectory() as directory:
            download(page_url, directory)
            expected_path = os.path.join(directory, expected_name)
            assert os.path.exists(expected_path)


parameters = [
    (created_html_file, expected_file),
    (created_css, expected_css),
    (created_png, expected_png),
    (created_html, expected_html),
    (created_js, expected_js),
]


@pytest.mark.parametrize('new_file, exp_file', parameters)
def test_link_is_download(new_file, exp_file):
    with requests_mock.Mocker() as mock:
        mock.get(page_url, content=read_file(file_for_download))
        mock.get(image_url, content=read_file(expected_png))
        mock.get(script_url, content=read_file(expected_js))
        mock.get(css_url, content=read_file(expected_css))
        with tempfile.TemporaryDirectory() as directory:
            download(page_url, directory)
            new_file = os.path.join(directory, new_file)
            assert read_file(new_file) == read_file(exp_file)
