import threading
from networktables import NetworkTables
import time
import subprocess

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
prev = table.getNumber('epochTS', 0)

while True:
	x = table.getNumber('epochTS', 0)
	if x != 0 and x != prev:
		subprocess.call(["sudo", "date", "-s", "@" + str(int(x))])
		prev = table.getNumber('epochTS', 0)
	time.sleep(1)