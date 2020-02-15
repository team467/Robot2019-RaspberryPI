from AngleTracker2020_pi_v2_Draft import haveAngle1, haveDistance1, turningAngle1, distanceFromTarget1
from AngleTracker2020_pi_v2_camera2 import haveAngle2, haveDistance2, turningAngle2, distanceFromTarget2
from AngleTracker2020_pi_v2_camera3 import haveAngle3, haveDistance3, turningAngle3, distanceFromTarget3
import cv2
from networktables import NetworkTables
import threading
from math import *
from numpy import *



float average_distance = (distanceFromTarget1 + distanceFromTarget2 + distanceFromTarget3)/3

print (average_distance)

def main():
    table.putNumber("average distance", average_distance)


if __name__ == "__main__":
    main()
