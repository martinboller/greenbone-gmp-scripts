# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-credentials.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns credentials "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return credentials in the GVM trashcan. No parameters show default credentials\n"
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
        "trashed",
        nargs="?",
        default="Default",
        type=str,
        help=("trash or default"),
    )

    script_args, _ = parser.parse_known_args(args)
    return script_args


def list_credentials(gmp: Gmp, trashed: str) -> None:
    # pylint: disable=unused-argument

    if trashed == "trash":
        response_xml = gmp.get_credentials(trash=True, filter_string="rows=-1")
    else:
        response_xml = gmp.get_credentials(filter_string="rows=-1")

    credentials_xml = response_xml.xpath("credential")

    heading = ["#", "Id", "Name", "Type", "Insecure use"]

    rows = []
    numberRows = 0

    print("Listing credentials.\n")

    for credential in credentials_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(credential.xpath("name/text()"))
        credential_id = credential.get("id")
        cred_type = "".join(credential.xpath("type/text()"))
        if cred_type.upper() == "UP":
            cred_type = "Username + Password (up)"
        elif cred_type.upper() == "USK":
            cred_type = "Username + SSH Key (usk)"
        elif cred_type.upper() == "SMIME":
            cred_type = "S/MIME Certificate (smime)"
        elif cred_type.upper() == "PGP":
            cred_type = "PGP Encryption Key (pgp)"
        elif cred_type.upper() == "SNMP":
            cred_type = "Simple Network Management Protocol (snmp)"
        elif cred_type.upper() == "PW":
            cred_type = "Password only (pw)"
        cred_insecureuse = "".join(credential.xpath("allow_insecure/text()"))
        if cred_insecureuse == "1":
            cred_insecureuse = "Yes"
        else:
            cred_insecureuse = "No"

        rows.append(
            [rowNumber, credential_id, name, cred_type, cred_insecureuse]
        )

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the creds
    list_credentials(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
