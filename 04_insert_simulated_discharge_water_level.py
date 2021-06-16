#!/usr/bin/python
import os
import csv
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import ConfigParser

# constants
STATIONS = {
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

# config for connection to MYSQL database
def set_db_conn():
  # global DB_USER, DB_PWD, DB_HOST, DB_NAME, DB_PORT, DB_RAISE_WARNINGS
  config = ConfigParser.ConfigParser()
  config.read("config")
  DB_USER = config.get('DATABASE_CONFIG', 'NPL_FLOOD_DB_USER')
  DB_PWD =  config.get('DATABASE_CONFIG', 'NPL_FLOOD_DB_PWD')
  DB_HOST = config.get('DATABASE_CONFIG', 'NPL_FLOOD_DB_HOST')
  DB_NAME = config.get('DATABASE_CONFIG', 'NPL_FLOOD_DB')
  DB_PORT = config.get('DATABASE_CONFIG', 'NPL_FLOOD_DB_PORT')
  DB_RAISE_WARNINGS = True

  # create mysql connection
  conn = mysql.connector.connect(
              host = DB_HOST,
              user = DB_USER,
              password = DB_PWD,
              port = DB_PORT,
              database = DB_NAME
        )
  return conn

def insert_update_discharge_water_level(fcst_date, station_id, discharge, water_level, conn, cursor):
  inserted = 0
  updated = 0
  try:
    if conn.is_connected():
      cursor.execute("""SELECT * FROM simulated_discharge_wl_hec_hms 
                        WHERE fcst_date = %s 
                        AND station_id = %s""",(fcst_date, station_id))
      rows = cursor.fetchall()
      num_rows = len(rows)
      # print("num_rows: {}".format(num_rows))
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
        updated = 1
      else:
        cursor.execute("""INSERT INTO simulated_discharge_wl_hec_hms 
                            (station_id,fcst_date,discharge,water_level,entry_date) 
                            VALUES (%s,%s,%s,%s,%s)""",(station_id, fcst_date, discharge, water_level, entry_date))
        inserted = 1

      conn.commit() 
  except Error as e:
    print(e)
    # cursor.close()
    # conn.close()
  finally:
    # cursor.close()
    # conn.close()
    pass

  return inserted, updated

# Flow stage files location
file_path = os.path.normpath("/home/rimesnp/ws-narayani-scripts-2021/Flow_Stage_output_files/")

conn = set_db_conn()
cursor = conn.cursor()

entry_date = datetime.today().strftime("%Y-%m-%d")
rows_updated = 0
rows_inserted = 0

for key in STATIONS:
  file_name = STATIONS[key][0] + "_flow_combine_stage.csv"
  # print("Filename: {}".format(os.path.join(file_path, file_name)))
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
      insert_cnt, update_cnt = insert_update_discharge_water_level(fcst_date, station_id, discharge, water_level, conn, cursor)
      rows_inserted += insert_cnt
      rows_updated += update_cnt

cursor.close()
conn.close()

print("-------------------------------------")
print("Number of rows inserted: {}".format(rows_inserted))
print("Number of rows updated: {}".format(rows_updated))
print("-------------------------------------")
