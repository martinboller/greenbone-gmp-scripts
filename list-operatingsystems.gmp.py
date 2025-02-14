# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Loosely based on other greenbone scripts
#
# Run with: gvm-script --gmp-username admin-user --gmp-password password socket list-operating_systems.gmp.py <days>
# example: gvm-script --gmp-username admin --gmp-password top$ecret socket list-operating_systems.gmp.py 2


import sys
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from datetime import date, datetime, time, timedelta

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script generates a table of operating_systems (assets) "
    "from Greenbone Vulnerability Manager.\n\n"
    "table will contain:\n"
    "operating_systemname, IP Address, MAC Address, Operating System, last seen, and severity\n"
)


def check_args(args: Namespace) -> None:
    len_args = len(args.script) - 1
    if len_args < 1:
        message = """
        This script requests information about all operating_systems <days> days prior to today (included) and 
        displays it as a table. It requires one parameter after the script name:
        1. days -- number of days prior to today to pull operating_systems information from

        Examples:
            $ gvm-script --gmp-username username --gmp-password password socket list-operating_systems.gmp.py <days>
            $ gvm-script --gmp-username admin --gmp-password 0f6fa69b-32bb-453a-9aa4-b8c9e56b3d00 socket list-operating_systems.gmp.py 4
        """
        print(message)
        sys.exit()


def parse_args(args: Namespace) -> Namespace:  # pylint: disable=unused-argument
    """Parsing args ..."""

    parser = ArgumentParser(
        prefix_chars="+",
        add_help=False,
        formatter_class=RawTextHelpFormatter,
    )

    parser.add_argument(
        "+h",
        "++help",
        action="help",
        help="Show this help message and exit.",
    )

    parser.add_argument(
        "delta_days",
        type=int,
        help=("Number of days in the past to pull operating_systems information"),
    )

    script_args, _ = parser.parse_known_args(args)
    return script_args

def list_operating_systems(gmp: Gmp, from_date: date, to_date: date) -> None:
    operating_system_filter = (
        f"rows=-1 "
        f"and modified>{from_date.isoformat()} "
        f"and modified<{to_date.isoformat()}"
    )

    operating_systems_xml = gmp.get_operating_systems(filter_string=operating_system_filter)
    heading = [
        "#",
        "Title",
        "Latest Severity",
        "Count",
    ]
    rows = []
    numberRows = 0

    print("Listing operating_systems.\n" f"From: {from_date}\n" f"To:   {to_date}\n")

    for operating_system in operating_systems_xml.xpath("asset"):
        # title will always be there   
        os_title = operating_system.xpath(
            "name/text()"
        )[0]

        os_latest_severity = operating_system.xpath(
            "os/latest_severity/value/text()"
        )[0]

        os_host_count = operating_system.xpath(
            "os/installs/text()"
        )[0]

        # Count number of operating_systems
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)
        rows.append(
            [
                rowNumber,
                os_title,
                os_latest_severity,
                os_host_count,
            ]
        )

    print(Table(heading=heading, rows=rows))

def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable
    check_args(args)
    if args.script:
        args = args.script[1:]
    parsed_args = parse_args(args=args)
    delta_days = parsed_args.delta_days
    # simply getting yesterday from midnight to today (now)
    from_date = datetime.combine(datetime.today(), time.min) - timedelta(
        days=delta_days
    )
    to_date = datetime.now()
    # print(from_date, to_date)

    list_operating_systems(gmp, from_date, to_date)


if __name__ == "__gmp__":
    main(gmp, args)
