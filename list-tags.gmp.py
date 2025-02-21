# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-tags.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns tags "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return tags in the GVM trashcan. No parameters show default tags\n"
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


def list_tags(gmp: Gmp, trashed: str) -> None:
    if trashed == "trash":
        response_xml = gmp.get_tags(trash=True, filter_string="rows=-1")
    else:
        response_xml = gmp.get_tags(filter_string="rows=-1")

    tags_xml = response_xml.xpath("tag")

    heading = ["#", "Name", "Id", "Modified", "Value", "Type", "Count"]

    rows = []
    numberRows = 0

    print("Listing tags.\n")

    for tag in tags_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(tag.xpath("name/text()"))
        modified = "".join(tag.xpath("modification_time/text()"))
        value = "".join(tag.xpath("value/text()"))
        type = "".join(tag.xpath("resources/type/text()"))
        count = "".join(tag.xpath("resources/count/total/text()"))
        tag_id = tag.get("id")
        rows.append([rowNumber, name, tag_id, modified, value, type, count])

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the scanners
    list_tags(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
