'''
This code is for scheduling the code to run every hour
'''

from apscheduler.schedulers.blocking import BlockingScheduler
from SQLDB_Conn import SQL_Conn

def some_job():
    print("Decorated job")

scheduler = BlockingScheduler()
scheduler.add_job(SQL_Conn, 'interval', hours=1)
scheduler.start()