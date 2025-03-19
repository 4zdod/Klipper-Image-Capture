#!/bin/bash
# File: /home/klipper/capture_images/start_print.sh

# Deleting while if it exists
rm -f /tmp/stop_capture

# Activating script on a backgroundоне
nohup /usr/bin/python3 /home/klipper/capture_images/capture_images.py > /home/klipper/capture_images/capture_log.txt 2>&1 &
echo "Started image capture."
