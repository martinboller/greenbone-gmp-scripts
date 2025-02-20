# SPDX-FileCopyrightText: 2024 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-scanners.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns scanners "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return scanners in the GVM trashcan. No parameters show default scanners\n"
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


def list_scanners(gmp: Gmp, trashed: str) -> None:
    if trashed == "trash":
        response_xml = gmp.get_scanners(trash=True, filter_string="rows=-1")
    else:
        response_xml = gmp.get_scanners(filter_string="rows=-1")

    scanners_xml = response_xml.xpath("scanner")

    heading = ["#", "Name", "Id", "Host", "Port", "Created", "Modified"]

    rows = []
    numberRows = 0

    print("Listing scanners.\n")

    for scanner in scanners_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(scanner.xpath("name/text()"))
        scanner_id = scanner.get("id")
        host = "".join(scanner.xpath("host/text()"))
        created = "".join(scanner.xpath("creation_time/text()"))
        # modified = "".join(scanner.xpath("modification_time/text()"))
        port = "".join(scanner.xpath("port/text()"))
        rows.append([rowNumber, name, scanner_id, host, port, created])

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the scanners
    list_scanners(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
