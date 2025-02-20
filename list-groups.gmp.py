# SPDX-FileCopyrightText: 2024 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-groups.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns groups "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return groups in the GVM trashcan. No parameters show default groups\n"
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


def list_groups(gmp: Gmp, trashed: str) -> None:

    if trashed == "trash":
        response_xml = gmp.get_groups(trash=True, filter_string="rows=-1")
    else:
        response_xml = gmp.get_groups(filter_string="rows=-1")

    groups_xml = response_xml.xpath("group")

    heading = ["#", "Name", "Id", "Members"]

    rows = []
    numberRows = 0

    print("Listing groups.\n")

    for group in groups_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(group.xpath("name/text()"))
        group_id = group.get("id")
        group_members = "".join(group.xpath("users/text()"))

        rows.append([rowNumber, name, group_id, group_members])

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the groups
    list_groups(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
