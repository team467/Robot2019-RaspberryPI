import time
import cv2
from networktables import *
from grip import TapeRecognitionCode
import threading
from ctypes import *

def extra_processing(pipeline):
    """
    Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
    :param pipeline: the pipeline that just processed an image
    :return: None
    """
    center_x_positions = []
    center_y_positions = []
    widths = []
    heights = []
    angle = 0
    # Find the bounding boxes of the contours to get x, y, width, and height
    for contour in pipeline.filter_contours_output:
        x, y, w, h = cv2.boundingRect(contour)
        center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
        center_y_positions.append(y + h / 2)
        widths.append(w)
        heights.append(h)

    # Publish to the '/vision/red_areas' network table


    if len(heights) == 2:

        '''
        print ('Box 1 center point', 'x: ' + str(center_x_positions[0]), 'y: ' + str(center_y_positions[0]))
        print ('Box 2 center point', 'x: ' + str(center_x_positions[1]), 'y: ' + str(center_y_positions[1]))
        print ('Box 1 width: ' + str(widths[0]), 'Box 2 width: ' + str(widths[1]))
        print ('Box 1 height: ' + str(heights[0]), 'Box 2 height: ' + str(heights[1]))
        '''

        midpoint = ((center_x_positions[0] + center_x_positions[1])/2)
        distance = abs(midpoint - (350* pipeline._TapeRecognitionCode__cv_resize_fx))

        #print ('distance', distance)

        angle = 35 * distance / (350* pipeline._TapeRecognitionCode__cv_resize_fx)

        if midpoint < (350* pipeline._TapeRecognitionCode__cv_resize_fx):
            angle = angle * -1
    
    return angle

def main():

    turning_angle = 0 

    frame_print = input ("How many frames do you want? ")
    camera_used = input ("Which camera do you want to use? (0, 1, 2, or 3)")

    print('Initializing NetworkTables')
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
    print("Connected!")

    table = NetworkTables.getTable('vision')
    

    print('Creating video capture')
    cap = cv2.VideoCapture(int(camera_used))

    frame_number = 0

    print('Creating pipeline')
    pipeline = TapeRecognitionCode()

    print('Running pipeline')
    while cap.isOpened():

        frame_number = frame_number + 1

        #print ("in while loop")
        have_frame, frame = cap.read()

        if have_frame:
            #time1 = time.clock() * 1000
            #print ("in if")
            pipeline.process(frame)
            if pipeline is not None:
                turning_angle = extra_processing(pipeline)

                table.putNumber('angle', turning_angle)

                if frame_number%int(frame_print) == 0:

                    '''
                    print (frame_number/int(frame_print))
                    print ('Box 1 center point', 'x: ' + str(x1_center), 'y: ' + str(y1_center))
                    print ('Box 2 center point', 'x: ' + str(x2_center), 'y: ' + str(y2_center))
                    print ('Box 1 width: ' + str(width1), 'Box 2 width: ' + str(width2))
                    print ('Box 1 height: ' + str(height1), 'Box 2 height: ' + str(height2))
                    '''
                    
                    print ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxAngle = ' + str(turning_angle))

            #time2 = time.clock() * 1000

            #print (time2 - time1)
                    

    print('Capture closed')

if __name__ == '__main__':
    main()