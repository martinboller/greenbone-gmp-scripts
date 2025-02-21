# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-users.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns users " "from Greenbone Vulnerability Manager.\n\n"
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

    script_args, _ = parser.parse_known_args(args)
    return script_args


def list_users(gmp: Gmp) -> None:
    response_xml = gmp.get_users(filter_string="rows=-1")
    users_xml = response_xml.xpath("user")

    heading = ["#", "Name", "Id", "Role", "Groups"]

    rows = []
    numberRows = 0

    print("Listing users.\n")

    for user in users_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(user.xpath("name/text()"))
        user_id = user.get("id")
        user_role = "".join(user.xpath("role/name/text()"))
        user_groups = "".join(user.xpath("groups/group/name/text()"))

        rows.append([rowNumber, name, user_id, user_role, user_groups])

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable
    args = args.script[1:]
    parse_args(args=args)
    # get the tasks
    list_users(gmp)


if __name__ == "__gmp__":
    main(gmp, args)
