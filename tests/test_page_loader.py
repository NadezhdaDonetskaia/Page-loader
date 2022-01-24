import os
import tempfile
import requests_mock
from page_loader import download


test_dirname = os.path.dirname(__file__)
expected_file = os.path.join(test_dirname, 'fixtures', 'ru-hexlet-io-courses.html')
page_url = 'https://ru.hexlet.io/courses'


def test_download_worked():
    with open(expected_file) as f:
        exp_data = f.read()
        with requests_mock.Mocker() as mock:
            mock.get(page_url, text=exp_data)
            with tempfile.TemporaryDirectory() as directory:
                download(page_url, directory)
                expected_path = os.path.join(directory, 'ru-hexlet-io-courses.html')
                assert os.path.exists(expected_path)
                with open(expected_path) as f:
                    assert exp_data == f.read()
