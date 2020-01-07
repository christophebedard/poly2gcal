#!/usr/bin/python3

"""poly2gcal - add PolyMTL classes to Google Calendar."""

from poly2gcal import args
from poly2gcal import poly2gcal


def main() -> None:
    params = args.parse_args()
    poly2gcal.main(
        params.file_path,
        params.test,
        params.checklist,
    )


if __name__ == '__main__':
    main()
