# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-report-formats.gmp.py


from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns report formats "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return report formats in the GVM trashcan. No parameters show default report formats\n"
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


def list_reportformats(gmp: Gmp, trashed: str) -> None:
    if trashed == "trash":
        response_xml = gmp.get_report_formats(
            trash=True, filter_string="rows=-1"
        )
    else:
        response_xml = gmp.get_report_formats(
            details=True, filter_string="rows=-1"
        )

    report_formats_xml = response_xml.xpath("report_format")
    heading = ["#", "Name", "Id", "Summary"]
    rows = []
    numberRows = 0

    print("Listing report formats.\n")

    for report_format in report_formats_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)
        name = "".join(report_format.xpath("name/text()"))
        report_format_id = report_format.get("id")
        report_format_summary = "".join(report_format.xpath("summary/text()"))
        # report_format_description = "".join(report_format.xpath("description/text()"))

        rows.append([rowNumber, name, report_format_id, report_format_summary])

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the report formats
    list_reportformats(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
