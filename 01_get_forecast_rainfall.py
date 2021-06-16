#!/usr/bin/python
import os
import csv
import time
import urllib2
from datetime import date
from datetime import timedelta
#============================================================================================+
# FUNCTION TO CHECK WHETHER LINK URL AVAILABLE
#============================================================================================+
def link_exists(url):
  request = urllib2.Request(url)
  request.get_method = lambda : 'HEAD'
  try:
    response = urllib2.urlopen(request)
    return True
  except urllib2.HTTPError:
    return False 
#============================================================================================+

## dd/mm/yyyy format
tm = (time.strftime("%d/%m/%Y"))
tm = tm.split('/')
day = tm[0]
month_name = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
mn = month_name[int(tm[1])-1]
year = tm[2]
yr = year[-2:]
#============================================================================================+
# GET YESTERDAY DATE
#============================================================================================+
today = date.today()
temp_yest = today - timedelta(days=1)
temp_yest = temp_yest.strftime("%d/%m/%Y")
temp_y = temp_yest.split('/')
temp_day = temp_y[0]
temp_mn = month_name[int(temp_y[1])-1]
temp_yr = temp_y[2]
temp_year = temp_yr[-2:]
yesterday = temp_mn + temp_day + temp_year
#============================================================================================+
dt = yesterday
#============================================================================================+
# FOR MANUAL
#============================================================================================+
#dt = 'Jun2020'
#============================================================================================+
# CLEAN FORECAST TXT FILE
#============================================================================================+
cmd_clean = 'rm /home/rimesnp/ws-narayani-scripts-2021/Forecast_files/*.txt'
os.system(cmd_clean)
#============================================================================================+
# SUB BASIN LIST
#============================================================================================+
basin_name = ['W650','W740','W750','W760','W800','W810','W820','W840','W850',
              'W900','W910','W930','W940','W960','W970','W980','W990','W1000',
              'W1010','W1040','W1050','W1060','W1120','W1130','W1170','W1190',
              'W1210','W1230','W1270','W1290','W1320','W1330','W1370','W1380',
              'W1420','W1430','W1470','W1490','W1570','W1580','W1620','W1640',
              'W1670','W1680','W1770','W1780','W1820','W1830','W1870','W1880',
              'W1920','W1940','W1960','W1980','W2020','W2040']

for i in range(len(basin_name)) :
  filename = basin_name[i]+'_'+dt
  #data_link = 'http://www.rimes.int/services/10DAYSFCST/BASIN_DATA/NEPAL/NAR/'+dt+'/'+filename+'.txt'
  data_link = 'https://flood-npl.rimes.int/wrf_data_rimes/NAR/'+dt+'/'+filename+'.txt'
  link_url = link_exists(data_link)
  if link_url is True:
    cmd = 'wget '+data_link+' -P /home/rimesnp/ws-narayani-scripts-2021/Forecast_files/'
    os.system(cmd)
