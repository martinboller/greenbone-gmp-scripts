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
# GVM Specific
from gvm.protocols.gmp import Gmp
from gvmtools.helper import error_and_exit

HELP_TEXT = (
    "This script generates a csv file with certificates "
    "from Greenbone Vulnerability Manager.\n"
    "Optional: Specify csv filename and days in the past to get data from as positional arguments\n"
    "or live with the defaults\n"
    "csv file will contain:\n"
    "Subject, Issuer, Serial, SHA256 Fingerprint, MD5 Fingerprint, last_seen, Valid From, Valid To"
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
        nargs='?',
        default="gvm_certificates.csv",
        type=str,
        help=("Optional: CSV File with certificate information - Default: gvm_certificates.csv"),
    )

    parser.add_argument(
        "delta_days",
        nargs='?',
        default='1',
        type=int,
        help=("Optional: Number of days in the past to pull information - Default: 1 day"),
    )

    script_args, _ = parser.parse_known_args(args)
    return script_args

def list_tls_certificates(
    gmp: Gmp, from_date: date, to_date: date, csvfilename: str
) -> None:
    tls_certificate_filter = (
        f"rows=-1 and modified>{from_date.isoformat()} "
        f"and modified<{to_date.isoformat()}"
    )

    certificate_info = []

    tls_certificates_xml = gmp.get_tls_certificates(
        filter_string=tls_certificate_filter
    )
    # pretty_print(tls_certificates_xml)

    for tls_certificate in tls_certificates_xml.xpath("tls_certificate"):

        certificate_seen = tls_certificate.xpath("last_seen/text()")[0]

        certificate_from = tls_certificate.xpath("activation_time/text()")[0]

        certificate_to = tls_certificate.xpath("expiration_time/text()")[0]

        certificate_subject = tls_certificate.xpath("subject_dn/text()")[0]

        certificate_issuer = tls_certificate.xpath("issuer_dn/text()")[0]

        certificate_serial = tls_certificate.xpath("serial/text()")[0]

        certificate_sha256 = tls_certificate.xpath("sha256_fingerprint/text()")[
            0
        ]

        certificate_md5 = tls_certificate.xpath("md5_fingerprint/text()")[0]

        certificate_info.append(
            [
                certificate_subject,
                certificate_issuer,
                certificate_serial,
                certificate_sha256,
                certificate_md5,
                certificate_seen,
                certificate_from,
                certificate_to,
            ]
        )

    # Write the list host_info to csv file
    writecsv(csvfilename, certificate_info)
    print(
        f"CSV file: {csvfilename}\n"
        f"From:     {from_date}\n"
        f"To:       {to_date}\n"
    )


def writecsv(csv_filename, hostinfo: list) -> None:
    field_names = [
        "Subject",
        "Issuer",
        "Serial",
        "SHA256 Fingerprint",
        "MD5 Fingerprint",
        "Last seen",
        "Valid From",
        "Valid To",
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
    csv_filename = parsed_args.csv_filename
    delta_days = parsed_args.delta_days

    # simply getting yesterday from midnight to now
    from_date = datetime.combine(datetime.today(), time.min) - timedelta(
        days=delta_days
    )
    to_date = datetime.now()
    # get the certs
    list_tls_certificates(gmp, from_date, to_date, csv_filename)

if __name__ == "__gmp__":
    main(gmp, args)
