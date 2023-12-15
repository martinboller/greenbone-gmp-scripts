import sys
import time
import csv

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from pathlib import Path
from typing import List

from gvm.protocols.gmp import Gmp

from gvmtools.helper import error_and_exit

sender_email: str
recipient_email: str
alert_name: str = "Test_Alert"
alert_object = gmp.get_alerts(filter_string=f"name={alert_name}")
alert = alert_object.xpath("alert")

if len(alert) == 0:
    print(f"creating new alert {alert_name}")
    recipient_email="noc@bollers.dk"
    sender_email="martin@bollers.dk"
    alert_name="Alert_Test"
    alert_type=gmp.types.AlertMethod.EMAIL

    gmp.create_alert(
        name=alert_name,
        event=gmp.types.AlertEvent.TASK_RUN_STATUS_CHANGED,
        event_data={"status": "Done"},
        condition=gmp.types.AlertCondition.ALWAYS,
        method=alert_type,
        method_data={
            "message": "TEST",
            "notice": "1",
            "from_address": sender_email,
            "subject": "[Greenbone] Scan Done",
            #"notice_report_format": "a3810a62-1f62-11e1-9219-406186ea4fc5",
            "to_address": recipient_email,
        },
    )

#alert_object = gmp.get_alerts(filter_string=f"name={recipient_email}")
#alert = alert_object.xpath("alert")

# alert_id = alert[0].get("id", "no id found")
# if debug:
#     print(f"alert_id: {str(alert_id)}")




#gmp.create_alert(
#    name="Alert_Test",
#    comment=f"Created: {time.strftime('%Y/%m/%d-%H:%M:%S')}",
#    alert_event_data={"status": "Done"},
#    alert_event=AlertEvent.TASK_RUN_STATUS_CHANGED,
#    alert_method=gmp.types.AlertMethod.EMAIL,
#    method_data={
#        "message": "Task '$n': $e",
#        "notice": "2",
#        "from_address": sender_email,
#        "subject": "[Greenbone] Task",
#        "notice_attach_format": "c402cc3e-b531-11e1-9163-406186ea4fc5",
#        "to_address": recipient_email,
#    },
#    condition=gmp.types.AlertCondition.ALWAYS
#    )
