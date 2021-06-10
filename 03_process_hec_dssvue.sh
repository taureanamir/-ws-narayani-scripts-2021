#!/bin/bash
#=============================================================================+
# WORKDIR, HEC-HMS, HEC-DSSVUE SCRIPTS 
#=============================================================================+
hecdssvue='/home/rimesnp/hec-dssvue201/hec-dssvue.sh'
hechms421='/home/rimesnp/hec-hms-421/hec-hms.sh'
#=============================================================================+
DISPLAY=":1.0"
export DISPLAY
#=============================================================================+
# Execute the program here....
#=============================================================================+
$hecdssvue 03_1_write_to_input_dss.py
$hechms421 -s /home/rimesnp/ws/Narayani_model_2021/model/Narayani4.script
$hecdssvue 03_2_get_station_flow_and_stage.py
