import cv2


def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)


# cap = cv2.VideoCapture(0, cv2.CAP_V4L)
cap = cv2.VideoCapture(0)
change_res(1280, 720)
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("Frame width: ", frame_width)
print("Frame height: ", frame_height)
while True:
    ret, frame = cap.read()
    cv2.imshow("frame", frame)
    print("frame")
    # cv2.imwrite("/home/pi/Vision2020/frames/frame.jpg", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    