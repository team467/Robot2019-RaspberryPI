#!/bin/bash
sudo su pi
sudo apt-get install git -y
sudo mv * ../
cd ../
cd scripts
sudo chmod +x *
./lsm9ds1.sh
./pynetworktables.sh
./pixycam.sh
cd ~/
sudo rm -r Robot2019-RaspberryPI
