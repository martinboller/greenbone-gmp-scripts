# SPDX-FileCopyrightText: 2024 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket empty-trash.gmp.py

from argparse import Namespace

from gvm.protocols.gmp import Gmp

from gvmtools.helper import Table



def main(gmp: Gmp, args: Namespace) -> None:

    print(
        "Emptying Trash...\n"
    )

    try:
        status_text = gmp.empty_trashcan().xpath("@status_text")[0]
        print(status_text)
    except:
        pass

if __name__ == "__gmp__":
    main(gmp, args)
