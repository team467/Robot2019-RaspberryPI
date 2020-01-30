# This version of AngleTracker2020 is supposed to be used on the raspberry pi

import cv2
#from networktables import NetworkTables
# from grip_two import TapeRecCodeTwo
from grip_three_convexhull import TapeRecCodeThree
#from grip import WideAngleGrip
from math import *

def extra_processing(cap, pipeline3, frame):
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
                # cv2.imshow("frame", frame) 
                print("h = {}, w = {}, x = {}, y = {}, a = {}".format(h, w, x, y, (w*h)))

                # boundingCenterX = ((x+x+w)/2)
                # William made some changes here with the bounding center calcs
                # if (x > w):
                #     boundingCenterX = (x + w/2)
                # elif (x < w):
                #     boundingCenterX = (x - w/2) 
                boundingCenterX = (x + (w/2))

                frameCenterX = 540

                # Initializing zero which is dead on
                distanceFromCenterFrameInches = 0

                """
                When frameCenterX < boundingCenterX, the target is to the right of us.
                When frameCenterX > boundingCenterX, the target is to the left of us.
                """                 
                if (frameCenterX < boundingCenterX):
                   distanceFromCenterFrameInches = (boundingCenterX - frameCenterX) * (39.25/w)
                elif (frameCenterX > boundingCenterX):
                    distanceFromCenterFrameInches = (frameCenterX - boundingCenterX) * (39.25/w)

                
                
                #print(distanceFromCenterFrameInches)

                # distanceFromTarget = float((372*46.25)/h) 
                # distanceFromTarget = float((434*41)/h)
                # distanceFromTarget = float(((-50)/151)*h + 186.06623) (This is a function we came up with)
                distanceFromTarget = float((122*150)/h)
                haveDistance = True

                # we need to find a better ratio using more accurate tests


                feet = distanceFromTarget/12
                inches = distanceFromTarget%12

                print("Distance from frame center to box center: {}, Bounding box center: {}, Frame center: {}".format((boundingCenterX-frameCenterX), boundingCenterX, frameCenterX))

                print("Distance in inches: {}, Distance in feet and inches: {} feet, {} inches".format(int(distanceFromTarget), int(feet), int(inches)))

                angleRad = atan(distanceFromCenterFrameInches/distanceFromTarget)
                # angleDeg = degrees(angleRad)



                # Take a look at this if it makes sense. 
                # It just makes the angle negative or positive 
                # We out put the angle as a negative when it is to the left of us.

            
                if (frameCenterX < boundingCenterX):
                   angleDeg = degrees(angleRad)
                elif (frameCenterX > boundingCenterX):
                    angleDeg = degrees(angleRad)*(-1)
                

                haveAngle = True

                print("Angle: {}".format(angleDeg))

        



    return haveAngle, haveDistance, angleDeg, distanceFromTarget, frame


        

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
    # pipeline2 = TapeRecCodeTwo()
    pipeline3 = TapeRecCodeThree()
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # cap = cv2.VideoCapture(0)
    change_res(cap, 1080, 720)
    frame_count = 0
    while True:
        have_frame, frame = cap.read()
        if have_frame:

            frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            print(frame_width)
            print(frame_height)

            pipeline3.process(frame)
            extra_processing(cap, pipeline3, frame)

            cv2.imwrite("/home/pi/Vision2020/frames/frame.jpg", frame)
            # cv2.imshow("frame", frame)
            frame_count += 1

            print("frame")

            # hit q to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            elif frame_count == 5:
                break


if __name__ == "__main__":
    main()