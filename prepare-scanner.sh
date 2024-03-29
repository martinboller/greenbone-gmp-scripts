#! /bin/bash

if [[ -z $1 ]]; then
	echo -e "\e[1;31mNo GMP Username supplied, use prepare-scanner.sh gmp-username gmp-password\e[1;0m"
	echo -e
	echo -e "\e[1;32mExample: ./prepare-scanner.sh admin d2b29ee7-ba2d-4d1f-a893-76bad744268e\e[1;0m"
	exit 1
else
	GMPUSERNAME=$1
fi

if [[ -z $2 ]]; then
	echo -e "\e[1;31mNo GMP Password supplied, use prepare-scanner.sh gmp-username gmp-password\e[1;0m"
	echo -e
	echo -e "\e[1;32mExample: ./prepare-scanner.sh admin d2b29ee7-ba2d-4d1f-a893-76bad744268e\e[1;0m"
    exit 1
else
	GMPPASSWORD=$2
fi

# Create Credentials
gvm-script --gmp-username $GMPUSERNAME --gmp-password $GMPPASSWORD socket create-credentials-from-csv.gmp.py credentials.csv

# Create Schedules
gvm-script --gmp-username $GMPUSERNAME --gmp-password $GMPPASSWORD socket create-schedules-from-csv.gmp.py schedules.csv

# Create Alerts
gvm-script --gmp-username $GMPUSERNAME --gmp-password $GMPPASSWORD socket create-alerts-from-csv.gmp.py alerts.csv

# Create Targets
## Make sure that required (default) port lists are available before creating targets
PORTLISTS=$(gvm-script --gmp-username $GMPUSERNAME --gmp-password $GMPPASSWORD socket list-portlists.gmp.py)
if [[ -z $PORTLISTS ]]; then
    echo -e "\e[1;31mNo portlists, exiting\e[1;0m"
else
    ## Now create the targets
    gvm-script --gmp-username $GMPUSERNAME --gmp-password $GMPPASSWORD socket create-alerts-from-csv.gmp.py alerts.csv
fi

# Create Tasks
## Make sure that the required Scan Configurations are available before creating tasks
SCANCONFIGS=$(gvm-script --gmp-username $GMPUSERNAME --gmp-password $GMPPASSWORD socket list-scan-configs.gmp.py)
if [[ -z $PORTLISTS ]]; then
    echo -e "\e[1;31mNo scan configs, exiting\e[1;0m"
else
    ## Now create the Tasks
    gvm-script --gmp-username $GMPUSERNAME --gmp-password $GMPPASSWORD socket create-tasks-from-csv.gmp.py tasks.csv
fi