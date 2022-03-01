import os
from bs4 import BeautifulSoup
from progress.bar import Bar
from .file import get_file_name
from .page_parse import get_links_for_download
from .folder import get_folder_name
from .response import get_response
from .download_link import download_link
from .url import make_absolute_url
from .page_parse import replace_links
from .logger_config import logger


def download(page_url, download_path):
    if not os.path.exists(download_path):
        logger.debug(f'Folder {download_path} is not exist')
        raise OSError(f'Folder {download_path} is not exist, try again')
    page_response = get_response(page_url)
    page_data = BeautifulSoup(page_response.content, 'html.parser')
    file_name = get_file_name(page_url)
    file_path = os.path.join(download_path, file_name)
    folder_name = get_folder_name(file_name)
    download_folder = os.path.join(download_path, folder_name)
    try:
        os.mkdir(download_folder)
        logger.debug(f'Folder {download_folder} created')
    except FileExistsError:
        logger.debug(f'Folder {download_folder} exist')
    except Exception as err:
        logger.debug(err)
        raise err
    links_for_download = get_links_for_download(page_data, page_url)
    progress = Bar(page_url, max=len(links_for_download), suffix='%(percent)d%%')
    progress.start()
    for link, tag, atr in links_for_download:
        try:
            new_link = make_absolute_url(link, page_url)
            resource_file_name = download_link(new_link, download_folder)
            resource_folder_name = os.path.basename(download_folder)
            resource_file_path = os.path.join(resource_folder_name, resource_file_name)
            replace_links(page_data, tag, atr, link, resource_file_path)
            progress.next()
        except Exception as err:
            logger.debug(err)
            print(f'Link {link} not downloaded: {err}')
    progress.finish()
    page_data = page_data.prettify()
    with open(file_path, 'w') as f:
        f.write(page_data)
        logger.debug(f'Page {page_url} is downloaded')
    return file_path
