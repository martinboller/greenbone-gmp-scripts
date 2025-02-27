# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket stop-scans-from-csv.gmp.py csv-file

import sys
import time
import csv

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from pathlib import Path
from typing import List
from gvm.errors import GvmResponseError
from gvm.protocols.gmp import Gmp
from gvmtools.helper import error_and_exit

HELP_TEXT = "This script pulls task names from a csv file and starts the tasks listed in every row. \n"


def check_args(args):
    len_args = len(args.script) - 1
    if len_args != 2:
        message = """
        This script pulls tasks from a csv file and creates a \
task for each row in the csv file.
        One parameter after the script name is required.

        1. <tasks_csvfile>  -- csv file containing names and secrets required for scan tasks

        Example:
            $ gvm-script --gmp-username name --gmp-password pass \
ssh --hostname <gsm> scripts/stop_tasks_from_csv.gmp.py \
<tasks-csvfile>
        """
        print(message)
        sys.exit()


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
        "task_file",
        type=str,
        help=("CSV File containing tasks"),
    )
    script_args, _ = parser.parse_known_args(args)
    return script_args


def task_id(
    gmp: Gmp,
    task_name: str,
):
    response_xml = gmp.get_tasks(
        filter_string="rows=-1, status=Running "
        "or status=Requested "
        "or status=Queued "
        "and name=" + task_name
    )
    tasks_xml = response_xml.xpath("task")
    task_id = ""

    for task in tasks_xml:
        name = "".join(task.xpath("name/text()"))
        task_id = task.get("id")
    return task_id


def stop_tasks(
    gmp: Gmp,
    task_file: Path,
):
    try:
        numbertasks = 0
        with open(task_file, encoding="utf-8") as csvFile:
            content = csv.reader(csvFile, delimiter=",")  # read the data
            try:
                for row in content:  # loop through each row
                    if len(row) == 0:
                        continue
                    task_stop = task_id(gmp, row[0])
                    if task_stop:
                        numbertasks = numbertasks + 1
                        print(
                            f"Stopping task name: {row[0]} with uuid: {task_stop} ..."
                        )
                        status_text = gmp.stop_task(task_stop).xpath(
                            "@status_text"
                        )[0]
                        print(status_text)
                    else:
                        print(
                            "Task "
                            + row[0]
                            + " is either in status Stopped, Stop Requested, or does not exist on this system.\n"
                        )
            except GvmResponseError as gvmerr:
                print(f"{gvmerr=}, task: {task_stop}")
                pass
        csvFile.close()  # close the csv file

    except IOError as e:
        error_and_exit(f"Failed to read task_file: {str(e)} (exit)")

    if len(row) == 0:
        error_and_exit("tasks file is empty (exit)")

    return numbertasks


def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable
    if args.script:
        args = args.script[1:]

    parsed_args = parse_args(args=args)

    print("Stopping tasks.\n")

    numbertasks = stop_tasks(
        gmp,
        parsed_args.task_file,
    )

    numbertasks = str(numbertasks)
    print("   \n [" + numbertasks + "] task(s)/scan(s) stopped!\n")


if __name__ == "__gmp__":
    main(gmp, args)
