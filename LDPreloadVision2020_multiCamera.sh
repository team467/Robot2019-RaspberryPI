#!/bin/bash

v4l2-ctl -c brightness=60
v4l2-ctl -c exposure_auto=1
v4l2-ctl -c exposure_absolute=5

v4l2-ctl -d 2 -c brightness=60
v4l2-ctl -d 2 -c exposure_auto=1
v4l2-ctl -d 2 -c exposure_absolute=5

sudo -u pi LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0 python3 /home/pi/Vision2020/AngleTracker2020_pi_v2_multiCamera.py