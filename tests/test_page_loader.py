import os
import sys
import tempfile
import pytest
import logging
import requests_mock
from page_loader import download


Log_Format = "%(process)d - %(levelname)s - %(name)s - %(module)s - % (funcName)s - %(message)s"
logging.basicConfig(stream=sys.stdout,
                    format=Log_Format,
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


test_dirname = os.path.dirname(__file__)
file_for_download = os.path.join(test_dirname, 'fixtures', 'for_download', 'ru-hexlet-io-courses.html')
created_html_file = 'ru-hexlet-io-courses.html'
created_dir = 'ru-hexlet-io-courses_files'
page_url = 'https://ru.hexlet.io/courses'
image_url = 'https://ru.hexlet.io/assets/professions/nodejs.png'
link1_url = 'https://ru.hexlet.io/assets/application.css'
link2_url = page_url
script_url = 'https://ru.hexlet.io/packs/js/runtime.js'
created_img = os.path.join(created_dir, 'ru-hexlet-io-assets-professions-nodejs.png')
expected_file = os.path.join(test_dirname, 'fixtures', 'must_be', created_html_file)
expected_dir = os.path.join(test_dirname, 'fixtures', 'must_be', created_dir)
expected_img = os.path.join(test_dirname, 'fixtures', 'must_be', created_img)
expected_script = os.path.join(expected_dir, 'ru-hexlet-io-packs-js-runtime.js')
expected_link1 = os.path.join(expected_dir, 'ru-hexlet-io-assets-application.css')
expected_link2 = os.path.join(expected_dir, created_html_file)


parameters_exists = [
    created_html_file,
    created_dir,
    expected_img,
    expected_script,
    expected_link1,
    expected_link2,
]


@pytest.mark.parametrize('expected_name', parameters_exists)
def test_new_file_is_created(expected_name):
    with open(file_for_download) as f:
        exp_data = f.read()
        with open(expected_img, 'rb') as image:
            exp_img = image.read()
            with requests_mock.Mocker() as mock:
                mock.get(page_url, text=exp_data)
                mock.get(image_url, content=exp_img)
                mock.get(script_url, content=exp_img)
                mock.get(link1_url, content=exp_img)
                with tempfile.TemporaryDirectory() as directory:
                    download(page_url, directory)
                    expected_path = os.path.join(directory, expected_name)
                    assert os.path.exists(expected_path)


# def test_page_is_download():
#     with open(file_for_download) as f:
#         exp_data = f.read()
#         with open(expected_img, 'rb') as image:
#             exp_img = image.read()
#             with requests_mock.Mocker() as mock:
#                 mock.get(page_url, text=exp_data)
#                 mock.get(image_url, content=exp_img)
#                 mock.get(script_url, content=exp_img)
#                 mock.get(link1_url, content=exp_img)
#                 with tempfile.TemporaryDirectory() as directory:
#                     download(page_url, directory)
#                     expected_path = os.path.join(directory, created_html_file)
#                     with open(expected_path) as f:
#                         with open(expected_file) as exp_f:
#                             assert f.read() == exp_f.read()
# 
# 
# def test_images_is_download():
#     with open(file_for_download) as f:
#         exp_data = f.read()
#         with open(expected_img, 'rb') as image:
#             exp_img = image.read()
#             with requests_mock.Mocker() as mock:
#                 mock.get(page_url, text=exp_data)
#                 mock.get(image_url, content=exp_img)
#                 mock.get(script_url, content=exp_img)
#                 mock.get(link1_url, content=exp_img)
#                 with tempfile.TemporaryDirectory() as directory:
#                     download(page_url, directory)
#                     expected_path = os.path.join(directory, created_img)
#                     with open(expected_path, 'rb') as img:
#                         assert img.read() == exp_img
