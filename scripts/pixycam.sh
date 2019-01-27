#!/bin/bash
cd ~/
mkdir libs
cd ~/libs
sudo apt-get install git libusb-1.0-0-dev g++ -y
git clone https://github.com/charmedlabs/pixy2
cd pixy2/scripts && ./build_libpixyusb2.sh
