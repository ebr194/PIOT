import subprocess as sp
import os
import time
import sqlite3
import bluetooth
import time
import notifyDevice as nD

DB_NAME = 'sensehat.db'

#Located and nearby devices both tutorial code that i've modified, not quite sure if i've done the task completely right but this is what the 
#task sounds like on the discussion board.
#So it locates a certain device from the already paired list (my device) and then compares them with the discover list
#if the device is there a notification is sent
#databases are there to make sure only 1 device is sent
class blueTooth:
    def __init__(self):
        pass

    def locatedDevice(self):
        p = sp.Popen(["bt-device", "--list"], stdin = sp.PIPE, stdout = sp.PIPE, close_fds = True)
        (stdout, stdin) = (p.stdout, p.stdin)
        data = stdout.readlines()
        pairedDevice = data[1]
        pDev = pairedDevice.decode()
        ppDev = pDev[8:-2]
        return ppDev

    def nearbyDevices(self, device):
        nearbyDevices = bluetooth.discover_devices()

        for macAddress in nearbyDevices:
            if(macAddress == device):
                if(blueTooth().deviceSent() == False):
                    blueTooth().insertDeviceDB(macAddress)
                    nD.send_notification_via_pushbullet('Device Paired', macAddress)

    def createDeviceDB(self):
        with  sqlite3.connect(DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS device_data(device VARCHAR)')
        cursor.close()
        connection.close()
    
    def insertDeviceDB(self, name):
        with  sqlite3.connect(DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO device_data (device) VALUES (?)',(name,))
        cursor.close()
        connection.close()

    def deviceSent(self):
        with sqlite3.connect(DB_NAME) as connection:
            cursor = connection.cursor()
            row = cursor.execute('SELECT COUNT(*) from device_data where device = DEVICE').fetchone()
        cursor.close()
        connection.close()

        return row[0] >= 1



def main():
    while True:
        blueTooth().createDeviceDB()
        device = blueTooth().locatedDevice()
        blueTooth().nearbyDevices(device)
        blueTooth().insertDeviceDB(device)
        time.sleep(60)


if __name__ == '__main__':
    main()