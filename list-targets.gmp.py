# SPDX-FileCopyrightText: 2024 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-targets.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns targets "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return targets in the GVM trashcan. No parameters show default targets\n"
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


def list_targets(gmp: Gmp, trashed: str) -> None:
    if trashed == "trash":
        response_xml = gmp.get_targets(trash=True, filter_string="rows=-1")
    else:
        response_xml = gmp.get_targets(filter_string="rows=-1")

    targets_xml = response_xml.xpath("target")

    heading = [
        "#",
        "Name",
        "Id",
        "Count",
        "SSH Credential",
        "SMB Cred",
        "ESXi Cred",
        "SNMP Cred",
        "Alive test",
    ]

    rows = []
    numberRows = 0

    print("Listing targets.\n")

    for target in targets_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(target.xpath("name/text()"))
        maxhosts = "".join(target.xpath("max_hosts/text()"))
        sshcred = "".join(target.xpath("ssh_credential/name/text()"))
        smbcred = "".join(target.xpath("smb_credential/name/text()"))
        esxicred = "".join(target.xpath("esxi_credential/name/text()"))
        snmpcred = "".join(target.xpath("snmp_credential/name/text()"))
        target_id = target.get("id")
        alive_test = "".join(target.xpath("alive_tests/text()"))
        rows.append(
            [
                rowNumber,
                name,
                target_id,
                maxhosts,
                sshcred,
                smbcred,
                esxicred,
                snmpcred,
                alive_test,
            ]
        )

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the targets
    list_targets(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
