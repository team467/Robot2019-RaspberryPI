import time
import VL53L0X
from networktables import NetworkTables

NetworkTables.initialize(server='10.4.67.2')
sensors = NetworkTables.getTable('sensors')

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
# I2C Address can change before tof.open()
# tof.change_address(0x32)
tof.open()
# Start ranging
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing/1000))

while True:
    distance = tof.get_distance()
    sensors.putNumber('tof', distance)
    #print("%d mm" % (distance))

    time.sleep(timing/1000000.00)

tof.stop_ranging()
tof.close()
