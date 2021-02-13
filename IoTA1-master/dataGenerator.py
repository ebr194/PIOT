import sqlite3
import datetime
import json

DB_NAME = 'sensehat.db'

#Get Min / Max temp and humidity from sense table, sorts it by day
def getData():
    with  sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT timestamp, MIN(temperature) as mTemp, MAX(temperature) as MTemp, MIN(humidity) as mHum, MAX(humidity) as MHum FROM sensehat_data GROUP BY date(timestamp)')
        rows = cursor.fetchall()
        return rows

#creates the Report table
def createReportDB():
        with  sqlite3.connect(DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS csvReport_data(date VARCHAR, minTempStatus VARCHAR, maxTempStatus VARCHAR, minHumStatus VARCHAR, maxHumStatus VARCHAR)')
        cursor.close()
        connection.close()

#Checks the min and max and then inserts into the report table
def csvChecker():
    data = getData()
    for rows in data:
        time = datetime.datetime.strptime(rows[0], '%Y-%m-%d  %H:%M:%f').date()
        temporarymintemp = float(rows[1])
        tempmaxtemp = float(rows[2])
        tempminhum = float(rows[3])
        tempmaxhum = float(rows[4])
        
        minTemp = tempChecker(temporarymintemp)
        maxTemp = tempChecker(tempmaxtemp)
        minHum = humChecker(tempminhum)
        maxHum = humChecker(tempmaxhum)
        insertCSVData(time, minTemp, maxTemp, minHum, maxHum)

def insertCSVData(time, minTemp, maxTemp, minHum, maxHum):
    with  sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO csvReport_data (date, minTempStatus, maxTempStatus, minHumStatus, maxHumStatus) VALUES (?, ?, ?,?,?)',(time,minTemp,maxTemp,minHum,maxHum,))
    cursor.close()
    connection.close()

#check temp, return appropriate message
def tempChecker(temp):
        with open('config.json', 'r') as f:
                data = json.load(f)
        
        if temp < data['min_temperature']:
                Temp = data['min_temperature'] - temp
                Temp = round(Temp,1)
                return " BAD: {}°C Below Minimum Temperature. ".format(Temp)
        if temp > data['max_temperature']:
                Temp = temp - data['max_temperature']
                Temp = round(Temp,1)
                return ' BAD: {}°C Above Maximum Temperature. '.format(Temp) 
        else:
                return ' OK. '

#check humidity, return appropriate message
def humChecker(hum):
        with open('config.json', 'r') as f:
                data = json.load(f)
        if hum < data['min_humidity']:
                Hum = (data['min_humidity'] * hum) / 100
                Hum = round(Hum,0)
                return " BAD: {}% Below Minimum Humidity. ".format(Hum)
        if hum > data['max_humidity']:
                Hum = (hum/data['max_humidity']) / 100
                Hum = round(Hum,0)
                return ' BAD: {}% Above Maximum Humidity. '.format(Hum) 
        else:
                return ' OK. '           