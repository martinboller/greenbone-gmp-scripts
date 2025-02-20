# SPDX-FileCopyrightText: 2024 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-filters.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns filters "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return filters in the GVM trashcan. No parameters show default filters\n"
)


def parse_args(args: Namespace) -> Namespace:  # pylint: disable=unused-argument
    """Parsing args ..."""

    parser = ArgumentParser(
        prefix_chars="+",
        add_help=False,
        formatter_class=RawTextHelpFormatter,
        description=HELP_TEXT,
    )

    parser.add_argument(
        "+h",
        "++help",
        action="help",
        help="Show this help message and exit.",
    )

    parser.add_argument(
        "trashed",
        nargs="?",
        default="Default",
        type=str,
        help=("trash or default"),
    )

    script_args, _ = parser.parse_known_args(args)
    return script_args


def list_filters(gmp: Gmp, trashed: str) -> None:
    # pylint: disable=unused-argument

    if trashed == "trash":
        response_xml = gmp.get_filters(trash=True, filter_string="rows=-1")
    else:
        response_xml = gmp.get_filters(filter_string="rows=-1")

    filters_xml = response_xml.xpath("filter")

    heading = ["#", "Name", "Id", "Modified", "Type", "Term"]

    rows = []
    numberRows = 0

    print("Listing filters.\n")

    for filter in filters_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(filter.xpath("name/text()"))
        modified = "".join(filter.xpath("modification_time/text()"))
        term = "".join(filter.xpath("term/text()"))
        type = "".join(filter.xpath("type/text()"))
        filter_id = filter.get("id")
        rows.append([rowNumber, name, filter_id, modified, type, term])

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the filters
    list_filters(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
