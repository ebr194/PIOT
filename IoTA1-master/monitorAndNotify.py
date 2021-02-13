#!/usr/bin/env python3
import sys
import time

from getSenseData import Range
from databaseManipulator import Database

#infinite loop to run always, with a sleep of 60 seconds 
def main():
        while True:
                Database().createSenseDB()
                Database().createNotificationDB()
                Range().getSenseData()
                time.sleep(60)



if __name__ == '__main__':
    main()