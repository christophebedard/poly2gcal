"""Module for arguments parsing."""

import argparse


def get_parser() -> argparse.ArgumentParser:
    """Get arguments parser."""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '-t',
        '--test',
        dest='test',
        action='store_const',
        const=True,
        default=False,
        help='only preview requests & do not actually add to calendar (default: %(default)s)',
    )
    parser.add_argument(
        '-c',
        '--checklist',
        dest='checklist',
        action='store_const',
        const=True,
        default=False,
        help='generate checklist of labs to hand in, separated by weeks (default: %(default)s)',
    )
    parser.add_argument(
        '-f',
        '--file',
        dest='file_path',
        default='input_data.json',
        help='the path to the input data JSON file (default: %(default)s)',
    )
    return parser


def parse_args() -> argparse.Namespace:
    """Parse arguments."""
    return get_parser().parse_args()
