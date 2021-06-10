#!/usr/bin/python
#==================================================================================================+
import time
import os
from datetime import date
from datetime import timedelta
#==================================================================================================+
# CURRENT DATE
today = date.today()
#print today.strftime("%-d %B %Y")
current_date = today.strftime("%-d %B %Y")
# DAY AFTER TOMORROW DATE
day_after_tomorrow = today + timedelta(days=4)
day_after_tomorrow = day_after_tomorrow.strftime("%-d %B %Y")
#print day_after_tomorrow 
current_time = time.strftime("%I:%M:%S")
# FILE PATH CONTROL FILE OF NARAYANI MODEL
file_path = '/home/rimesnp/ws/Narayani_model_2021/model/2017_2021.control'

control_str = "Control: 2017-2021\n" + \
              "     Last Modified Date: " + current_date +"\n" + \
              "     Last Modified Time: " + current_time +"\n" + \
              "     Version: 4.2.1\n" + \
              "     Time Zone ID: Asia/Bangkok\n" + \
              "     Time Zone GMT Offset: 25200000\n" + \
              "     Start Date: 1 January 2017\n" + \
              "     Start Time: 08:00\n" + \
              "     End Date: " + day_after_tomorrow +"\n" + \
              "     End Time: 08:00\n" + \
              "     Time Interval: 1440\n" + \
              "     Grid Write Interval: 1440\n" + \
              "     Grid Write Time Shift: 0\n" + \
              "End:\n"

fo = open(file_path,"wb")
fo.write(control_str)
fo.close()
#==================================================================================================+
