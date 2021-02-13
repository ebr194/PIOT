from sense_hat import SenseHat
from databaseManipulator import Database
import dataChecker as dC

class Range:
        def __init__(self):
                pass
        
        def getSenseData(self):
                sense = SenseHat()
                temp = sense.get_temperature()
                hum = sense.get_humidity()

                if temp and hum is not None:
                        temp = round(temp, 1)
                        hum = round(hum, 1)
                        Database().insertData(temp,hum)
                        dC.checkData(temp,hum)