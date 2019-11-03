import threading
from networktables import NetworkTables
import calendar
import time

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.4.67.23')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

# Insert your processing code here
print("Connected!")

table = NetworkTables.getTable('time')

while True:
	table.putNumber('epochTS', calendar.timegm(time.gmtime()))
	time.sleep(1)