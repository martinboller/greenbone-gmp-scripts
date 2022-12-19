# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Based on other Greenbone scripts 
#
# Martin Boller
#

from gvm.protocols.gmp import Gmp

from gvmtools.helper import Table

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

HELP_TEXT = (
    "This script list reports with the status "
    "defined on the commandline. Status can be: \n"
    "Requested, Running, or Done \n"
    "Note: Case matters"
)


def check_args(args):
    len_args = len(args.script) - 1
    if len_args != 1:
        message = """
        This script lists all reports depending on status.
        One parameter after the script name is required.

        1. Status -- Either Requested, Running, or Done

        Example:
            $ gvm-script --gmp-username name --gmp-password pass \
socket list-reports.gmp.py Done \n
Don't forget that case matters
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
        "status_cmd",
        type=str,
        help=("Status Requested, Running, Done"),
    )
    script_args, _ = parser.parse_known_args(args)
    return script_args

def list_reports (
    gmp: Gmp,
    status: str,
):
    str_status = status
    print("Status: " + str_status + "\n")

    response_xml = gmp.get_reports(ignore_pagination=True, details=True, filter_string="status=" + str_status + "  and sort-reverse=name")
    reports_xml = response_xml.xpath("report")
    heading = ["#", "ID", "Date"]
    rows = []
    numberRows = 0

    for report in reports_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(report.xpath("name/text()"))
        report_id = report.get("id")
        status = report.get("status")
        rows.append([rowNumber, report_id, name])

    print(Table(heading=heading, rows=rows))

def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=unused-argument
    if args.script:
        args = args.script[1:]

    parsed_args = parse_args(args = args)
    list_reports (
        gmp,
        parsed_args.status_cmd
    )

if __name__ == "__gmp__":
    main(gmp, args)
