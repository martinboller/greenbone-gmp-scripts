# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-feeds.gmp.py

from argparse import Namespace

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

# from gvm.xml import pretty_print


def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=unused-argument

    response_xml = gmp.get_feeds()
    feeds_xml = response_xml.xpath("feed")
    heading = ["#", "Name", "Version", "Status"]
    rows = []
    numberRows = 0
    #    pretty_print(feeds_xml)

    print("Listing feeds and their status.\n")

    for feed in feeds_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)
        name = "".join(feed.xpath("name/text()"))
        version = "".join(feed.xpath("version/text()"))
        # type = "".join(feed.xpath("type/text()"))
        status = "".join(feed.xpath("currently_syncing/timestamp/text()"))
        nvt_status = "".join(feed.xpath("sync_not_available/error/text()"))

        if not status:
            if not nvt_status:
                status = "Up-to-date..."
            else:
                status = nvt_status
                name = "NVT/Greenbone Community Feed"
                version = "Sync issue"
        else:
            status = "Update in progress..."

        rows.append([rowNumber, name, version, status])

    print(Table(heading=heading, rows=rows))


if __name__ == "__gmp__":
    main(gmp, args)
