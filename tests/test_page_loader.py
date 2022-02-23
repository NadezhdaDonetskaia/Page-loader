import os
import pytest
from requests.exceptions import HTTPError, Timeout, ConnectionError, RequestException, TooManyRedirects
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


parameters = [
    (created_html_file, expected_file),
    (created_css, expected_css),
    (created_png, expected_png),
    (created_html, expected_html),
    (created_js, expected_js),
]


@pytest.mark.parametrize('new_file, exp_file', parameters)
def test_link_is_download(new_file, exp_file, tmpdir, requests_mock):
    requests_mock.get(page_url, content=read_file(file_for_download))
    requests_mock.get(image_url, content=read_file(expected_png))
    requests_mock.get(script_url, content=read_file(expected_js))
    requests_mock.get(css_url, content=read_file(expected_css))
    download(page_url, tmpdir)
    new_file = os.path.join(tmpdir, new_file)
    assert read_file(new_file) == read_file(exp_file)


def test_folder_not_exist():
    with pytest.raises(OSError) as e:
        directory = os.path.join(expected_dir, 'not-exist')
        download(page_url, directory)
    assert str(e.value) == f'Folder {directory} is not exist, try again'


exc = [
    (Timeout, 'Connect or Read Timeout!'),
    (ConnectionError, 'A Connection error occurred'),
    (RequestException, 'Other request exceptions occurred'),
    (TooManyRedirects, 'Too many redirects'),
    (HTTPError, 'HTTP Error occurred'),
]


@pytest.mark.parametrize('exception, exc_val', exc)
def test_exception(exception, exc_val, tmpdir, requests_mock):
    with pytest.raises(Exception) as error:
        requests_mock.get(page_url, exc=exception)
        download(page_url, tmpdir)
    assert str(error.value) == exc_val
