# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-schedules.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns schedules "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return schedules in the GVM trashcan. No parameters show default schedules\n"
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


def list_schedules(gmp: Gmp, trashed: str) -> None:
    if trashed == "trash":
        response_xml = gmp.get_schedules(trash=True, filter_string="rows=-1")
    else:
        response_xml = gmp.get_schedules(filter_string="rows=-1")

    schedules_xml = response_xml.xpath("schedule")

    heading = ["#", "Name", "Id", "TZ", "iCalendar"]

    rows = []
    numberRows = 0

    print("Listing schedules.\n")

    for schedule in schedules_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(schedule.xpath("name/text()"))
        schedule_id = schedule.get("id")
        icalendar = "".join(schedule.xpath("icalendar/text()"))
        timezone = "".join(schedule.xpath("timezone/text()"))
        rows.append([rowNumber, name, schedule_id, timezone, icalendar])
        # print(icalendar)

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the scanners
    list_schedules(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
