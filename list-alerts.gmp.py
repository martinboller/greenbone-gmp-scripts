# SPDX-FileCopyrightText: 2024 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-alerts.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns alerts "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return alerts in the GVM trashcan. No parameters show default alerts\n"
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


def list_alerts(gmp: Gmp, trashed: str) -> None:
    # pylint: disable=unused-argument

    if trashed == "trash":
        response_xml = gmp.get_alerts(trash=True, filter_string="rows=-1")
    else:
        response_xml = gmp.get_alerts(filter_string="rows=-1")

    alerts_xml = response_xml.xpath("alert")

    heading = [
        "#",
        "Name",
        "Id",
        "Event",
        "Event type",
        "Method",
        "Condition",
        "In use",
    ]

    rows = []
    numberRows = 0

    print("Listing alerts.\n")

    for alert in alerts_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(alert.xpath("name/text()"))
        alert_id = alert.get("id")
        alert_condition = "".join(alert.xpath("condition/text()"))
        alert_method = "".join(alert.xpath("method/text()"))
        alert_event_type = "".join(alert.xpath("event/data/text()"))
        alert_event = "".join(alert.xpath("event/text()"))
        alert_inuse = "".join(alert.xpath("in_use/text()"))
        if alert_inuse == "1":
            alert_inuse = "Yes"
        else:
            alert_inuse = "No"

        rows.append(
            [
                rowNumber,
                name,
                alert_id,
                alert_event,
                alert_event_type,
                alert_method,
                alert_condition,
                alert_inuse,
            ]
        )

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the alerts
    list_alerts(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
