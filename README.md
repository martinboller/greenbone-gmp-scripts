# Greenbone Vulnerability Manager 22.4.x Python tools #

## Python scripts that can be used to configure your Greenbone Source Edition (OpenVAS) Scanner ###
I hope these will make your life a little easier managing Greenbone/OpenVAS.

[API Reference for GVM 22.4](https://docs.greenbone.net/API/GMP/gmp-22.4.html)

----

## Latest changes ##
### 2023-12-15 - Script to create alerts ###
- Added create-alerts-from-csv.gmp.py
- Added template alerts.csv
- Updated credentials.csv to add SMB credentials for "storage" as this should be different from the credentials used for scanning
- Updated create_tasks_from_csv.gmp.py and template tasks.csv to add up to 4 alerts per task.

### 2023-11-25 - Additional script to create schedules ###
- Added create-schedules-from-csv.gmp.py
- Updated create-tasks-from.csv.gmp.py to lookup schedule Ids from schedule name to add to tasks created.
- Created sample schedules.csv for reference.
- Updated tasks.csv with schedules.

### 2023-05-20 - Additional script for feeds ###
- Adjustments to export-*xxx*-report scripts to add extension
- Added list-feeds.gmp.py
- Script list-reports.gmp.py now show finish percentage and you can now specify "All".

### 2022-12-17 - Scripts and updated readme ###
- First version of Python code

## Running Python GVM Scripts
For details on Python GVM, please refer to https://gvm-tools.readthedocs.io/en/latest/scripting.html#gvm-scripts, but for these scripts, use
- gvm-script --gmp-username *admin-user* --gmp-password *password* socket *script-name* - Example:
- gvm-script --gmp-username admin --gmp-password SecretPassword socket list-alerts.gmp.py
When you just want to get the XML from Greenbone to look for values/value names, it's easy to use gvm-cli, like this: <br/><br/> 
- gvm-cli --gmp-username *admin-user* --gmp-password *password* socket --xml="<get_alerts/>"

## Python Scripts in this repo:
### clean-sensor.gmp.py ###
**Script provided by Greenbone as part of GVM-Tools. Used when cleaning up after testing scripts (or starting over)**<br/><br/> 
- Usage: gvm-script --gmp-username admin --gmp-password '0f6fa69b-32bb-453a-9aa4-b8c9e56b3d00' socket export-csv-report.gmp.py *report_uuid* ./output.csv
- Other example scripts from Greenbone can be found here: https://github.com/greenbone/gvm-tools/tree/main/scripts <br/><br/> 

### create-Alerts-from-csv.gmp.py ###
**Creates alerts as specified in a csv-file. See alerts.csv for file format/contents.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-alerts-from-csv.gmp.py alerts.csv
- For SMB Alerts use something like %N_%CT%z in the naming of the report, as shown in the example alerts.csv
- %N is the name for the object or the associated task for reports, %C is the creation date in the format YYYYMMDD, and %c is the creation time in the format HHMMSS.
- The script only support EMAIL and SMB Alerts, please note that the fields are quite different between the two alert types, but refer to the sample alerts.csv
- The CSV must starts with name, type (EMAIL or SMB). The remaining fields then depend on the type chosen, specifically:
- EMAIL; *senders email*, *recipients email*, *mail subject*, *message body*, *notice type* (0=Simple Notice 1=Report in message or 2=Attach Report), *Report Type* (e.g. CSV Results), *Status* (Done, Requested)
- SMB; *SMB Credentials*,*SMB Share Path*,*Report Name*, *Report Folder* (if not stored in the root of the share), *Not used*, *Report Type* (e.g. CSV Results), *Status* (Done, Requested)
- A simple example below with 1 EMAIL alert and 1 SMB Alert.
Alert_EMAIL_Stop,EMAIL,"martin@bollers.dk","noc@bollers.dk","Message Subject","Message Body",0,"CSV Results","Stop Requested"
Alert_SMB_Done,SMB,"Cred_Storage_SMB","\\smbserver\share","%N_%CT%cZ","Reports",,"CSV Results","Done"

**Note**: This script relies on credentials as/if specified in alerts.csv as well as a working SMTP server on the Greenbone primary server. If you're using SMB add the required credentials first using [create-credentials-from-csv.gmp.py](#create-credentials-from-csvgmppy).


### create-schedules-from-csv.gmp.py ###
**Creates schedules as specified in a csv-file. See schedules.csv for file format/contents.**<br/><br/> 
Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-schedules-from-csv.gmp.py ./schedules.csv
**Note**: create schedules, then credentials, then targets, then tasks and make sure to use the same names between the input csv-files.
The sample files should serve as examples, however a short explanation of a VCALENDAR stream exported from Greenbone below¹.

Example Key:Value pair | Comment
---|---
BEGIN:VCALENDAR | Begin VCalendar Entry
VERSION:2.0 | iCalendar Version number
PRODID:-//Greenbone.net//NONSGML Greenbone Security Manager 23.1.0//EN | As generated by Greenbone replace with something else if you want to
BEGIN:VEVENT | Start of Vevent
DTSTART:20231125T220000Z | Start date
DURATION:PT1H | Duration of scan. PT0S means "Entire Operation". S = seconds, M = minutes, H = hours
RRULE:FREQ=HOURLY;INTERVAL=4 | Frequency; Yearly, Monthly, Weekly, Hourly. Optionally Interval withs same unit
DTSTAMP:20231125T212042Z | Date stamp created
END:VEVENT | End Vevent
END:VCALENDAR | End VCalendar Entry

¹ See also https://www.rfc-editor.org/rfc/rfc5545.txt Internet Calendaring and Scheduling Core Object Specification (iCalendar)

### create-credentials-from-csv.gmp.py ###
**Creates credentials as specified in a csv-file. See credentials.csv for file format/contents.**<br/><br/> 
Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-credentials-from-csv.gmp.py ./credentials.csv
**Note**: create schedules, then credentials, then targets, then tasks and make sure to use the same names between the input csv-files.
The sample files should serve as an example.<br/><br/> 

### create-targets-from-csv.gmp.py ###
**Creates targets as specified in a csv-file. See targets.csv for file format/contents.**<br/><br/> 
Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-targets-from-csv.gmp.py ./targets.csv  <br/><br/> 

### create-tasks-from-csv.gmp.py ###
**Creates tasks as specified in a csv-file. See tasks.csv for file format/contents**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-tasks-from-csv.gmp.py ./task.csv  <br/><br/> 
**Note**: Make sure that all other configurations that the tasks may rely on are already created, including alerts, schedules, credentials, and targets,
in other words if it is referenced in tasks.csv it must already exist.

### empty-trash.gmp.py ###
- Does what is says on the tin, empties the trashcan in Greenbone.
- Use it when you're testing like crazy and have a trashcan with ~ a gazillion objects
- You can also just use gvm-cli --gmp-username *admin-user* --gmp-password *password* socket --pretty --xml="<empty_trashcan/>"

### export-csv-report.gmp.py ###
**Requests the report specified and exports it as a csv formatted report locally.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket export-csv-report.gmp.py *report_uuid* ./output.csv
- Get the *report_uuid* with list-reports.gmp.py or find it in the UI. If the output is not specified it will be named *report_uuid.csv*
- Note the only changes to this script is an added ignore_pagination=True, details=True to get the full report.  <br/><br/> 

### export-pdf-report.gmp.py ###
**Requests the report specified and exports it as a pdf formatted report locally.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket export-pdf-report.gmp.py *report_uuid* ./output.pdf
- Get the *report_uuid* with list-reports.gmp.py or find it in the UI. If the output is not specified it will be named *report_uuid.pdf*
**Note**: the only changes to this script is an added ignore_pagination=True, details=True to get the full report.  <br/><br/> 

## list-alerts.gmp.py ###
**Lists all alerts configured with name and uuid.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-alerts.gmp.py  <br/><br/> 

## list-credentials.gmp.py ###
**Lists all credentials configured with name and uuid.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-credentials.gmp.py  <br/><br/> 

### list-feeds.gmp.py ###
**Lists feeds and their status.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-feeds.gmp.py  <br/><br/> 

### list-portlists.gmp.py ###
**Lists port lists.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-portlists.gmp.py  <br/><br/> 

### list-report-formats.gmp.py ###
**Lists all report formats with name and uuid.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-report-formats.gmp.py  <br/><br/> 

### list-reports.gmp.py ###
**Lists all reports that have specified status**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-reports.gmp.py *Status*
- where status is "All", "Requested", "Queued", "Interrupted", "Running", "Stop Requested", "Stopped", or "Done"
- Case matters, so "Done" or "Stopped" will work while "done" or "stopped" will not.
- Script now shows, in percentage, how far the scan/report is.
- There are no reports generated before at least one scan task has been started.  <br/><br/> 

### list-scan-configs.gmp.py ### 
**Lists all scan configs.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-scan-configs.gmp.py  <br/><br/> 

### list-scanners.gmp.py ###
**Lists all scanners currently configured.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-scanners.gmp.py
- Returns the scanners Name, uuid, & the host on which it resides (note CVE scanner does not return a host and sockets are local)

## list-schedules.gmp.py ###
**Lists all schedules configured with name, uuid, timezone, and iCalendar information.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-schedules.gmp.py  <br/><br/> 

### list-targets.gmp.py ###
**Lists all targets currently configured.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-targets.gmp.py
- No targets configured by default, however using the provided files in this repo, you should now have a few (5).
- Returns targets Name, uuid, number of Hosts, and credentials (SSH, SMB, ESXi, & SNMP Credentials)

### list-tasks.gmp.py ###
**Lists all tasks configured**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-tasks.gmp.py
- No tasks configured by default, however using the provided files in this repo, you should now have some (9).
- Returns the tasks Name, uuid, Target, Scanner, and the highest severity (empty if no reports)

### start-scans-from-csv.gmp.py ###
**starts scans (tasks) specified in csv file**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket start-scans-from-csv.gmp.py *csv-file with task names*
- Starts the tasks specified in the file (example startscan.csv)
- Returns the number of tasks started.

----

## Other files
### alerts.csv
- Example csv-file to use with create-alerts-from-csv.gmp.py

### credentials.csv ###
- Example csv-file to use with create-credentials-from-csv.gmp.py  <br/><br/> 

### targets.csv ###
- Example csv-file to use with create-targets-from-csv.gmp.py  <br/><br/> 

### tasks.csv ###
- Example csv-file to use with create-tasks-from-csv.gmp.py  <br/><br/> 

## Tips and tricks
### Using filters with gvm-cli
- gvm-cli --gmp-username *admin-user* --gmp-password *password* socket --pretty --xml="<get_alerts filter='name=Alert_Email_Done'/>"

### Creating reports with gvm-cli
gvm-cli --gmp-username admin --gmp-password 8274105c-dabc-4223-8e5c-3eceb812477f socket --pretty --xml='<get_reports report_id="a248c4e1-f098-4ea9-888b-b3455e9880fa" report_format_id="c402cc3e-b531-11e1-9163-406186ea4fc5" filter="rows=-1"/>'
