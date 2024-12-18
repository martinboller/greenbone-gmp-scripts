# SPDX-FileCopyrightText: 2024 Martin Boller
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Run with gvm-script --gmp-username admin-user --gmp-password password socket stop-all-scans.gmp.py


from argparse import Namespace

from gvm.protocols.gmp import Gmp

from gvmtools.helper import Table

def stop_tasks(gmp: Gmp) -> None:
    tasks = gmp.get_tasks(
            filter_string="rows=-1 status=Running or status=Requested or status=Queued"
        )
    try:
        for task_id in tasks.xpath("task/@id"):
            print(f"Stopping task {task_id} ... ")
            gmp.stop_task(task_id).xpath(
                "@status_text"
            )[0]
            print(status_text)
    except:
        pass

def main(gmp: Gmp, args: Namespace) -> None:
    # pylint: disable=undefined-variable
    print(
        "This script stops all tasks on the system.\n"
    )

    stop_tasks(gmp)
    
if __name__ == "__gmp__":
    main(gmp, args)
