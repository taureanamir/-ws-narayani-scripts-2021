#!/bin/bash
#====================================================================================================+
# DEFINE DIRECTORY AND WORKDIR
#====================================================================================================+
export WORKDIR=$HOME/ws-narayani-scripts-2021
cd $WORKDIR
#====================================================================================================+
# YESTERDAY
#====================================================================================================+
day1="$(date +'%d-%m-%Y')"
yesterday="$(date +'%b%d%y' --date='-1 day')"
echo $yesterday
url="https://flood-npl.rimes.int/wrf_data_rimes/NAR/"$yesterday"/W650_"$yesterday".txt"
if curl --output /dev/null --silent --head --fail "$url"; then
  echo "-----------------------------------------------------"
  echo "Forecast data available: $url"
  echo "-----------------------------------------------------"
  # RUN get rainfall bias correction script ---------------+
  echo "-----------------------------------------------------"
  echo " Get forecast rainfall !!!"
  echo "-----------------------------------------------------"
  python 01_get_forecast_rainfall.py
  # RUN create control file for hec-hms model -------------+
  # CURRENTLY RUN FILE NOT UPDATED
  echo "-----------------------------------------------------"
  echo " Create HEC-HMS control file !!!"
  echo "-----------------------------------------------------"
  python 02_create_control_file_hec_hms_model.py
  # BASH/SHELL script of HEC-HMS,HEC-DSSVUE ---------------+
  echo "-----------------------------------------------------"
  echo " Execute HEC HMS model !!! "
  echo "-----------------------------------------------------"
  bash 03_process_hec_dssvue.sh
  # RUN insert data into database -------------------------+
  echo "-----------------------------------------------------"
  echo " Insert into DB "
  echo "-----------------------------------------------------"
  python 04_insert_simulated_discharge_water_level.py
  echo "-----------------------------------------------------"
  #--------------------------------------------------------+
else
  echo "Forecast data not available: $url"
fi
