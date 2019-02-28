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
sudo mv camera.sh /usr/bin/
sudo chmod +x /usr/bin/camera.sh
sudo chmod +x opencv_AngleFinder_pi.py
sudo mv camera.service /lib/systemd/system/
sudo mv angleFinder.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/camera.service
sudo chmod 644 /lib/systemd/system/angleFinder.service
cd /lib/systemd/system/
sudo systemctl enable camera.service
sudo systemctl enable angleFinder.service
sudo systemctl start camera.service
sudo systemctl start angleFinder.service
cd ~/
sudo ln -s /dev/video0 /home/vid
sudo mv frc.json /boot