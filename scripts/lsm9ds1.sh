#!/bin/bash
cd ~/
mkdir libs
cd ~/libs
sudo apt-get install libi2c-dev git -y
git clone git://git.drogon.net/wiringPi
cd wiringPi
git pull origin
./build
cd ~/libs
git clone https://github.com/akimach/LSM9DS1_RaspberryPi_Library.git
cd LSM9DS1_RaspberryPi_Library
make -j4
sudo make install -j4