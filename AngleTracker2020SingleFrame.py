# This version of AngleTracker2020 is supposed to be used locally

import cv2
#from networktables import NetworkTables
# from grip_two import TapeRecCodeTwo
# from grip_three_convexhull_trials import TapeRecCodeThreeTrials
from grip_three_convexhull import TapeRecCodeThree
#from grip import WideAngleGrip
from math import *

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
 
    # Find the bounding boxes of the contours to get x, y, width, and height
    # print(len(pipeline3.filter_contours_output))

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
                #William made some changes here with the bounding center calcs
                # if (x > w):
                #     boundingCenterX = (x + w/2)
                # elif (x < w):
                #     boundingCenterX = (x - w/2) 
                boundingCenterX = (x + (w/2))

                frameCenterX = 540

                # Initializing zero which is dead on
                distanceFromCenterFrameInches = 0
                if (frameCenterX < boundingCenterX):
                   distanceFromCenterFrameInches = (boundingCenterX - frameCenterX) * (39.25/w)
                elif (frameCenterX > boundingCenterX):
                    distanceFromCenterFrameInches = (frameCenterX - boundingCenterX) * (39.25/w)

                
                
                #print(distanceFromCenterFrameInches)

                # distanceFromTarget = float((372*46.25)/h) 
                #distanceFromTarget = float((434*41)/h)
                # distanceFromTarget = float(((-50)/151)*h + 186.06623)
                distanceFromTarget = float((122*150)/h)

                # we need to find a better ratio using more accurate tests


                feet = distanceFromTarget/12
                inches = distanceFromTarget%12

                print("Distance from frame center to box center: {}, Bounding box center: {}, Frame center: {}".format((boundingCenterX-frameCenterX), boundingCenterX, frameCenterX))

                print("Distance in inches: {}, Distance in feet and inches: {} feet, {} inches".format(int(distanceFromTarget), int(feet), int(inches)))

                angleRad = atan(distanceFromCenterFrameInches/distanceFromTarget)
                angleDeg = degrees(angleRad)

                print("Angle: {}".format(angleDeg))


        

    # if len(pipeline3.filter_contours_output) > 1:
        # cv2.imshow("frame", frame)

    # if len(pipeline3.filter_contours_output) == 1:
    #     cv2.imshow("frame", frame)

    # if (len(widths) == 1) and (len(heights) == 1):
        # do angle calculations here


def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


def main():
    pipeline3 = TapeRecCodeThree()

    frame = cv2.imread("C:\\Users\\theak\\Documents\\Akash\\Robotics\\Robot_Programs\\Competition\\Robot2019-RaspberryPI\local_frame.png")
    cv2.imshow("frame", frame)
    pipeline3.process(frame)
    extra_processing(pipeline3, frame)
    # cv2.imshow("frame", frame)
    while True:
        # hit q to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    main()