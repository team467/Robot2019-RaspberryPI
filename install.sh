#!/bin/bash
sudo mount -o remount, rw /
sudo su pi
sudo apt-get install git -y
git clone -b programs-added https://github.com/team467/Robot2019-RaspberryPI.git
cd Robot2019-RaspberryPI
sudo mv * ../
cd ../
cd scripts
sudo chmod +x *
./lsm9ds1.sh
./pynetworktables.sh
cd ~/
sudo rm -r Robot2019-RaspberryPI
sudo mv camera.sh /etc/init.d/