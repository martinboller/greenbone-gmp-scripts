# -*- coding: utf-8 -*-
#
# Loosely based on the create-filterw-from-host-list
# As provided by Greenbone in the gvm-tools repo
#
# Martin Boller
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
# Run with gvm-script --gmp-username admin-user --gmp-password password socket create-filters-from-csv.gmp.py hostname-server filters.csv
#
#

import sys
import time
import csv

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from pathlib import Path
from typing import List

from gvm.protocols.gmp import Gmp

from gvmtools.helper import error_and_exit

HELP_TEXT = (
    "This script pulls filtername, hostnames/IP addresses, and credentials "
    "from a csv file and creates a filter for each row. \n\n"
    "csv file to contain name of filter, ips, and up to 4 credentials previously created \n"
    "name,ip-addresses,credential1,credential2,credential3,credential4"
)


def check_args(args):
    len_args = len(args.script) - 1
    if len_args != 1:
        message = """
        This script pulls filter names from a csv file and creates a filter \
for each row.
        One parameter after the script name is required.

        1. <filters_csvfile>  -- text file containing filtername and hostnames or IP-addresses

        Example:
            $ gvm-script --gmp-username name --gmp-password pass \
ssh --hostname <gsm> scripts/create_filters_from_csv.gmp <filters_csvfile>
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
        "filters_csv_file",
        type=str,
        help=("File containing host names / IPs"),
    )

    script_args, _ = parser.parse_known_args(args)
    return script_args

def create_filters(   
    gmp: Gmp,
    filter_csv_file: Path,
):
    try:
        numberfilters = 0
        with open(filter_csv_file, encoding="utf-8") as csvFile:
            content = csv.reader(csvFile, delimiter=',')  #read the data
            for row in content:   #loop through each row
                numberfilters = numberfilters + 1
                filterType = row[0]
                filterName = row[1]
                filterDescription = row[2]
                filterTerm = row[3]
                filterNameFull = filterType + ":" + filterDescription + ":" + filterName
                comment = f"Created: {time.strftime('%Y/%m/%d-%H:%M:%S')}"
                filterResources = []
                if filterType.upper() == "ALERT":
                    resource_type=gmp.types.FilterType.ALERT
                elif filterType.upper() == "CONFIG":
                    resource_type=gmp.types.FilterType.SCAN_CONFIG
                elif filterType.upper() == "CREDENTIAL":
                    resource_type=gmp.types.FilterType.CREDENTIAL
                elif filterType.upper() == "REPORT":
                    resource_type=gmp.types.FilterType.REPORT 
                elif filterType.upper() == "SCANNER":
                    resource_type=gmp.types.FilterType.SCANNER
                elif filterType.upper() == "SCHEDULE":
                    resource_type=gmp.types.FilterType.SCHEDULE
                elif filterType.upper() == "TARGET":
                   resource_type=gmp.types.FilterType.TARGET
                elif filterType.upper() == "TASK":
                    resource_type=gmp.types.FilterType.TASK
                else:
                    print("Only alert, config, credential, report, scanner, schedule, target, and task supported")
                    exit()
                gmp.create_filter(
                   name=filterNameFull, comment=comment, filter_type=resource_type, term=filterTerm,
                )

        csvFile.close()   #close the csv file
    except IOError as e:
        error_and_exit(f"Failed to read filter_csv_file: {str(e)} (exit)")

    if len(row) == 0:
        error_and_exit("filter file is empty (exit)")
    
    return numberfilters
    
def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable
    if args.script:
        args = args.script[1:]

    parsed_args = parse_args(args=args)

    numberfilters = create_filters(
        gmp,
        parsed_args.filters_csv_file,
    )

    numberfilters = str(numberfilters)
    print("   \n [" + numberfilters + "] filter(s) created!\n")


if __name__ == "__gmp__":
    main(gmp, args)
