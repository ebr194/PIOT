import json
import notifyDevice as nD
from databaseManipulator import Database

#Checks temp and humidity with the appropriate json data, pushes a notification only if a notification hasn't been sent that day
def checkData(temp, hum):
        with open('config.json', 'r') as f:
                data = json.load(f)

        if(Database().currentDay() == False):
                Database().logNotData()
                if temp < data['min_temperature']:
                        nD.send_notification_via_pushbullet('temp error', 'temperature below configuration')
                elif temp > data['max_temperature']:
                        nD.send_notification_via_pushbullet('temp error', 'temperature above configuration')
                elif hum < data['min_humidity']:
                        nD.send_notification_via_pushbullet('humidity error', 'humidity below configuration')
                elif hum > data['max_humidity']:
                        nD.send_notification_via_pushbullet('humidity error', 'humidity below configuration')
        
