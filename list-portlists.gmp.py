# SPDX-FileCopyrightText: 2024 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-portlists.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns port lists "
    "from Greenbone Vulnerability Manager.\n\n"
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

    script_args, _ = parser.parse_known_args(args)
    return script_args


def list_portlists(gmp: Gmp) -> None:
    response_xml = gmp.get_port_lists(filter_string="rows=-1")
    portlists_xml = response_xml.xpath("port_list")

    heading = ["#", "Name", "Id", "Ports All", "Ports TCP", "Ports UDP"]

    rows = []
    numberRows = 0

    print("Listing portlists.\n")

    for portlist in portlists_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(portlist.xpath("name/text()"))
        port_list_id = portlist.get("id")
        port_all = "".join(portlist.xpath("port_count/all/text()"))
        port_tcp = "".join(portlist.xpath("port_count/tcp/text()"))
        port_udp = "".join(portlist.xpath("port_count/udp/text()"))

        rows.append(
            [rowNumber, name, port_list_id, port_all, port_tcp, port_udp]
        )

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parse_args(args=args)
    # get the portlists
    list_portlists(gmp)


if __name__ == "__gmp__":
    main(gmp, args)
