#!/usr/bin/env python
# coding: utf-8

import threading
from networktables import NetworkTables
import subprocess
import sys

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

def camera_switcher(cameraNum): 
    switcher = { 
        0: ["ln", "-sfn", "/dev/video" + sys.argv[1], "/home/vid"], 
        1: ["ln", "-sfn", "/dev/video" + sys.argv[2], "/home/vid"], 
        2: ["ln", "-sfn", "/dev/video" + sys.argv[3], "/home/vid"], 
	3: ["ln", "-sfn", "/dev/video" + sys.argv[4], "/home/vid"]
    }
    return switcher.get(cameraNum, 0) 
  

prev = 0
subprocess.call(["ln", "-sfn", "/dev/video0", "/home/vid"])

while True:
    if int(table.getNumber('camera', 0)) != prev and 0 <= int(table.getNumber('camera', 0)) <= 3:
        subprocess.call(camera_switcher(int(table.getNumber('camera', 0))))
        prev = int(table.getNumber('camera', 0))
