# this script demonstate how to run things automatically at specified time

import schedule
import time

def job(self):
	print('I am working...')

def print_time(self):
	print('time')

schedule.every(1).minutes.do(job)
schedule.every().day.at("14:40").do(print_time)

while 1:
	schedule.run_pending()
	time.sleep(5)
