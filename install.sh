#!/bin/bash
sudo mv * ../
cd ../
cd scripts
sudo chmod +x *
./lsm9ds1.sh
./pynetworktables.sh
./pixycam.sh
cd ~/