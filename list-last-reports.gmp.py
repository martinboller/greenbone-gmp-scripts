# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-tasks.gmp.py


from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns tasks "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return tasks in the GVM trashcan. No parameters show default tasks\n"
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


def list_tasks(gmp: Gmp, trashed: str) -> None:
    # pylint: disable=unused-argument

    if trashed == "trash":
        response_xml = gmp.get_tasks(trash=True, filter_string="rows=-1")
    else:
        response_xml = gmp.get_tasks(details=True, filter_string="rows=-1")

    tasks_xml = response_xml.xpath("task")

    heading = ["#", "Name", "Task Id", "Report Id", "Report Time"]

    rows = []
    numberRows = 0

    print("Listing tasks.\n")

    for task in tasks_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(task.xpath("name/text()"))
        task_id = task.get("id")
        targetname = "".join(task.xpath("target/name/text()"))
        scanner = "".join(task.xpath("scanner/name/text()"))
        severity = "".join(task.xpath("last_report/report/severity/text()"))
        order = "".join(task.xpath("hosts_ordering/text()"))
        last_report_id = "".join(task.xpath("last_report/report/@id"))
        last_report_timestamp = "".join(task.xpath("last_report/report/timestamp/text()"))
        rows.append(
            [rowNumber, name, task_id, last_report_id, last_report_timestamp]
        )

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the tasks
    list_tasks(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
