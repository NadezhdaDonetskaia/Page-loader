#!/usr/bin/env python3
import sys
import os
import argparse
from requests.exceptions import HTTPError, Timeout, ConnectionError, RequestException, TooManyRedirects
from page_loader import download


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
    except Timeout as errt:
        print(errt)
        sys.exit(1)
    except ConnectionError as errc:
        print(errc)
        sys.exit(1)
    except TooManyRedirects as errr:
        print(errr)
        sys.exit(1)
    except HTTPError as errh:
        print(errh)
        sys.exit(1)
    except RequestException as err:
        print(err)
        sys.exit(1)
    except OSError as erros:
        print(erros)
        sys.exit(1)
    except Exception:
        print('Something went wrong')
        sys.exit(1)


if __name__ == '__main__':
    main()
