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
        modified = "".join(scanner.xpath("modification_time/text()"))
        port = "".join(scanner.xpath("port/text()"))
        rows.append([rowNumber, name, scanner_id, host, port, created])

    print(Table(heading=heading, rows=rows))


if __name__ == "__gmp__":
    main(gmp, args)
