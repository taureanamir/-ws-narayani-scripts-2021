from hec.script import *
from hec.heclib.dss import *
from hec.heclib.util import *
from hec.io import *
from os import *
import time
import java
import urllib2
from datetime import date
from datetime import timedelta
#===========================================================================================+
#===========================================================================================+
#===========================================================================================+
#===========================================================================================+
# FUNCTION TO WRITE FORECAST DATA TO DSS INPUT FILE 
#===========================================================================================+
def writetodss(location,forecast_d1,forecast_d2,forecast_d3,hec_dt):
  try:
    try:
      dssfile = HecDss.open("/home/rimesnp/ws/Narayani_model_2020/model/Narayani4_TimeSeries.dss")
      tsc = TimeSeriesContainer()
      tsc.fullName = "/NARAYANI/"+location+"/PRECIP-INC//1DAY/OBS/"
      start = HecTime(hec_dt,"0930")
      precip = [forecast_d1,forecast_d2,forecast_d3]
      times = []
      for value in precip:
        times.append(start.value())
        start.add(tsc.interval)
      tsc.times = times
      tsc.values = precip
      tsc.numberValues = len(precip)
      tsc.units = "MM"
      tsc.type = "PER-CUM"
      dssfile.put(tsc)
    except Exception, e:
      MessageBox.showError(' '.join(e.args), "Python Error")
    except java.lang.Exception, e :
      MessageBox.showError(e.getMessage(), "Error")
  finally :
    dssfile.close()
#==============================================================================================+
## dd/mm/yyyy format
tm = (time.strftime("%d/%m/%Y"))
tm = tm.split('/')
#print tm[0] + tm[1] + tm[2]
day = tm[0]
month_name = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
mn = month_name[int(tm[1])-1]
year = tm[2]
yr = year[-2:]
# GET YESTERDAY DATE BUT FORECAST TODAY, TOMORROW AND DAY AFTER
today = date.today()
temp_yest = today - timedelta(days=1)
temp_yest = temp_yest.strftime("%d/%m/%Y")
temp_y = temp_yest.split('/')
temp_day = temp_y[0]
temp_mn = month_name[int(temp_y[1])-1]
temp_yr = temp_y[2]
temp_year = temp_yr[-2:]
yesterday = temp_mn + temp_day + temp_year
#=============================================================================================+
# THIS DATE IS FOR WGET FILE EXAMPLE Jun1516
#=============================================================================================+ 
dt = yesterday
#=============================================================================================+
# DATE IF MANUAL
#=============================================================================================+
#dt = 'Jun2020'
#=============================================================================================+
# THIS DATE IS FOR HECTIME INPUT TO DSS FILE EXAMPLE 15Jun2016 
#=============================================================================================+ 
hec_dt = day+mn+year
#=============================================================================================+
# HEC DATE MANUAL
#=============================================================================================+
#hec_dt = '21Jun2020'
#=============================================================================================+
# SUB BASIN LIST
#=============================================================================================+
basin_name = ['W650','W740','W750','W760','W800','W810','W820','W840',
              'W850','W900','W910','W930','W940','W960','W970','W980',
              'W990','W1000','W1010','W1040','W1050','W1060','W1120',
              'W1130','W1170','W1190','W1210','W1230','W1270','W1290',
              'W1320','W1330','W1370','W1380','W1420','W1430','W1470',
              'W1490','W1570','W1580','W1620','W1640','W1670','W1680',
              'W1770','W1780','W1820','W1830','W1870','W1880','W1920',
              'W1940','W1960','W1980','W2020','W2040']

for i in range(len(basin_name)) :
  filename = basin_name[i]+'_'+dt
  # READ FILE
  file_path = '/home/rimesnp/ws-narayani-scripts-2021/rainfall_bias_correction/'+basin_name[i]+'/'+basin_name[i]+'Corrected_forecast.csv'
  rownum = 0
  file = open(file_path,'r')
  for row in file:
    if rownum == 0:
      fc_day1 = float(row.strip())
      rownum = rownum + 1
    elif rownum == 1:
      fc_day2 = float(row.strip())
      rownum = rownum + 1
    elif rownum == 2:
      fc_day3 = float(row.strip())
      rownum = rownum + 1
    #END OF FOR LOOP line
  #CALL FUNCTION TO WRITE DATA IN TIME SERIES FILE
  writetodss(basin_name[i],fc_day1,fc_day2,fc_day3,hec_dt)
  #END OF FOR LOOP i  
  file.close()
# END OF PROGRAM 
