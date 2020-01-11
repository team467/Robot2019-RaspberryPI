import cv2

#from networktables import NetworkTables
from grip_two import TapeRecCodeTwo


def extra_processing(pipeline2, frame):
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
    print(len(pipeline2.filter_contours_output))
    for contour in pipeline2.filter_contours_output:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 80 and h > 80:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)

        center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
        center_y_positions.append(y + h / 2)
        widths.append(w)
        heights.append(h)
        
    # print(pipeline2.filter_contours_output)

def main():
    pipeline2 = TapeRecCodeTwo()
    cap = cv2.VideoCapture(1)
    while True:
        have_frame, frame = cap.read()
        if have_frame:
            pipeline2.process(frame)
            extra_processing(pipeline2, frame)
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

if __name__ == "__main__":
    main()