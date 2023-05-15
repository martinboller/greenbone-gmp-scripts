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

from gvm.xml import pretty_print


def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=unused-argument

    CERT = gmp.types.FeedType.from_string('CERT')
    GVMD_DATA = gmp.types.FeedType.from_string('GVMD_DATA')
    NVT = gmp.types.FeedType.from_string('NVT')
    SCAP = gmp.types.FeedType.from_string('SCAP')
    feed_types = [SCAP, NVT, CERT, GVMD_DATA]

    heading = ["Type", "Name", "Version"]
    rows = []
    #pretty_print(feeds_xml)

    for feed_type in feed_types:
        response_xml = gmp.get_feed(feed_type)
        feeds_xml = response_xml.xpath("feed")
        pretty_print(feeds_xml)
    
        for feed in feeds_xml:
            name = "".join(feed.xpath("name/text()"))
            version = "".join(feed.xpath("version/text()"))
            type = "".join(feed.xpath("type/text()"))

        rows.append([type, name, version])

    print(Table(heading=heading, rows=rows))


if __name__ == "__gmp__":
    main(gmp, args)
