# Greenbone Vulnerability Manager 22.4.x Python tools #

### Python scripts that can be used to configure your Greenbone Source Edition (OpenVAS) Scanner ###
I hope these will make your life a little easier managing Greenbone/OpenVAS.  <br/><br/> 

----

## Latest changes ##

### 2022-12-17 - Scripts and updated readme ###
- First version of Python code

## Running Python GVM Scripts
For details on Python GVM, please refer to https://gvm-tools.readthedocs.io/en/latest/scripting.html#gvm-scripts


## Python Scripts in this repo:
### clean-sensor.gmp.py ###
**Script provided by Greenbone as part of GVM-Tools. Used when cleaning up after testing scripts (or starting over)**<br/><br/> 
- Usage: gvm-script --gmp-username admin --gmp-password '0f6fa69b-32bb-453a-9aa4-b8c9e56b3d00' socket export-csv-report.gmp.py *report_uuid* ./output.csv
- Other example scripts from Greenbone can be found here: https://github.com/greenbone/gvm-tools/tree/main/scripts <br/><br/> 

### create-credentials-from-csv.gmp.py ###
**Creates credentials as specified in a csv-file. See credentials.csv for file format/contents.**<br/><br/> 
Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-credentials-from-csv.gmp.py ./credentials.csv
Note: create credentials, then targets, then tasks and make sure to use the same names between the input csv-files.
The sample files should serve as an example.<br/><br/> 

### create-targets-from-csv.gmp.py ###
**Creates targets as specified in a csv-file. See targets.csv for file format/contents.**<br/><br/> 
Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-targets-from-csv.gmp.py ./targets.csv  <br/><br/> 

### create-tasks-from-csv.gmp.py ###
**Creates tasks as specified in a csv-file. See tasks.csv for file format/contents**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket create-tasks-from-csv.gmp.py ./task.csv  <br/><br/> 

### export-csv-report.gmp.py ###
**Requests the report specified and exports it as a csv formatted report locally.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket export-csv-report.gmp.py *report_uuid* ./output.csv
- Get the *report_uuid* with list-reports.gmp.py or find it in the UI. If the output is not specified it will be named *report_uuid.csv*
- Note the only changes to this script is an added ignore_pagination=True, details=True to get the full report.  <br/><br/> 

### export-pdf-report.gmp.py ###
**Requests the report specified and exports it as a pdf formatted report locally.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket export-pdf-report.gmp.py *report_uuid* ./output.pdf
- Get the *report_uuid* with list-reports.gmp.py or find it in the UI. If the output is not specified it will be named *report_uuid.pdf*
- Note the only changes to this script is an added ignore_pagination=True, details=True to get the full report.  <br/><br/> 

## list-credentials.gmp.py ###
**Lists all credentials configured with name and uuid.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-credentials.gmp.py  <br/><br/> 

### list-report-formats.gmp.py ###
**Lists all report formats with name and uuid.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-report-formats.gmp.py  <br/><br/> 

### list-reports.gmp.py ###
**Lists all reports that have finished (status=done)**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-reports.gmp.py
- There are no reports generated before at least one scan task has completed.  <br/><br/> 

### list-scanner-configs.gmp.py ###<br/><br/> 
**Lists all scan configs.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-scanner-configs.gmp.py  <br/><br/> 

### list-scanners.gmp.py ###
**Lists all scanners currently configured.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-scanners.gmp.py  <br/><br/> 

### list-targets.gmp.py ###
**Lists all targets currently configured.**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-targets.gmp.py
- No targets configured by default, however using the provided files in this repo, you should now have a few (5).<br/><br/> 

### list-tasks.gmp.py ###
**Lists all tasks configured**<br/><br/> 
- Usage: gvm-script --gmp-username *admin-user* --gmp-password *password* socket list-tasks.gmp.py
- No tasks configured by default, however using the provided files in this repo, you should now have some (9).<br/><br/> 

----

## Other files
### credentials.csv ###
- Example csv-file to use with create-credentials-from-csv.gmp.py  <br/><br/> 

### targets.csv ###
- Example csv-file to use with create-targets-from-csv.gmp.py  <br/><br/> 

### tasks.csv ###
- Example csv-file to use with create-tasks-from-csv.gmp.py  <br/><br/> 
