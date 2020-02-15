from AngleTracker2020_pi_v2_Draft import distanceFromTarget1 
from AngleTracker2020_pi_v2_camera2 import distanceFromTarget2
from AngleTracker2020_pi_v2_camera3 import distanceFromTarget3


float average_distance = (distanceFromTarget1 + distanceFromTarget2 + distanceFromTarget3)/3

print (average_distance)


