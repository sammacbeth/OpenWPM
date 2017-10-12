#! /bin/bash

set -x

export DISPLAY=:0
Xvfb $DISPLAY -screen 0 $2 -ac &
sleep 1
openbox &

x11vnc -storepasswd vnc /tmp/vncpass
x11vnc -rfbport 5900 -rfbauth /tmp/vncpass -forever > /dev/null 2>&1 &

cd /home/openwpm/OpenWPM
python crawl.py $1
