#!/usr/bin/env python3
import sys
import os
import argparse
from urllib.error import URLError
from page_loader import download
import logging.config


# log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logger_config.cnf')
# logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
# logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Page loader',
                                 prog='page-loader', usage='%(prog)s [options] <url>')
parser.add_argument('page_url', metavar='<url>',
                    help='enter page address'
                    )
parser.add_argument('-o', '--output', default=os.getcwd(),
                    help='output dir (default: current folder)')

args = parser.parse_args()

Log_Format = "%(message)s"
logging.basicConfig(stream=sys.stdout,
                    format=Log_Format,
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    try:
        download(args.page_url, args.output)
        sys.exit(0)
    except URLError as e:
        logger.error(e.strerror)
        print(e.strerror)
        sys.exit(1)
    except Exception as e:
        logger.error(e)
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
