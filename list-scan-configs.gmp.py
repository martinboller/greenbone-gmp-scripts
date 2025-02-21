# SPDX-FileCopyrightText: 2025 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket list-scan.configs.gmp.py

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from gvm.protocols.gmp import Gmp
from gvmtools.helper import Table

HELP_TEXT = (
    "This script returns scan configs "
    "from Greenbone Vulnerability Manager.\n\n"
    "specify trash as first script parameter to "
    "return scan configs in the GVM trashcan. No parameters show default scan configs\n"
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


def list_scanconfigs(gmp: Gmp, trashed: str) -> None:
    if trashed == "trash":
        response_xml = gmp.get_scan_configs(trash=True, filter_string="rows=-1")
    else:
        response_xml = gmp.get_scan_configs(filter_string="rows=-1")

    scan_configs_xml = response_xml.xpath("config")

    heading = ["#", "Name", "Id", "NVT Count"]

    rows = []
    numberRows = 0

    print("Listing scan configurations.\n")

    for scan_config in scan_configs_xml:
        # Count number of reports
        numberRows = numberRows + 1
        # Cast/convert to text to show in list
        rowNumber = str(numberRows)

        name = "".join(scan_config.xpath("name/text()"))
        scan_config_id = scan_config.get("id")
        scan_config_nvt = "".join(scan_config.xpath("nvt_count/text()"))

        rows.append([rowNumber, name, scan_config_id, scan_config_nvt])

    print(Table(heading=heading, rows=rows))


def main(gmp: Gmp, args: Namespace) -> None:
    args = args.script[1:]
    parsed_args = parse_args(args=args)
    # get the scan configs
    list_scanconfigs(gmp, parsed_args.trashed)


if __name__ == "__gmp__":
    main(gmp, args)
