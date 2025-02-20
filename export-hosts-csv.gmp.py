# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Loosely based on other greenbone scripts
#
# Run with: gvm-script --gmp-username admin-user --gmp-password password socket export-hosts-csv.gmp.py <csv file> days
# example: gvm-script --gmp-username admin --gmp-password top$ecret socket export-hosts-csv.gmp.py hosts.csv 2


import csv
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from datetime import date, datetime, time, timedelta

from gvm.protocols.gmp import Gmp
from gvmtools.helper import error_and_exit

HELP_TEXT = (
    "This script generates a csv file with hosts (assets) "
    "from Greenbone Vulnerability Manager.\n\n"
    "csv file will contain:\n"
    "IP Address, Hostname, MAC Address, Operating System, last seen, and severity\n"
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
        "csv_filename",
        nargs="?",
        default="gvm_hosts.csv",
        type=str,
        help=(
            "Optional: CSV File for hosts information - Default: gvm_hosts.csv"
        ),
    )

    parser.add_argument(
        "delta_days",
        nargs="?",
        default="1",
        type=int,
        help=(
            "Optional: Number of days in the past to pull hosts information - Default: 1 day"
        ),
    )

    script_args, _ = parser.parse_known_args(args)
    return script_args


def list_hosts(
    gmp: Gmp, from_date: date, to_date: date, csvfilename: str
) -> None:
    host_filter = (
        f"rows=-1 and modified>{from_date.isoformat()} "
        f"and modified<{to_date.isoformat()}"
    )

    # Get the XML of hosts
    hosts_xml = gmp.get_hosts(filter_string=host_filter)
    host_info = []

    for host in hosts_xml.xpath("asset"):
        # ip will always be there
        ip = host.xpath("name/text()")[0]
        host_seendates = host.xpath("modification_time/text()")
        host_lastseen = host_seendates[0]

        # hostnames and other attributes may not be there
        hostnames = host.xpath(
            'identifiers/identifier/name[text()="hostname"]/../value/text()'
        )
        if len(hostnames) == 0:
            hostname = ""
            pass
        else:
            hostname = hostnames[0]

        host_macs = host.xpath(
            'identifiers/identifier/name[text()="MAC"]/../value/text()'
        )
        if len(host_macs) == 0:
            host_mac = ""
            pass
        else:
            host_mac = host_macs[0]

        host_severity = host.xpath("host/severity/value/text()")
        if len(host_severity) == 0:
            host_severity = 0
            pass
        else:
            host_severity = host_severity[0]

        host_os = host.xpath(
            'host/detail/name[text()="best_os_txt"]/../value/text()'
        )
        if len(host_os) == 0:
            host_os = ""
            pass
        else:
            host_os = host_os[0]

        host_info.append(
            [hostname, ip, host_mac, host_os, host_lastseen, host_severity]
        )
    # Write the list host_info to csv file
    writecsv(csvfilename, host_info)
    print(
        f"CSV file: {csvfilename}\n"
        f"From:     {from_date}\n"
        f"To:       {to_date}\n"
    )


def writecsv(csv_filename, hostinfo: list) -> None:
    field_names = [
        "IP Address",
        "Hostname",
        "MAC Address",
        "Operating System",
        "Last Seen",
        "CVSS",
    ]
    try:
        with open(csv_filename, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_ALL)
            writer.writerow(field_names)
            writer.writerows(hostinfo)
            csvfile.close
    except IOError as e:
        error_and_exit(f"Failed to write csv file: {str(e)} (exit)")


def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable
    args = args.script[1:]
    parsed_args = parse_args(args=args)

    delta_days = parsed_args.delta_days
    # simply getting yesterday from midnight to now
    from_date = datetime.combine(datetime.today(), time.min) - timedelta(
        days=delta_days
    )
    to_date = datetime.now()
    # get the hosts
    list_hosts(gmp, from_date, to_date, parsed_args.csv_filename)


if __name__ == "__gmp__":
    main(gmp, args)
