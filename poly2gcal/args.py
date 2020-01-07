"""Module for arguments parsing."""

import argparse


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '-t',
        dest='test',
        action='store_const',
        const=True,
        default=False,
        help='test: only preview requests & do not actually add to calendar',
    )
    parser.add_argument(
        '-c',
        dest='checklist',
        action='store_const',
        const=True,
        default=False,
        help='generate checklist of labs to hand in, separated by weeks',
    )
    return parser


def parse_args() -> argparse.Namespace:
    return get_parser().parse_args()
