import os
import csv
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# constants
STATIONS = {
            1: ['Arughat','ARUGHAT'],
            2: ['Betrawoti','BETRAWOTI'],
            3: ['Bimalnagar','BIMALNAGAR'],
            4: ['Devghat','DEVGHAT'],
            5: ['Jomsom','JOMSOM'],
            7: ['Kumalgaun','KUMALGAUN'],
            8: ['Rajaiya','RAJAIYA'],
            9: ['Setidamauli','SETIDAMAULI_430.5'],
            10: ['Sisaghat','SISAGHAT'],
            22: ['Kalikhola', 'KALIKHOLA']
          }

# config for connection to MYSQL database
def set_db_conn():
  # global DB_USER, DB_PWD, DB_HOST, DB_NAME, DB_PORT, DB_RAISE_WARNINGS
  DB_USER = os.environ['NPL_FLOOD_DB_USER']
  DB_PWD = os.environ['NPL_FLOOD_DB_PWD']
  DB_HOST = os.environ['NPL_FLOOD_DB_HOST']
  DB_NAME = os.environ['NPL_FLOOD_DB']
  DB_PORT = os.environ['NPL_FLOOD_DB_PORT']
  DB_RAISE_WARNINGS = True
  return DB_USER, DB_PWD, DB_HOST, DB_NAME, DB_PORT, DB_RAISE_WARNINGS

# Flow stage files location
file_path = os.path.normpath("/home/rimesnp/ws-narayani-scripts-2021/Flow_Stage_output_files/")

db_user, db_pwd, db_host, db_name, db_port, db_raise_warnings = set_db_conn()

# create mysql connection
conn = mysql.connector.connect(
            host = db_host,
            user = db_user,
            password = db_pwd,
            port = db_port,
            database = db_name
      )

entry_date = datetime.today().strftime("%Y-%m-%d")
rows_updated = 0
rows_inserted = 0

for key in STATIONS:
  file_name = STATIONS[key][0] + "_flow_combine_stage.csv"
  with open(os.path.join(file_path, file_name),'r') as csvfile:
    csvfileReader = csv.reader(csvfile,delimiter=',')
    # Skip header of the CSV file.
    next(csvfileReader)

    for row in csvfileReader:
      fcst_date = row[0]
      station_name = row[1]
      station_id = row[2]
      discharge = row[3]
      water_level = row[4]

      # print(fcst_date, station_name, station_id, discharge, water_level)

      try:
        if conn.is_connected():
          cursor = conn.cursor()
          cursor.execute("""SELECT * FROM simulated_discharge_wl_hec_hms 
                            WHERE fcst_date = %s 
                            AND station_id = %s""",(fcst_date, station_id))
          rows = cursor.fetchall()
          num_rows = len(rows)
          if num_rows > 0:
            cursor.execute("""UPDATE 
                                simulated_discharge_wl_hec_hms 
                              SET 
                                discharge = %s, 
                                water_level= %s, 
                                entry_date = %s 
                              WHERE 
                                station_id = %s AND 
                                fcst_date = %s""",(discharge, water_level, entry_date, station_id, fcst_date))
            rows_updated += 1
          else:
            cursor.execute("""INSERT INTO simulated_discharge_wl_hec_hms 
                                (station_id,fcst_date,discharge,water_level,entry_date) 
                                VALUES (%s,%s,%s,%s,%s)""",(station_id, fcst_date, discharge, water_level, entry_date))
            rows_inserted += 1

          conn.commit() 
      except Error as e:
        print(e)
      finally:
        cursor.close()
        conn.close()

print("-------------------------------------")
print("Number of rows inserted: {}".format(rows_inserted))
print("Number of rows updated: {}".format(rows_updated))
print("-------------------------------------")
