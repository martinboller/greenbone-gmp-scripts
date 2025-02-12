# SPDX-FileCopyrightText: 2024 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-scanners.gmp.py

from argparse import Namespace

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table


def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=unused-argument

    response_xml = gmp.get_scanners(filter_string="rows=-1")
    scanners_xml = response_xml.xpath("scanner")

    heading = ["#", "Name", "Id", "Host", "Port", "Created", "Modified"]

    rows = []
    numberRows = 0

    print(
        "Listing scanners.\n"
    )

    for scanner in scanners_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(scanner.xpath("name/text()"))
        scanner_id = scanner.get("id")
        host = "".join(scanner.xpath("host/text()"))
        created = "".join(scanner.xpath("creation_time/text()"))
        #modified = "".join(scanner.xpath("modification_time/text()"))
        port = "".join(scanner.xpath("port/text()"))
        rows.append([rowNumber, name, scanner_id, host, port, created])

    print(Table(heading=heading, rows=rows))


if __name__ == "__gmp__":
    main(gmp, args)
