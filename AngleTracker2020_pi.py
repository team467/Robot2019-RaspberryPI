# This version of AngleTracker2020 is for use on the pi since it uses networktables

import cv2
from networktables import NetworkTables
import threading
#from grip_two import TapeRecCodeTwo
from grip_three_convexhull import TapeRecCodeThree
#from grip_wideangle import WideAngleGripFinal
from math import *
import sys

def extra_processing(cap, pipeline3, frame):
    """
    Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
    :param pipeline: the pipeline that just processed an image
    :return: None
    """
    print("Entered extra processing")
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

    distanceFromTarget = 0.0
 
    # Find the bounding boxes of the contours to get x, y, width, and height
    print(len(pipeline3.filter_contours_output))

    angleDeg = 0 
    distanceFromTarget = 0 
    haveAngle = False
    haveDistance = False




    for contour in pipeline3.filter_contours_output:

        x, y, w, h = cv2.boundingRect(contour)

        # cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)

        center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
        center_y_positions.append(y + h / 2)
        
        topLeftX.append(x)
        topLeftY.append(y)
        widths.append(w)
        heights.append(h)

        if float(w/h) >= 2.0:
            if float(w/h) <= 2.3:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
                cv2.line(frame, (x,y), (x,y), (0,255,0), 10)
                cv2.imshow("frame", frame) 
                print("h = {}, w = {}, x = {}, y = {}, a = {}".format(h, w, x, y, (w*h)))

                #boundingCenterX = ((x+x+w)/2)
                
                boundingCenterX = (x-w/2)
                frameCenterX = cap.get(int((cv2.CAP_PROP_FRAME_WIDTH)/2))

                # Initializing zero which is dead on
                distanceFromCenterFrameInches = 0

                # These account for when we are to the left or to the right of the target
                if (frameCenterX < boundingCenterX):
                   distanceFromCenterFrameInches = (boundingCenterX - frameCenterX) * (39.25/w)
                elif (frameCenterX > boundingCenterX):
                    distanceFromCenterFrameInches = (frameCenterX - boundingCenterX) * (39.25/w)

                
                distanceFromTarget = float((122*150)/h)
                haveDistance = True
         
                feet = distanceFromTarget/12
                inches = distanceFromTarget%12

                print("Distance in inches: {}, Distance in feet and inches: {} feet, {} inches".format(int(distanceFromTarget), int(feet), int(inches)))

                angleRad = atan(distanceFromCenterFrameInches/distanceFromTarget)
                angleDeg = degrees(angleRad)

                """
                When frameCenterX < boundingCenterX, the target is to the right of us.
                When frameCenterX > boundingCenterX, the target is to the left of us.
                We out put the angle as a negative when it is to the left of us.
                """ 
                if (frameCenterX < boundingCenterX):
                   angleDeg = degrees(angleRad)
                elif (frameCenterX > boundingCenterX):
                    angleDeg = degrees(angleRad)*(-1)

                print("Angle: {}".format(angleDeg))

                haveAngle = True
        else:
            haveAngle = False
            haveDistance = False

    return angleDeg, distanceFromTarget, haveAngle, haveDistance



def change_res(cap, width, height):
     cap.set(3, width)
     cap.set(4, height)


def main():

    # cond = threading.Condition()
    # notified = [False]

    # def connectionListener(connected, info):
    #     with cond:
    #         notified[0] = True
    #         cond.notify()


    #Initializing and connecting to network tables
    # NetworkTables.initialize(server='10.4.67.23')
    # NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    # with cond:
    #     if not notified[0]:
    #         cond.wait()

    # table = NetworkTables.getTable('vision')
   
    # pipeline4 = WideAngleGripFinal()
    pipeline3 = TapeRecCodeThree()
    print("before videocapture")
    # cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("http://localhost:1181/stream.mjpg")
    change_res(cap, 1080, 720)
    frame_count = 0
    # frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # print(frame_width)
    # print(frame_height)
    print("after videocapture")
    while True:
        have_frame, frame = cap.read()
        print("after read")
        if have_frame:
            pipeline3.process(frame)
            frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            print(frame_width)
            print(frame_height)

            print("Before extra processing")
            angle, distance, have_angle, have_distance = extra_processing(cap, pipeline3, frame)

            # cv2.imwrite("/home/pi/Vision2020/frames/" + "frame" + str(frame_count) + ".jpg", frame)

            cv2.imwrite("/home/pi/Vision2020/frames/frame.jpg", frame)

            print("After extra processing")
            # extra_processing(cap, pipeline3, frame)
            # table.putBoolean("have_angle", have_angle)
            # if have_angle:
                # table.putNumber("angle", angle)
            # table.putBoolean("have_distance", have_distance)
            # if have_distance:
                # table.putNumber("distance", distance)

            # cv2.imshow("frame", frame)
            frame_count += 1
            # print(frame_count)
            # hit q to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


if __name__ == "__main__":
    main()