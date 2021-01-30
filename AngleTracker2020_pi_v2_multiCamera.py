# This version of AngleTracker2020 is supposed to be used on the raspberry pi
# This is probably the final version we will use
# It is able to support both cameras

import cv2
from networktables import NetworkTables
import threading
from reduced_pipeline_hsl_rgb_convex_hull import RetroReflectiveTapeDetector
from math import *
import sys
from numpy import *

def extra_processing(capNum, pipeline3, frame):
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
    horizontalDistance = 0
 
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
        if bounding_rect_aspect_ratio >= 1.7 and bounding_rect_aspect_ratio < 3.35:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
            cv2.line(frame, (x,y), (x,y), (0,255,0), 10)
            # cv2.imshow("frame", frame)

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
            if capNum == 1:
                distanceFromTarget = 20170/h
            if capNum == 2:
                distanceFromTarget = 16000/h

            # convert distance from target from inches to ft and inches
            feet = distanceFromTarget/12
            inches = distanceFromTarget%12

            # haveDistance = True

            # finding turning angle in radians
            angleRad = atan(distanceFromCenterFrameInches/distanceFromTarget)

            # calculating turning angle in degrees
            if (frameCenterX < boundingCenterX):
                angleDeg = degrees(angleRad) # if center of bounding box is to the right of the center of the frame, negative angle
            elif (frameCenterX > boundingCenterX):
                angleDeg = degrees(angleRad)*(-1) # if center of bounding box is to the left of the center of the frame, positive angle
            

            # haveAngle = True

            """
            This is used to try and remove bounding boxes that aren't correct
            The miscellaneous boxes are usually are pretty off, and the driver should line us up pretty well
            Lol, this might not actually be a good idea because the two cameras will have different angles
            """
            """
            if (angleDeg > 30 or angleDeg < -30):
              haveAngle = False
              haveDistance = False
              print("the angle is greater than 30 degrees")
            
            else:
                haveAngle = True
                haveDistance = True
            """

            # A distance filter
            if (distanceFromTarget <= 480) and (distanceFromTarget >= 100) and (y >= 5) and ((y+h) <= 715):
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
                    cv2.line(frame, (x,y), (x,y), (0,255,0), 10)
                    # cv2.imshow("frame", frame)

                    # print("height: {}, width: {}, x: {}, y: {}".format(h, w, x, y,))
                    haveDistance = True
                    haveAngle = True
                    break
            else:
                haveDistance = False
                haveAngle = False

            
            # print("height: {}, width: {}, area: {}, distance: {}, x: {}, y: {}, angle: {}".format(h, w, (h*w), distanceFromTarget, x, y, angleDeg))

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
    horizontalDistance = 0

    haveAngle2 = False
    haveDistance2 = False
    distanceFromTarget2 = 0
    turningAngle2 = 0

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

    cap = None
    cap2 = None
    have_frame = False
    have_frame2 = False
    
    # Two cameras
    while (cap == None) and (cap2 == None):
        try:
            # print("cap")
            cap = cv2.VideoCapture(0)
        except:
            cap = None
            # print("trying")

        try:
            # print("cap2")
            cap2 = cv2.VideoCapture(2)
        except:
            cap2 = None
            # print("trying2")

        try:
            if cap.isOpened() == False:
                cap = None
        except:
            cap = None
        try:
            if cap2.isOpened() == False:
                cap2 = None
        except:
            cap2 = None
        
        

        # print(cap == None)
        # print(cap2 == None)
        # print(cap)
        # print(cap2)
        # print((cap == None) and (cap2 == None))


    # print("found a camera")
    # set resolution of video feed to 1280x720
    if cap != None:
        change_res(cap, 1280, 720)
    if cap2 != None:
        change_res(cap2, 1280, 720)

    frame_count = 0

    # Make sure to change values if we are using a third camera
    while True:
        try:
            have_frame, frame = cap.read()
        except BaseException:
            # print("no have_frame")
            pass
        try:
            have_frame2, frame2 = cap2.read()
        except BaseException:
            # print("no have_frame2")
            pass
        #have_frame3, frame3, cap3.read()
        if (have_frame or have_frame2):

            # process returned frame from video feed and return angle, distance, if angle is found, if distance is found
            if have_frame:
                pipeline3.process(frame)
                haveAngle, haveDistance, turningAngle, distanceFromTarget = extra_processing(1, pipeline3, frame)
            if have_frame2:
                pipeline3.process(frame2)
                haveAngle2, haveDistance2, turningAngle2, distanceFromTarget2 = extra_processing(2, pipeline3, frame2)

            # put values to network tables
            
            # Camera 1
            table.putBoolean("haveAngle", haveAngle)
            table.putBoolean("haveDistance", haveDistance)
            
            # Camera 2
            table.putBoolean("haveAngle2", haveAngle2)
            table.putBoolean("haveDistance2", haveDistance2)

            # print("haveDistance: {}, haveAngle: {}".format(haveDistance, haveAngle))
            # print("haveDistance2: {}, haveAngle2: {}".format(haveDistance2, haveAngle2))
            # print("distanceFromTarget: {}, distanceFromTarget2: {}".format(distanceFromTarget, distanceFromTarget2))

            if haveDistance and haveDistance2:
                finalDistanceFromTarget = (distanceFromTarget + distanceFromTarget2)/2
                table.putNumber("DistanceFromTarget", finalDistanceFromTarget)
                # print("DistanceFromTarget: {}".format(finalDistanceFromTarget))
            elif haveDistance:
                table.putNumber("DistanceFromTarget", distanceFromTarget)
                # print("DistanceFromTarget: {}, HorizontalDistance: {}".format(distanceFromTarget, horizontalDistance))
            elif haveDistance2:
                table.putNumber("DistanceFromTarget", distanceFromTarget2)
                # print("DistanceFromTarget: {}".format(distanceFromTarget2))

            if haveAngle and haveAngle2:
                finalTurningAngle = (turningAngle + turningAngle2)/2
                table.putNumber("Average TurningAngle:", finalTurningAngle)
                # print("TurningAngle: {}".format(finalTurningAngle))
            elif haveAngle:
                table.putNumber("TurningAngle", turningAngle)
                # print("TurningAngle: {}".format(turningAngle))
            elif haveAngle2:   
                table.putNumber("TurningAngle", turningAngle2)
                # print("TurningAngle: {}".format(turningAngle2))

            # if have_frame:
            #     cv2.imwrite("/home/pi/Vision2020/frames/frame1.jpg", frame)
            # if have_frame2:
            #     cv2.imwrite("/home/pi/Vision2020/frames/frame2.jpg", frame2)

            frame_count += 1

            # hit q to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


if __name__ == "__main__":
    main()