
# -*- coding: utf-8 -*-
#
# Based on other Greenbone scripts 
#
# Martin Boller
#

import sys

from argparse import Namespace

from gvm.protocols.gmp import Gmp

from gvmtools.helper import Table

from datetime import datetime, timedelta, time, date


def list_hosts(gmp: Gmp, from_date: date, to_date: date) -> None:
    host_filter = (
        f"rows=-1 and modified>{from_date.isoformat()} "
        f"and modified<{to_date.isoformat()}"
        f'and "rows=-1"'
    )

    # Get the XML of hosts
    hosts_xml = gmp.get_hosts(filter_string=host_filter)
    heading = ["hostname", "IP-Address", "MAC", "OS", "Last Seen", "Severity"]
    rows=[]

    for host in hosts_xml.xpath("asset"):
        hostnames = host.xpath('identifiers/identifier/name[text()="hostname"]/../value/text()')
        if len(hostnames) == 0:
            continue
        hostname = hostnames[0]
        ip = host.xpath("name/text()")[0]
        host_seendates = host.xpath("modification_time/text()")
        host_lastseen = host_seendates[0]
        host_macs = host.xpath('identifiers/identifier/name[text()="MAC"]/../value/text()')
        if len(host_macs) == 0:
            continue
        host_mac = host_macs[0]
        host_severity = host.xpath('host/severity/value/text()')[0]
        host_os = host.xpath('host/detail/name[text()="best_os_txt"]/../value/text()')[0]

        rows.append([hostname, ip, host_mac, host_os, host_lastseen, host_severity])

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable

    # simply getting yesterday from midnight to midnight today
    from_date = (datetime.combine(datetime.today(), time.min) - timedelta(days=1))
    night_time = datetime.strptime('235959','%H%M%S').time()
    to_date = datetime.combine(datetime.now(), night_time) 

    list_hosts(gmp, from_date, to_date)

if __name__ == "__gmp__":
    main(gmp, args)
