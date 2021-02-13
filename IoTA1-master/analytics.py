import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
import seaborn as sns
import pandas as pd

DB_NAME = "sensehat.db"
#reference: 
        # https://pythonprogramming.net/graphing-from-sqlite-database/
        #https://stackoverflow.com/questions/25328003/how-can-i-change-the-font-size-using-seaborn-facetgrid
        #https://stackoverflow.com/questions/31594549/how-do-i-change-the-figure-size-for-a-seaborn-plot
        #https://www.datacamp.com/community/tutorials/seaborn-python-tutorial
#also used my practical data science notes 
def matplotGraph():
    with  sqlite3.connect(DB_NAME) as connection:
        c = connection.cursor()
        c.execute('SELECT timestamp, AVG(temperature) as temp FROM sensehat_data group by timestamp')
        data = c.fetchall()

        date = []
        temp = []

        for row in data:
                date.append(parser.parse(row[0]))
                temp.append(row[1])

                style.use('fivethirtyeight')
                plt.plot_date(date,temp,'-')
                plt.savefig('figure1.png', dpi=400)
        
        c.close()
        plt.close()

def seabornGraph():
        connection = sqlite3.connect('sensehat.db')
        data = pd.read_sql_query('SELECT date(timestamp) as date, AVG(humidity) as humidity FROM sensehat_data group by timestamp', connection)

        sns.set(rc={'figure.figsize':(30,30)})
        sns.set(font_scale=0.5)
        sns.factorplot(x='date', y='humidity', data=data, kind='bar')
        plt.savefig('figure2.png', dpi=400)

        plt.close()
        connection.close()





def main():
        matplotGraph()
        seabornGraph()




if __name__ == '__main__':
    main()
