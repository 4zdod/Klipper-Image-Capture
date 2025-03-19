#!/bin/bash
# File: /home/klipper/capture_images/stop_print.sh

# Create stop file to signal the Python script to exit
touch /tmp/stop_capture

# Wait a moment to allow graceful exit
sleep 2

# Force kill the script if it's still running
pkill -f "python3 /home/klipper/capture_images/capture_images.py"

echo "Stopped image capture."
