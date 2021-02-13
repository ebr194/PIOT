import sqlite3
import time

DB_NAME = "sensehat.db"

#Database class for monitorAndNotify, creates the appropriate tables
#inserts the data and the database also works with working out if the notification
#has been sent that
class Database:
    def __init__(self):
        pass

    #Database Creators
    def createSenseDB(self):
        with  sqlite3.connect(DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS sensehat_data(timestamp DATETIME, temperature NUMERIC, humidity NUMERIC)")
        cursor.close()
        connection.close()

    def createNotificationDB(self):
        with  sqlite3.connect(DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS notification_data(date DATETIME)")
        cursor.close()
        connection.close()
            
    #Insert Time, Temp & Humidity into Database from SenseHat
    def insertData(self, temp, hum):
        with  sqlite3.connect(DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO sensehat_data (timestamp, temperature, humidity) VALUES (DATETIME('now', 'localtime'), ?, ?)",
            (temp,hum))
        cursor.close()
        connection.close()

    #For notifications to be sent once a day - matthew helped with this. This is his code
    def currentDay(self):
        with  sqlite3.connect(DB_NAME) as connection:
            cursor = connection.cursor()
            row = cursor.execute("SELECT COUNT(*) FROM notification_data WHERE date = DATE(DATETIME('now', 'localtime'))").fetchone()
        cursor.close()
        connection.close()

        return row[0] >= 1

    def logNotData(self):
        with sqlite3.connect(DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO notification_data VALUES (DATE(DATETIME('now', 'localtime')))")
        cursor.close()
        connection.close()