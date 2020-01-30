from grip_three_convexhull import TapeRecCodeThree
import cv2

pipeline3 = TapeRecCodeThree()

frame = cv2.imread("C:\\Users\\theak\\Documents\\Akash\\Robotics\\Robot_Programs\\Competition\\Robot2019-RaspberryPI\\frame.jpg")
# frame = cv2.imread("C:\\Users\\theak\\Documents\\Akash\\Robotics\\Robot_Programs\\Competition\\Robot2019-RaspberryPI\\frame2.jpg")

img = cv2.resize(frame, (1080,720))

cv2.imwrite("C:\\Users\\theak\\Documents\\Akash\\Robotics\\Robot_Programs\\Competition\\Robot2019-RaspberryPI\\resized_frame.jpg", img)

pipeline3.process(img)

