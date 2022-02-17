import os
import pytest
import requests_mock
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


@requests_mock.Mocker(kw='mock')
@pytest.mark.parametrize('new_file, exp_file', parameters)
def test_link_is_download(new_file, exp_file, tmpdir, **kwargs):
    kwargs['mock'].get(page_url, content=read_file(file_for_download))
    kwargs['mock'].get(image_url, content=read_file(expected_png))
    kwargs['mock'].get(script_url, content=read_file(expected_js))
    kwargs['mock'].get(css_url, content=read_file(expected_css))
    download(page_url, tmpdir)
    new_file = os.path.join(tmpdir, new_file)
    assert read_file(new_file) == read_file(exp_file)


def test_folder_not_exist():
    with pytest.raises(OSError) as e:
        directory = os.path.join(expected_dir, 'not-exist')
        download(page_url, directory)
    assert str(e.value) == f'Folder {directory} is not exist, try again'


errors = [
    (404, f'404 Client Error: None for url: {page_url}'),
    (503, f'503 Server Error: None for url: {page_url}'),
]


@requests_mock.Mocker(kw='mock')
@pytest.mark.parametrize('status_code, err_val', errors)
def test_status_code(status_code, err_val, tmpdir, **kwargs):
    with pytest.raises(Exception) as error:
        kwargs['mock'].get(page_url, status_code=status_code)
        download(page_url, tmpdir)
    assert str(error.value) == err_val


exc = [
    (Timeout, 'Timeout'),
    (ConnectionError, 'ConnectionError'),
    (RequestException, 'RequestException'),
    (TooManyRedirects, 'TooManyRedirects'),
    (HTTPError, 'HTTPError'),
]


@requests_mock.Mocker(kw='mock')
@pytest.mark.parametrize('exception, exc_val', exc)
def test_status_code(exception, exc_val, tmpdir, **kwargs):
    with pytest.raises(Exception) as error:
        kwargs['mock'].get(page_url, exc=exception)
        download(page_url, tmpdir)
    assert str(error.typename) == exc_val
