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
    '''
    table = NetworkTables.getTable('/vision/red_areas')
    table.putNumberArray('x', center_x_positions)
    table.putNumberArray('y', center_y_positions)
    table.putNumberArray('width', widths)
    table.putNumberArray('height', heights)
    '''

    '''
    print ('Box 1 center point', 'x: ' + str(center_x_positions[0]), 'y: ' + str(center_y_positions[0]))
    print ('y', center_y_positions)
    print ('width', widths)
    print ('height', heights)
    '''

    if len(heights) == 2:

        print ('Box 1 center point', 'x: ' + str(center_x_positions[0]), 'y: ' + str(center_y_positions[0]))
        print ('Box 2 center point', 'x: ' + str(center_x_positions[1]), 'y: ' + str(center_y_positions[1]))
        print ('Box 1 width: ' + str(widths[0]), 'Box 2 width: ' + str(widths[1]))
        print ('Box 1 height: ' + str(heights[0]), 'Box 2 height: ' + str(heights[1]))
        
        midpoint = abs(((center_x_positions[0] + center_x_positions[1])/2) - 350)
        print ('distance', midpoint)

        angle = 35 * midpoint / 350
        print ('Angle = ' + str(angle))
        table.putNumber('angle', angle)

    

def main():

    frame_print = input ("How many frames do you want? ")

    '''
    print('Initializing NetworkTables')
    NetworkTables.setClientMode()
    NetworkTables.setIPAddress('localhost')
    NetworkTables.initialize()
    '''

    print('Creating video capture')
    cap = cv2.VideoCapture(1)

    print('Creating pipeline')
    pipeline = TapeRecognitionCode()

    frame_number = 0

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
            #img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            cv2.imshow('video', cv2.resize(frame, (800, 600)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cap.release()

    cv2.destroyAllWindows()

    print('Capture closed')


if __name__ == '__main__':
    main()