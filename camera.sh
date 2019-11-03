sudo mount -o remount, rw /
cd /home/pi

order=(0 1 2 3)
x=0

for i in $(v4l2-ctl --list-devices | grep video)
do
  echo $i | awk '{print substr($0,length($0),1)}'
  order[$x]=$(echo $i | awk '{print substr($0,length($0),1)}')
  x=$x+1
done

sleep 30

while true
do
  sudo python camera.py ${order[1]} ${order[0]} ${order[2]} ${order[3]} $x+1
done
