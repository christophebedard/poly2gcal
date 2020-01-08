#!/usr/bin/python3

"""Print out week intervals from input data file."""

from poly2gcal.weekdates_intervals import print_intervals


def main() -> None:
    """Entrypoint."""
    print_intervals('input_data.json')


if __name__ == '__main__':
    main()
