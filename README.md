# Greenbone Vulnerability Manager 22.4.x Python tools #

## Python scripts that can be used to configure your Greenbone Source Edition (OpenVAS) Scanner ###
I hope these will make your life a little easier managing Greenbone/OpenVAS.

[API Reference for GVM 22.5](https://docs.greenbone.net/API/GMP/gmp-22.5.html)

[Python GVM API](https://greenbone.github.io/python-gvm/api/api.html)

----
### 2024-04-06 - stop scans from csv or stop all running or requested scans
- stop-all-scans.gmp.py, stop-scans-from-csv.gmp.py.
- GvmResponseErrors handled in those scripts + start-scans-from-csv.gmp.py

### 2024-04-05 - create filters and list filters
- list-tickets and list-policies.

### 2024-04-03 - create filters and list filters
- Creates filters and assign them to different types (alerts, tasks, targets, reports, etc.)

## Latest changes ##
### 2024-04-04 - Additional error-handling of GvmResponseErrors + clean-sensor updates 
- GvmResponseErrors handled in create-* scripts.
- clean-sensor.gmp.py now also deletes alerts, filters, schedules, and tags

### 2024-04-02 - create tags and list tags 
- Creates tags and assigns the to resources.
- Filters are evaluated at creation time, so new reports from the same task created after script is run won't be tagged. Would've been nice if they were re-evaluated at regular intervals.

### 2024-04-01 - Additional scripts and further details from list-* 
- list-users, list-groups, list-roles are new.
- Most other list-* scripts provide further details
- prepare-scanner.sh will add credentials, schedules, alerts, targets, and tasks as defined in the csv files for each of those, running the associated create-* scripts.

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
When you just want to get the XML from Greenbone to look for values/value names, it's easy to use gvm-cli, like this: 
- gvm-cli --gmp-username *admin-user* --gmp-password *password* socket --xml="<get_alerts/>"

## Python Scripts in this repo:
### clean-sensor.gmp.py ###
**Script provided by Greenbone as part of GVM-Tools. Used when cleaning up after testing scripts (or starting over)**
- Usage: gvm-script --gmp-username admin --gmp-password '0f6fa69b-32bb-453a-9aa4-b8c9e56b3d00' socket export-csv-report.gmp.py *report_uuid* ./output.csv
- Other example scripts from Greenbone can be found here: https://github.com/greenbone/gvm-tools/tree/main/scripts 

### create-Alerts-from-csv.gmp.py ###
**Creates alerts as specified in a csv-file. See alerts.csv for file format/contents.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-alerts-from-csv.gmp.py alerts.csv
- For SMB Alerts use something like %N_%CT%z in the naming of the report, as shown in the example alerts.csv
- %N is the name for the object or the associated task for reports, %C is the creation date in the format YYYYMMDD, and %c is the creation time in the format HHMMSS.
- The script only support EMAIL and SMB Alerts, please note that the fields are quite different between the two alert types, but refer to the sample alerts.csv
- The CSV must starts with name, type (EMAIL or SMB). The remaining fields then depend on the type chosen, specifically:
- EMAIL; *senders email*, *recipients email*, *mail subject*, *message body*, *notice type* (0=Report in message 1=Simple Notice or 2=Attach Report), *Report Type* (e.g. CSV Results), *Status* (Done, Requested)
- SMB; *SMB Credentials*,*SMB Share Path*,*Report Name*, *Report Folder* (if not stored in the root of the share), *Not used*, *Report Type* (e.g. CSV Results), *Status* (Done, Requested)
- A simple example below with 1 EMAIL alert and 1 SMB Alert.
Alert_EMAIL_Stop,EMAIL,"martin@example.org","noc@example.org","Message Subject","Message Body",1,"CSV Results","Stop Requested"
Alert_SMB_Done,SMB,"Cred_Storage_SMB","\\smbserver\share","%N_%CT%cZ","Reports",,"CSV Results","Done"

**Note**: This script relies on credentials as/if specified in alerts.csv as well as a working SMTP server on the Greenbone primary server. If you're using SMB add the required credentials first using [create-credentials-from-csv.gmp.py](#create-credentials-from-csvgmppy).


### create-schedules-from-csv.gmp.py ###
**Creates schedules as specified in a csv-file. See schedules.csv for file format/contents.**
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
**Creates credentials as specified in a csv-file. See credentials.csv for file format/contents.**
Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-credentials-from-csv.gmp.py ./credentials.csv
**Note**: create schedules, then credentials, then targets, then tasks and make sure to use the same names between the input csv-files.
The sample files should serve as an example.

### create-filters-from-csv.gmp.py ###
**Creates filters as specified in a csv-file. See filters.csv for file format/contents.**
-  Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-filters-from-csv.gmp.py ./filters.csv
- CSV-file; filterType, filterName, filterDescription, filterTerm, where
    - filterType is one of Alert, Config (scan-config), Credential, Report, Scanner, Schedule, Target, or Task.
    - filterName is the name of the filter.
    - filterDescription is your description of the filter.
    - FilterTerm is the actual term used to define the filter, such as \~Labnet.

### create-tags-from-csv.gmp.py ###
**Creates tags as specified in a csv-file. See tags.csv for file format/contents.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-tags-from-csv.gmp.py ./tags.csv 
- May contain up to 10 resources to assign to tag. Currently only creates tags for Credential, Target, and Tasks
- Use tag:*searchforthis* as filter. Example: *tag:bsecure*
- Will add reports when I've figured out if tags are really dynamic and a filter will do it for new reports. 

### create-targets-from-csv.gmp.py ###
**Creates targets as specified in a csv-file. See targets.csv for file format/contents.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-targets-from-csv.gmp.py ./targets.csv  
- Alive test can be:

No | Alive Test | Notes
---|---|---
1 | Scan Config Default | ICMP Ping is used by default with the Built-in Scan Configurations
2 | ICMP Ping | ICMP echo request and echo reply messages
3 | TCP-ACK Service Ping | Sends TCP packets with only the ACK bit set. Target is required by [RFC 793](http://www.rfc-editor.org/rfc/rfc793.txt) to respond with a RST packet
4 | TCP-SYN Service Ping | SYN only scans (never sends an ACK even if target replies with SYN/ACK)
5 | ICMP & TCP-ACK Service Ping | ICMP & TCP-ACK tests combined
6 | ICMP & ARP Ping | ICMP Ping & sends a broadcast ARP request to solicit a reply from the host that uses the specified IP address
7 | TCP-ACK Service & ARP Ping | TCP-ACK and ARP Ping combined
8 | ICMP, TCP-ACK Service & ARP Ping | ICMP, TCP-ACK, and ARP Ping combined
9 | Consider Alive | Consider the target alive. This may take considerably longer to finish.


### create-tasks-from-csv.gmp.py ###
**Creates tasks as specified in a csv-file. See tasks.csv for file format/contents**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-tasks-from-csv.gmp.py ./task.csv  <br/><br/>
- Change Hosts Scan Ordering by changing #5 within CSV to Random, Sequential or Reverse in script.
- Specify up to 5 alerts in CSV, blanks will be discarded.
**Note**: Make sure that all other configurations that the tasks may rely on are already created, including alerts, schedules, credentials, and targets,
in other words if it is referenced in tasks.csv it must already exist.

### empty-trash.gmp.py ###
- Does what is says on the tin, empties the trashcan in Greenbone.
- Use it when you're testing like crazy and have a trashcan with ~ a gazillion objects
- You can also just use gvm-cli --gmp-username *admin-user* --gmp-password *password* socket --pretty --xml="<empty_trashcan/>"

### export-csv-report.gmp.py ###
**Requests the report specified and exports it as a csv formatted report locally.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket export-csv-report.gmp.py *report_uuid* ./output.csv
- Get the *report_uuid* with list-reports.gmp.py or find it in the UI. If the output is not specified it will be named *report_uuid.csv*
- Note the only changes to this script is an added ignore_pagination=True, details=True to get the full report.  

### export-pdf-report.gmp.py ###
**Requests the report specified and exports it as a pdf formatted report locally.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket export-pdf-report.gmp.py *report_uuid* ./output.pdf
- Get the *report_uuid* with list-reports.gmp.py or find it in the UI. If the output is not specified it will be named *report_uuid.pdf*
**Note**: the only changes to this script is an added ignore_pagination=True, details=True to get the full report.  

## list-alerts.gmp.py ###
**Lists all alerts configured with name and uuid.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-alerts.gmp.py  

## list-credentials.gmp.py ###
**Lists all credentials configured with name and uuid.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-credentials.gmp.py  
- returns Credential uuid, Name, Type, & if insecure use is allowed

### list-feeds.gmp.py ###
**Lists feeds and their status.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-feeds.gmp.py  

### list-filters.gmp.py ###
**Lists filters.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-filters.gmp.py
- Returns Filter Name, uuid, type, and the term (filter)  

### list-groups.gmp.py ###
**Lists all groups**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-groups.gmp.py
- Returns Group Name, uuid, members

### list-policies.gmp.py ###
**Lists compliance policies.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-policies.gmp.py  

### list-portlists.gmp.py ###
**Lists port lists.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-portlists.gmp.py  

### list-report-formats.gmp.py ###
**Lists all report formats with name and uuid.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-report-formats.gmp.py  

### list-reports.gmp.py ###
**Lists all reports that have specified status**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-reports.gmp.py *Status*
- where status is "All", "Requested", "Queued", "Interrupted", "Running", "Stop Requested", "Stopped", or "Done"
- Case matters, so "Done" or "Stopped" will work while "done" or "stopped" will not.
- Script now shows, in percentage, how far the scan/report is.
- There are no reports generated before at least one scan task has been started.  

### list-roles.gmp.py ###
**Lists all roles**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-roles.gmp.py
- Returns Role Name, uuid, members

### list-scan-configs.gmp.py ### 
**Lists all scan configs.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-scan-configs.gmp.py  

### list-scanners.gmp.py ###
**Lists all scanners currently configured.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-scanners.gmp.py
- Returns the scanners Name, uuid, the host on which it resides, port used, creation and modification time (note CVE scanner does not return a host and sockets are local)

## list-schedules.gmp.py ###
**Lists all schedules configured with name, uuid, timezone, and iCalendar information.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-schedules.gmp.py  

### list-tags.gmp.py ###
**Lists all tags currently configured.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-tags.gmp.py
- Returns Tag name, uuid, Modified Date, Value, Type, and Count of ressources assigned to tag.

### list-targets.gmp.py ###
**Lists all targets currently configured.**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-targets.gmp.py
- No targets configured by default, however using the provided files in this repo, you should now have a few (5).
- Returns targets Name, uuid, number of Hosts, and credentials (SSH, SMB, ESXi, & SNMP Credentials)

### list-tasks.gmp.py ###
**Lists all tasks configured**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-tasks.gmp.py
- No tasks configured by default, however using the provided files in this repo, you should now have some (9).
- Returns the tasks Name, uuid, Target, Scanner, the order in which hosts are scanned¹, and the highest severity (empty if no reports)

### list-tickets.gmp.py ###
**Lists all tickets created**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-tickets.gmp.py
- Returns the tickets name, Host, Associated Task, Status, and Note (depending on status either Open-, Fixed-, or Closed note).

### list-users.gmp.py ###
**Lists all users**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-users.gmp.py
- Returns user Name, uuid, role, groups


¹ The default order is "None" which equals sequential, meaning that if this field is empty scanning will be sequential as it will be if specifically set to sequential. Possible results are None, Sequential, Reverse, or Random.

### start-scans-from-csv.gmp.py ###
**starts scans (tasks) specified in csv file**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket start-scans-from-csv.gmp.py *csv-file with task names*
- Starts the tasks specified in the file (example startscan.csv)
- Returns the number of tasks started.

### stop-all-scans.gmp.py ###
**stops scans (tasks) that are in status running, queued, or requested**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket stop-all-scans.gmp.py
- Stops all scans
- Returns the number of tasks stopped.

### stop-scans-from-csv.gmp.py ###
**stops scans (tasks) specified in csv file**
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket stop-scans-from-csv.gmp.py *csv-file with task names*
- Stops the tasks specified in the file (example startscan.csv works for both scripts)
- Returns the number of tasks stopped.

----

## Other files
### alerts.csv
- Example csv-file to use with create-alerts-from-csv.gmp.py

### credentials.csv
- Example csv-file to use with create-credentials-from-csv.gmp.py 

### schedules.csv
- example csv-file to use with create-schedules-from-csv.gmp.py

### tags.csv
- Example csv-file to use with create-tags-from-csv.gmp.py

### targets.csv
- Example csv-file to use with create-targets-from-csv.gmp.py  

### tasks.csv
- Example csv-file to use with create-tasks-from-csv.gmp.py  

### prepare-scanner.sh
- Usage: provide GMP Username and Password and the script will add credentials, schedules, alerts, targets, and tasks as defined in the csv files for each of those.
- Provide your own files csv-files together with other relevant files, such as SSH-keys before executing the script.
- **Important** Delete all of the above after running the script as they contain critical information (the GVM database encrypts the information, but these files are clear-text)

## Tips and tricks
### Using filters with gvm-cli
- gvm-cli --gmp-username *admin-user* --gmp-password *password* socket --pretty --xml="<get_alerts filter='name=Alert_Email_Done'/>"

### Creating reports with gvm-cli
gvm-cli --gmp-username admin --gmp-password 8274105c-dabc-4223-8e5c-3eceb812477f socket --pretty --xml='<get_reports report_id="a248c4e1-f098-4ea9-888b-b3455e9880fa" report_format_id="c402cc3e-b531-11e1-9163-406186ea4fc5" filter="rows=-1"/>'

### Some PostGreSql stuff
Checking size of gvmd Postgres db
- sudo -u postgres -i psql
- SELECT pg_size_pretty( pg_database_size('gvmd'));

 pg_size_pretty 
----------------
 2847 MB
(1 row)

Other db stuff
- \l+ - lists databases
- \c gvmd - connects to the gvmd database
- SELECT * FROM alerts; - shows all data in table alerts