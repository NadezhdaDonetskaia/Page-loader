import os
from progress.bar import Bar
from .add_scheme import add_scheme
from .download_link import download_link
from .page_parse import changed_link
from .logger_config import logger


def progress_downloader(links_for_download, base_url, download_folder, page_data):
    progress = Bar(base_url, max=len(links_for_download), suffix='%(percent)d%%')
    progress.start()
    for link, tag, atr in links_for_download:
        try:
            new_link = add_scheme(link, base_url)
            new_name_link = download_link(new_link, download_folder)
            name_download_folder = os.path.basename(download_folder)
            new_path = os.path.join(name_download_folder, new_name_link)
            changed_link(page_data, tag, atr, link, new_path)
            progress.next()
        except Exception as err:
            logger.debug(err)
            print(f'Link {link} not downloaded: {err}')
    progress.finish()
