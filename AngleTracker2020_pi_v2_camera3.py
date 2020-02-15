# This version of AngleTracker2020 is supposed to be used on the raspberry pi

import cv2
# from networktables import NetworkTables
import threading
# from grip_three_convexhull import TapeRecCodeThree
from reduced_pipeline_with_convex_hull import RetroReflectiveTapeDetector
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
    distanceFromTarget3 = 0
 
    # Find the bounding boxes of the contours to get x, y, width, and height
    

    for contour in pipeline3.filter_contours_output:

        x, y, w, h = cv2.boundingRect(contour)

        # X and Y are coordinates of the top-left corner of the bounding box
        center_x_positions.append(x + w / 2)  
        center_y_positions.append(y + h / 2)
        
        topLeftX.append(x)
        topLeftY.append(y)
        widths.append(w)
        heights.append(h)

        # if float(w/h) >= 2.0001:
        if float(w/h) <= 2.3:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
            cv2.line(frame, (x,y), (x,y), (0,255,0), 10)
            # cv2.imshow("frame",frame)
            
            # print height, width, x, and y positions of bounding box
            print("h = {}, w = {}, x = {}, y = {}, a = {}".format(h, w, x, y, (w*h))) # x and y represent the top left of the box

            # find center point of bounding box
            boundingCenterX = (x + (w/2))

            frameCenterX = 540

            # Initializing zero which is dead on
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

                
                
            # # print(distanceFromCenterFrameInches)

            # # distanceFromTarget3 = float((372*46.25)/h) 
            # # distanceFromTarget3 = float((434*41)/h)
            # # distanceFromTarget3 = float(((-50)/151)*h + 186.06623) (This is a function we came up with)
            
            # # I think this ratio might be better and find a better ratio
            # distanceFromTarget3 = float ((7200*(17/12))/h)

            # # distanceFromTarget3 = float((122*150)/h)
            # haveDistance = True

            distanceFromTarget3 = float((122*150)/h)
            haveDistance = True

            # we need to find a better ratio using more accurate tests

            # convert distance from target from inches to ft and inches
            feet = distanceFromTarget3/12
            inches = distanceFromTarget3%12

            print("Distance from frame center to box center: {}, Bounding box center: {}, Frame center: {}".format((boundingCenterX-frameCenterX), boundingCenterX, frameCenterX))

            print("Distance in inches: {}, Distance in feet and inches: {} feet, {} inches".format(int(distanceFromTarget3), int(feet), int(inches)))


            # finding turning angle in radians
            angleRad = atan(distanceFromCenterFrameInches/distanceFromTarget3)



            # calculating turning angle in degrees
            if (frameCenterX > boundingCenterX):
                angleDeg = degrees(angleRad) # if center of bounding box is to the right of the center of the frame, negative angle
            elif (frameCenterX < boundingCenterX):
                angleDeg = degrees(angleRad)*(-1) # if center of bounding box is to the left of the center of the frame, positive angle
            

            haveAngle = True

            print("Angle: {}".format(angleDeg))
        # else:
        #     haveAngle = False
        #     haveDistance = False
        
        
        return haveAngle, haveDistance, angleDeg, distanceFromTarget3, frame



def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


def main():

    haveAngle = False
    haveDistance = False
    distanceFromTarget3 = 0
    turningAngle = 0

    # cond = threading.Condition()
    # notified = [False]

    # def connectionListener(connected, info):
    #     with cond:
    #         notified[0] = True
    #         cond.notify()


    # Initializing and connecting to network tables
    # NetworkTables.initialize(server='10.4.67.23')
    # NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    # with cond:
    #     if not notified[0]:
    #         cond.wait()

    # table = NetworkTables.getTable('vision')
   
    # pipeline3 = TapeRecCodeThree()
    pipeline3 = RetroReflectiveTapeDetector()
    # cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap = cv2.VideoCapture(0)
    change_res(cap, 1280, 720)
    frame_count = 0
    while True:
        have_frame, frame = cap.read()
        if have_frame:

            frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            print(frame_width)
            print(frame_height)

            pipeline3.process(frame)
            haveAngle, haveDistance, turningAngle, distanceFromTarget3, frame = extra_processing(pipeline3, frame)

            # table.putBoolean("haveAngle", haveAngle)
            # table.putBoolean("haveDistance", haveDistance)
            # print("put to tables")

            # if haveAngle:
            #     table.putNumber("TurningAngle", turningAngle)
            # else:
            #     table.putNumber("TurningAngle", 0)
            # if haveDistance:
            #     table.putNumber("distanceFromTarget3", distanceFromTarget3)
            # else:
            #     table.putNumber("distanceFromTarget3", 0)

            # cv2.imwrite("/home/pi/Vision2020/frames/frame.jpg", frame)
            cv2.imwrite("C:\\Users\\theak\\Documents\\Akash\\Robotics\\Robot_Programs\\Competition\\Robot2019-RaspberryPI\\local_frame.png", frame)
            # cv2.imwrite("pi_frame.png", frame)
            # cv2.imshow("frame", frame)
            frame_count += 1

            print("Frame count: {}".format(frame_count))

            # hit q to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            elif frame_count == 50:
                break


if __name__ == "__main__":
    main()