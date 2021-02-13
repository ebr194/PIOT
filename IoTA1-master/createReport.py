import csv
import sqlite3
import dataGenerator as dG

DB_NAME = 'sensehat.db'

#selects all of the data from the report table and then writes it to a csv file
def csvWrite():
    with  sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM csvReport_data')

    with open('report.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Status: Min Temperature, Max Temperature, Min Humidity, Max Humidity'])
        writer.writerows(cursor)
    cursor.close()
    connection.close()

def main():
    dG.createReportDB()
    dG.csvChecker()
    csvWrite()
    
if __name__ == '__main__':
    main()