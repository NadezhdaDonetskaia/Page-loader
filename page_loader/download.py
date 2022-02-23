import os
from bs4 import BeautifulSoup
from .get_correct_name.get_correct_file_name import get_correct_file_name
from .download_link import download_link
from .page_parse import get_link_for_download, changed_link
from .get_correct_name.get_correct_folder_name import get_correct_folder_name
from .get_response import get_response
from .add_scheme import add_scheme
from .logger_config import logger


def download(page_url, download_path):
    if not os.path.exists(download_path):
        logger.debug(f'Folder {download_path} is not exist')
        raise OSError(f'Folder {download_path} is not exist, try again')
    page_response = get_response(page_url)
    page_data = BeautifulSoup(page_response.content, 'html.parser')
    file_name = get_correct_file_name(page_url)
    file_path = os.path.join(download_path, file_name)
    folder_name = get_correct_folder_name(file_name)
    download_folder = os.path.join(download_path, folder_name)
    try:
        os.mkdir(download_folder)
        logger.debug(f'Folder {download_folder} created')
    except FileExistsError:
        logger.debug(f'Folder {download_folder} exist')
    except Exception as err:
        logger.debug(err)
        raise err
    links_for_download = get_link_for_download(page_data, page_url)
    for link, tag, atr in links_for_download:
        try:
            new_link = add_scheme(link, page_url)
            new_name_link = download_link(new_link, download_folder)
            name_download_folder = os.path.basename(download_folder)
            new_path = os.path.join(name_download_folder, new_name_link)
            changed_link(page_data, tag, atr, link, new_path)
        except Exception as err:
            logger.debug(err)
            print(f'Link {link} not downloaded: {err}')
    page_data = page_data.prettify()
    with open(file_path, 'w') as f:
        f.write(page_data)
        logger.debug(f'Page {page_url} is downloaded')
    return file_path
