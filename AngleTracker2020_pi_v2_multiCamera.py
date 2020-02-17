# This version of AngleTracker2020 is supposed to be used on the raspberry pi

import cv2
from networktables import NetworkTables
import threading
from reduced_pipeline_hsl_rgb_convex_hull import RetroReflectiveTapeDetector
from math import *
import sys
from numpy import *

def extra_processing(pipeline3, frame):
    """
    Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
    :param pipeline: the pipeline that just processed an image
    :return: None
    """
    center_x_positions = []
    center_y_positions = []
    widths = []
    heights = []
    topLeftX = []
    topLeftY = []
    x = 0
    y = 0
    w = 0
    h = 0
    lx = 0
    ly = 0
    lw = 0
    lh = 0

    haveAngle = False
    haveDistance = False
    angleDeg = 0
    distanceFromTarget = 0
 
    # Find the bounding boxes of the contours to get x, y, width, and height and calculate distance and angle
    for contour in pipeline3.filter_contours_output:

        # get x, y, width, and height of contour by finding bounding rect using opencv
        x, y, w, h = cv2.boundingRect(contour)

        # X and Y are coordinates of the top-left corner of the bounding box
        center_x_positions.append(x + w / 2)  
        center_y_positions.append(y + h / 2)
        
        topLeftX.append(x)
        topLeftY.append(y)
        widths.append(w)
        heights.append(h)

        # only draw bounding box and do calculations if ratio of w to h of box is between 2.0 and 2.5 inclusive
        bounding_rect_aspect_ratio = w/h
        # If perfect, the bounding box ratio is around 2.31
        if bounding_rect_aspect_ratio >= 1.7 and bounding_rect_aspect_ratio < 2.6:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
            cv2.line(frame, (x,y), (x,y), (0,255,0), 10)
            cv2.imshow("frame", frame)

            # print("height: {}, width: {}".format(h, w))

            # find center point of bounding box
            boundingCenterX = (x + (w/2))

            frameCenterX = 540

            # Initializing variable for the distance between the center of the frame and center of bounding box in inches, used to calculate angle
            distanceFromCenterFrameInches = 0

            """
            When frameCenterX < boundingCenterX, the target is to the right of us.
            When frameCenterX > boundingCenterX, the target is to the left of us.
            """                 

            # find the distance in inches that the center of frame is from the the center of the bounding box
            if (frameCenterX < boundingCenterX):
                distanceFromCenterFrameInches = (boundingCenterX - frameCenterX) * (39.25/w)
            elif (frameCenterX > boundingCenterX):
                distanceFromCenterFrameInches = (frameCenterX - boundingCenterX) * (39.25/w)

            # calculate distance of camera from target in inches
            distanceFromTarget = 20170/h

            haveDistance = True

            # convert distance from target from inches to ft and inches
            feet = distanceFromTarget/12
            inches = distanceFromTarget%12

            # finding turning angle in radians
            angleRad = atan(distanceFromCenterFrameInches/distanceFromTarget)

            # calculating turning angle in degrees
            if (frameCenterX < boundingCenterX):
                angleDeg = degrees(angleRad) # if center of bounding box is to the right of the center of the frame, negative angle
            elif (frameCenterX > boundingCenterX):
                angleDeg = degrees(angleRad)*(-1) # if center of bounding box is to the left of the center of the frame, positive angle
            

            haveAngle = True

            # This is used to try and remove bounding boxes that aren't correct
            # The miscellaneous boxes are usually are pretty off, and the driver should line us up pretty well
            if (angleDeg > 30 or angleDeg < -30):
              haveAngle = False
              print("the angle is greater than 30 degrees")
            
            else:
                haveAngle = True

            # if (distanceFromTarget <= 350) and (distanceFromTarget >= 100):
            #         cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
            #         cv2.line(frame, (x,y), (x,y), (0,255,0), 10)
            #         cv2.imshow("frame", frame)

            #         print("height: {}, width: {}".format(h, w))
            #         haveDistance = True
            #         haveAngle = True
            # else:
            #     haveDistance = False
            #     haveAngle = False

            if (haveAngle == True) and (haveDistance == True):
                print("height: {}, width: {}, area: {}, distance: {}, x: {}, y: {}, angle: {}".format(h, w, (h*w), distanceFromTarget, x, y, angleDeg))

        elif (distanceFromTarget == 0) or (angleDeg == 0): # if distance or angle is 0, program does not have an angle or distance
            haveAngle = False
            haveDistance = False

        
        
    return haveAngle, haveDistance, angleDeg, distanceFromTarget



def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


def main():

    haveAngle = False
    haveDistance = False
    distanceFromTarget = 0
    turningAngle = 0

    cond = threading.Condition()
    notified = [False]

    def connectionListener(connected, info):
        with cond:
            notified[0] = True
            cond.notify()


    # Initializing and connecting to network tables
    NetworkTables.initialize(server='10.4.67.2')
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    # wait till network tables are found
    with cond:
        if not notified[0]:
            cond.wait()

    table = NetworkTables.getTable('vision')
   
    pipeline3 = RetroReflectiveTapeDetector()
    
    # Two cameras
    cap = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(2)

    # set resolution of video feed to 1280x720
    change_res(cap, 1280, 720)

    frame_count = 0

    # Make sure to change values if we are using a third camera
    while True:
        have_frame, frame = cap.read()
        have_frame2, frame2 = cap2.read()
        have_frame3, frame3, cap3.read()
        if have_frame:

            # process returned frame from video feed and return angle, distance, if angle is found, if distance is found
            pipeline3.process(frame)
            pipeline3.process(frame2)

            haveAngle, haveDistance, turningAngle, distanceFromTarget = extra_processing(pipeline3, frame)
            haveAngle2, haveDistance2, turningAngle2, distanceFromTarget2 = extra_processing(pipeline3, frame2)

            # put values to network tables
            
            # Camera 1
            table.putBoolean("haveAngle", haveAngle)
            table.putBoolean("haveDistance", haveDistance)
            
            # Camera 2
            table.putBoolean("haveAngle2", haveAngle2)
            table.putBoolean("haveDistance2", haveDistance2)


            if haveDistance and haveDistance2:
                FinaldistanceFromTarget = (distanceFromTarget + distanceFromTarget2)/2
                table.putNumber("DistanceFromTarget Camera 1:" + distanceFromTarget) # Knowing which values correspond to which camera is useful for debugging
                table.putNumber("DistanceFromTarget Camera 2:" + distanceFromTarget2)
                table.putNumber("Average DistanceFromTarget:", FinaldistanceFromTarget)
            elif haveDistance:
                table.putNumber("DistanceFromTarget Camera 1:", distanceFromTarget)
                table.putNumber("DistanceFromTarget Camera 2:", distanceFromTarget2)
            elif haveDistance2:
                table.putNumber("DistanceFromTarget Camera 1:", distanceFromTarget)
                table.putNumber("DistanceFromTarget Camera 2:", distanceFromTarget2)

            if haveAngle and haveAngle2:
                FinalturningAngle = (turningAngle + turningAngle2)/2
                table.putNumber("TurningAngle Camera 1:" + turningAngle)
                table.putNumber("TurningAngle Camera 2:" + turningAngle2)
                table.putNumber("Average TurningAngle:", FinalturningAngle)
            elif haveAngle:
                table.putNumber("TurningAngle Camera 1:" + turningAngle)
                table.putNumber("TurningAngle Camera 2:" + turningAngle2)

            elif haveAngle2:        
                table.putNumber("TurningAngle Camera 1:" + turningAngle)
                table.putNumber("TurningAngle Camera 2:" + turningAngle2)

            frame_count += 1

            # hit q to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


if __name__ == "__main__":
    main()