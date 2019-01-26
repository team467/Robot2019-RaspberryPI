import pixy 
from ctypes import *
from pixy import *
import math
import threading
from networktables import NetworkTables

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

frameRate = input ("Type in the number of frames: ")
iterations = 0
# Pixy2 Python SWIG get blocks example #

print ("Pixy2 Python SWIG Example -- Get Blocks")

pixy.init ()
pixy.change_prog ("color_connected_components");

class Blocks (Structure):
  _fields_ = [ ("m_signature", c_uint),
    ("m_x", c_uint),
    ("m_y", c_uint),
    ("m_width", c_uint),
    ("m_height", c_uint),
    ("m_angle", c_uint),
    ("m_index", c_uint),
    ("m_age", c_uint) ]

blocks = BlockArray(100)
frame = 0

old_x = 0

while 1:
	iterations = iterations + 1
  	count = pixy.ccc_get_blocks (100, blocks)
	#print (count)

	re_order_obj = {}
  	if count > 0:

    		#print 'frame %3d:' % (frame)
    		frame = frame + 1

	
	if iterations == 1:
		for index in range (0, count):
			print '[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d M_INDEX=%3d]' % (blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width, blocks[index].m_height, blocks[index].m_index)

	for index in range (0, count):

		obj = blocks[index]

		re_order_obj[obj.m_index] = obj


	change_in_x = blocks[0].m_x - old_x

	if abs(change_in_x) > 10:

		if frame%int(frameRate) == 0:

			print (frame/int(frameRate))

	
		for index in re_order_obj:
	
			if count > 0:
				area1 = float(blocks[0].m_width * blocks[0].m_height)
				area2 = float(blocks[1].m_width * blocks[1].m_height)

				if (area1 and area2 > 200):
					
					print '[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d M_INDEX=%3d]' % (re_order_obj[index].m_signature, re_order_obj[index].m_x, re_order_obj[index].m_y, re_order_obj[index].m_width, re_order_obj[index].m_height, re_order_obj[index].m_index)

		midpoint = ((blocks[0].m_x + blocks[1].m_x + blocks[1].m_width)/2)
		print ("Midpoint = " + str(midpoint))
		distance_from_center = abs(midpoint - 165)
		print ("Distance from center = " + str(distance_from_center))
		angle = distance_from_center * (32.5/165)
		
		if midpoint < 185:
			angle = -1 * angle
			print ("Angle = " + str(angle))
		else:
			print ("Angle = " + str(angle))	
		
		table.putNumber('angle', angle)
		old_x = blocks[0].m_x