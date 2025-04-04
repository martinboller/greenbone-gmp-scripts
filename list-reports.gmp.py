# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-reports.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script list reports with the status "
    "defined on the commandline. Status can be: \n"
    "All, Queued, Requested, Interrupted, Running, Stop Requested, Stopped, or Done \n"
    "Default: All"
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
        "status_cmd",
        nargs="?",
        default="All",
        type=str,
        help=(
            'Status: "All", "Queued", "Requested", "Interrupted", "Running", "Stop Requested", "Stopped", or "Done"'
        ),
    )
    script_args, _ = parser.parse_known_args(args)
    return script_args


def list_reports(
    gmp: Gmp,
    status: str,
):
    str_status = "All"
    if status.upper() == "ALL":
        status = "All"
    elif status.upper() == "REQUESTED":
        str_status = "Requested"
    elif status.upper() == "INTERRUPTED":
        str_status = "Interrupted"
    elif status.upper() == "QUEUED":
        str_status = "Queued"
    elif status.upper()[:6] == "STOPRE":
        str_status = "Stop Requested"
    elif status.upper()[:6] == "STOP R":
        str_status = "Stop Requested"
    elif status.upper() == "DONE":
        str_status = "Done"
    elif status.upper() == "RUNNING":
        str_status = "Running"
    elif status.upper() == "STOPPED":
        str_status = "Stopped"
    else:
        str_status = "All"

    print("Reports with status: " + str_status + "\n")

    if str_status == "All":
        response_xml = gmp.get_reports(
            ignore_pagination=True, details=True, filter_string="rows=-1"
        )
    elif str_status == "trash":
        response_xml = gmp.get_reports(
            trash=True,
            ignore_pagination=True,
            filter_string="status="
            + str_status
            + "  and sort-reverse=name and rows=-1",
        )
    else:
        response_xml = gmp.get_reports(
            ignore_pagination=True,
            details=True,
            filter_string="status="
            + str_status
            + "  and sort-reverse=name and rows=-1",
        )

    reports_xml = response_xml.xpath("report")
    heading = [
        "#",
        "Id",
        "Creation Time",
        "Modification Time",
        "Task Name",
        "Status",
        "Progress",
    ]
    rows = []
    numberRows = 0

    for report in reports_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)
        creation_time = "".join(report.xpath("creation_time/text()"))
        # report_name = "".join(report.xpath("name/text()")) # Report name is the same as Creation Time
        report_id = report.get("id")
        report_task = "".join(report.xpath("task/name/text()"))
        mod_time = "".join(report.xpath("modification_time/text()"))
        report_status = "".join(report.xpath("report/scan_run_status/text()"))
        report_progress = (
            "".join(report.xpath("report/task/progress/text()")) + "%"
        )
        rows.append(
            [
                rowNumber,
                report_id,
                creation_time,
                mod_time,
                report_task,
                report_status,
                report_progress,
            ]
        )

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    print("Listing reports.\n")

    list_reports(gmp, parsed_args.status_cmd)


if __name__ == "__gmp__":
    main(gmp, args)
