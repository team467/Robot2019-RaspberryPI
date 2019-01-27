#!/usr/bin/env python
# coding: utf-8

import threading
from networktables import NetworkTables
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
table = NetworkTables.getTable('camera')

var prev = 0

while True:
    if table.getNumber('camera', 0) == 1:
	    if prev != table.getNumber('camera', 0):
		    subprocess.run(["ln", "-sfn", "/dev/video1", "/home/vid"])
			prev = 1
		else: 
		    subprocess.run(["ln", "-sfn", "/dev/video0", "/home/vid"])
			prev = 0