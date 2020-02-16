import cv2

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    print("frame")

    ret2, frame2 = cap2.read()
    print("frame2")

    cv2.imwrite("/home/pi/Vision2020/frames/frame1.jpg", frame)
    cv2.imwrite("/home/pi/Vision2020/frames/frame2.jpg", frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

