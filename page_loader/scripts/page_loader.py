#!/usr/bin/env python3
import argparse
from page_loader import download

parser = argparse.ArgumentParser(description='Page loader,',
                                 prog='page-loader')
parser.add_argument('page_url', metavar='page_url',
                    help='page url for download')
parser.add_argument('-f', '--output', dest='OUTPUT',
                    default='current_directory',
                    help='enter download directory')

args = parser.parse_args()


def main():
    download(args.OUTPUT, args.page_url)


if __name__ == '__main__':
    main()
