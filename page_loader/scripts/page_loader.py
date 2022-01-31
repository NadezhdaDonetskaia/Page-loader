#!/usr/bin/env python3
import sys
import argparse
from page_loader import download
import logging

parser = argparse.ArgumentParser(description='Page loader',
                                 prog='page-loader', usage='%(prog)s [options] <url>')
parser.add_argument('page_url', metavar='<url>',
                    help='enter page address'
                    )
parser.add_argument('-o', '--output',
                    help='output dir (default: current folder)')

args = parser.parse_args()


Log_Format = "%(name)s - %(levelname)s - %(message)s"
logging.basicConfig(stream=sys.stdout,
                    format=Log_Format,
                    level=logging.ERROR)

logger = logging.getLogger(__name__)


def main():
    try:
        print(download(args.page_url, args.output))
    except OSError as e:
        logger.error(e, exc_info=True)


if __name__ == '__main__':
    main()
