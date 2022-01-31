#!/usr/bin/env python3
import argparse
from page_loader import download

parser = argparse.ArgumentParser(description='Page loader',
                                 prog='page-loader', usage='%(prog)s [options] <url>')
parser.add_argument('page_url', metavar='<url>',
                    help='enter page address'
                    )
parser.add_argument('-o', '--output',
                    help='output dir (default: current folder)')

args = parser.parse_args()


def main():
    print(download(args.page_url, args.output))


if __name__ == '__main__':
    main()
