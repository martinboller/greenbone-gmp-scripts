# SPDX-FileCopyrightText: 2024 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-tickets.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns tickets "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return tickets in the GVM trashcan. No parameters show default tickets\n"
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


def list_tickets(gmp: Gmp, trashed: str) -> None:
    # pylint: disable=unused-argument

    if trashed == "trash":
        response_xml = gmp.get_tickets(trash=True, filter_string="rows=-1")
    else:
        response_xml = gmp.get_tickets(filter_string="rows=-1")

    tickets_xml = response_xml.xpath("ticket")

    heading = ["#", "Name", "Status", "Open Time", "Host", "Task", "Note"]

    rows = []
    numberRows = 0

    print("Listing tickets.\n")

    for ticket in tickets_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(ticket.xpath("name/text()"))
        ticket_status = "".join(ticket.xpath("status/text()"))
        ticket_task = "".join(ticket.xpath("task/name/text()"))
        ticket_host = "".join(ticket.xpath("host/text()"))
        ticket_open = "".join(ticket.xpath("open_time/text()"))
        if ticket_status.upper() == "OPEN":
            ticket_note = "".join(ticket.xpath("open_note/text()"))
        elif ticket_status.upper() == "FIXED":
            ticket_note = "".join(ticket.xpath("fixed_note/text()"))
        elif ticket_status.upper() == "CLOSED":
            ticket_note = "".join(ticket.xpath("closed_note/text()"))

        rows.append(
            [
                rowNumber,
                name,
                ticket_status,
                ticket_open,
                ticket_host,
                ticket_task,
                ticket_note,
            ]
        )

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the tasks
    list_tickets(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
