import cv2
#from networktables import NetworkTables
from grip_two import TapeRecCodeTwo
from grip_three_convexhull import TapeRecCodeThree


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
    x = 0
    y = 0
    w = 0
    h = 0
 
    # Find the bounding boxes of the contours to get x, y, width, and height
    # print(len(pipeline3.filter_contours_output))

    for contour in pipeline3.filter_contours_output:

        x, y, w, h = cv2.boundingRect(contour)

        # cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)

        center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
        center_y_positions.append(y + h / 2)
        widths.append(w)
        heights.append(h)
    
        if float(w/h) >= 2:
            if float(w/h) <= 2.3:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
                cv2.line(frame, (x,y), (x,y), (0,255,0), 10)
                cv2.imshow("frame", frame) 
                print("h = {}, w = {}, x = {}, y = {}, a = {}".format(h, w, x, y, (w*h)))

    # if len(pipeline3.filter_contours_output) > 1:
        # cv2.imshow("frame", frame)

    # if len(pipeline3.filter_contours_output) == 1:
    #     cv2.imshow("frame", frame)

    # if (len(widths) == 1) and (len(heights) == 1):
        # do angle calculations here

        

def main():
    pipeline2 = TapeRecCodeTwo()
    pipeline3 = TapeRecCodeThree()
    cap = cv2.VideoCapture(1)
    while True:
        have_frame, frame = cap.read()
        if have_frame:
            pipeline3.process(frame)
            extra_processing(pipeline3, frame)
            # cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

if __name__ == "__main__":
    main()