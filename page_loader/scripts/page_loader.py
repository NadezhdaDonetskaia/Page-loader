#!/usr/bin/env python3
import sys
import os
import argparse
from requests.exceptions import HTTPError, Timeout, ConnectionError, RequestException, TooManyRedirects
from page_loader import download
from ..logger_config import logger

parser = argparse.ArgumentParser(description='Page loader',
                                 prog='page-loader', usage='%(prog)s [options] <url>')
parser.add_argument('page_url', metavar='<url>',
                    help='enter page address'
                    )
parser.add_argument('-o', '--output', default=os.getcwd(),
                    help='output dir (default: current folder)')

args = parser.parse_args()


def main():
    try:
        print(download(args.page_url, args.output))
        sys.exit(0)
    except(Timeout, ConnectionError, TooManyRedirects, HTTPError, RequestException):
        logger.debug('Requests exceptions')
        sys.exit(1)
    except Exception as e:
        print(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
