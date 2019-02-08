import cv2
from networktables import NetworkTables
from grip import TapeRecognitionCode

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
 
    # Find the bounding boxes of the contours to get x, y, width, and height
    for contour in pipeline.filter_contours_output:
        x, y, w, h = cv2.boundingRect(contour)
        center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
        center_y_positions.append(y + h / 2)
        widths.append(w)
        heights.append(h)

    # Publish to the '/vision/red_areas' network table


    if len(heights) == 2:

        print ('Box 1 center point', 'x: ' + str(center_x_positions[0]), 'y: ' + str(center_y_positions[0]))
        print ('Box 2 center point', 'x: ' + str(center_x_positions[1]), 'y: ' + str(center_y_positions[1]))
        print ('Box 1 width: ' + str(widths[0]), 'Box 2 width: ' + str(widths[1]))
        print ('Box 1 height: ' + str(heights[0]), 'Box 2 height: ' + str(heights[1]))
        
        midpoint = ((center_x_positions[0] + center_x_positions[1])/2)
        distance = abs(midpoint - 350)
        print ('distance', distance)

        angle = 35 * distance / 350

        if midpoint > 350:
            print ('Angle = ' + str(angle))
        else:
            angle = angle * -1
            print ('Angle = ' + str(angle))

        
        table.putNumber('angle', angle)
    
    return center_x_positions[0], center_y_positions[0], center_x_positions[1], center_y_positions[1]

def main():

    frame_print = input ("How many frames do you want? ")
    camera_used = input ("Which camera do you want to use? (0, 1, 2, or 3)")

    '''
    print('Initializing NetworkTables')
    NetworkTables.setClientMode()
    NetworkTables.setIPAddress('localhost')
    NetworkTables.initialize()
    '''
    

    print('Creating video capture')
    cap = cv2.VideoCapture(int(camera_used))

    print('Creating pipeline')
    pipeline = TapeRecognitionCode()

    frame_number = 0

    x1_center = 0
    x2_center = 0
    y1_center = 0
    y2_center = 0

    print('Running pipeline')
    while cap.isOpened():

        frame_number = frame_number + 1
        #print ("in while loop")
        have_frame, frame = cap.read()

        if have_frame:

            #print ("in if")
            pipeline.process(frame)
            if frame_number%int(frame_print) == 0:
                print (frame_number/20)
                extra_processing(pipeline)

    print('Capture closed')

if __name__ == '__main__':
    main()