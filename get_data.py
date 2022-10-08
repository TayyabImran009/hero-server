import schedule
from datetime import datetime
import time

def chk():
    print("Function starts")
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    time.sleep(2)

schedule.every().day.at("01:28").do(chk)
  
while True:
    schedule.run_pending()
