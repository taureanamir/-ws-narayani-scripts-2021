#!/usr/bin/python
"""
This script extracts the water discharge and water level from the HEC HMS DSS file
"""
#==========================================================================================================+
# IMPORT LIBRARIES
#==========================================================================================================+

from hec.heclib.dss import *
from hec.script import *
from hec.dataTable import *
import time
import datetime
import java, os


#==========================================================================================================+
# FUNCTION TO READ GET DATA AND OUTPUT xls FILE FLOW-COMBINE and STAGE
#==========================================================================================================+

def makeDir(path):
  if not os.path.exists(path):
    os.makedirs(path)

def get_flow_combine_and_stage(station_name, station_alias, station_id, dt_start, dt_end, pStartDate, pEndDate):
  file_path = os.path.normpath("/home/rimesnp/ws-narayani-scripts-2021/Flow_Stage_output_files/")
  file_name = station_alias + "_flow_combine_stage.csv"
  makeDir(file_path)

  try:
    dssfile = HecDss.open("/home/rimesnp/ws/Narayani_model_2021/model/New_Run.dss",dt_start,dt_end)
    flow = dssfile.get("//"+station_name+"/FLOW-COMBINE//1DAY/RUN:NEW_RUN/")
    stage = dssfile.get("//"+station_name+"/STAGE//1DAY/RUN:NEW_RUN/")
  except java.lang.Exception, e :
    # Take care of any missing data or errors
    MessageBox.showError(e.getMessage(), "Error reading data")
  
  # convert flow and stage data into required format
  flow_data = flow.values.tolist()
  stage_data = stage.values.tolist()

  pEndDate = pEndDate + datetime.timedelta(days=1)
  days = [pStartDate + datetime.timedelta(days=x) for x in range((pEndDate - pStartDate).days)]
  # print(len(flow_data))
  # print(len(stage_data))
  # print(len(days))

  len_flowData = len(flow_data)
  len_stageData = len(stage_data)

  # constant UNKNOWN
  UNKNOWN = "NA"
  header = "Date,Station_Name,Station_ID,Discharge,Water_Level\n"
  _file = open(os.path.join(file_path, file_name), "w")
  _file.write(header)
  
  if len_flowData != 0 and len_stageData == 0:
    base_stage_value = UNKNOWN
    for i in range(len_flowData):
      line = str(days[i]) + "," + station_alias + "," + str(station_id) + "," + str(flow_data[i]) + "," + str(base_stage_value) + "\n"
      _file.write(line)

  elif len_flowData == 0 and len_stageData != 0:
    base_flow_value = UNKNOWN
    for i in range(len_stageData):
      line =  str(days[i]) + "," + station_alias + "," + str(station_id) + "," + str(base_flow_value) + "," + str(stage_data[i]) + "\n"
      _file.write(line)
  else:
    for i in range(len_stageData):
      line =  str(days[i]) + "," + station_alias + "," + str(station_id) + "," + str(flow_data[i]) + "," + str(stage_data[i]) + "\n"
      _file.write(line)

  _file.close()

  
#==========================================================================================================+
## dd/mm/yyyy format
#==========================================================================================================+

tm = (time.strftime("%d/%m/%Y"))
tm = tm.split('/')
day = tm[0]
month_name = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
mn = month_name[int(tm[1])-1].upper()
year = tm[2]
#dt_start = day+mn+year+" "+"0800"
#print dt_start
# DAY AFTER TOMORROW
today = datetime.date.today()
#==========================================================================================================+
# START DATE 2 WEEKS AGO
#==========================================================================================================+
st_dt = today - datetime.timedelta(days=14)
start_date = st_dt
st_dt = st_dt.strftime("%d/%m/%Y")
temp_st = st_dt.split('/')
temp_st_day = temp_st[0]
temp_st_mn = month_name[int(temp_st[1])-1].upper()
temp_st_yr = temp_st[2]
temp_st_t = temp_st_day + temp_st_mn + temp_st_yr
dt_start = temp_st_t+" "+"0800"
dt_start_DDMMYYYY = st_dt
print "------------------------------"
print "Start date: " + dt_start
print "------------------------------"
after_tomorrow = today + datetime.timedelta(days=2)
end_date = after_tomorrow
after_tomorrow = after_tomorrow.strftime("%d/%m/%Y")
temp_after = after_tomorrow.split('/')
temp_after_day = temp_after[0]
temp_after_mn = month_name[int(temp_after[1])-1].upper()
temp_after_yr = temp_after[2]
temp_af_t = temp_after_day + temp_after_mn + temp_after_yr
dt_end = temp_af_t+" "+"0800"
dt_end_DDMMYYYY = after_tomorrow
print "End date:   " + dt_end
print "------------------------------"
# OUTLET FLOW
#dt_start = "01JAN2017 0800"
#dt_end = "31DEC2019 0800"


# Data of following stations are available but we use the stations defined in "stations" variable
# flow_outlet = ['ARUGHAT','BETRAWOTI','BIMALNAGAR','BORLANGPUL','DEVGHAT','JOMSOM',
#               'KALIKHOLA','KOTAGAUN','KUMALGAUN','RAJAIYA','SETIDAMAULI_430.5','SISAGHAT']

stations = {
            1: ['Arughat','ARUGHAT'],
            2: ['Betrawoti','BETRAWOTI'],
            3: ['Bimalnagar','BIMALNAGAR'],
            4: ['Devghat','DEVGHAT'],
            5: ['Jomsom','JOMSOM'],
            7: ['Kumalgaun','KUMALGAUN'],
            8: ['Rajaiya','RAJAIYA'],
            9: ['Setidamauli','SETIDAMAULI'],
            10: ['Sisaghat','SISAGHAT'],
            22: ['Kalikhola', 'KALIKHOLA']
          }

for key in stations:
  get_flow_combine_and_stage(stations[key][1], stations[key][0], key, dt_start, dt_end, start_date, end_date)

print("Writing flow and stage complete !!!")