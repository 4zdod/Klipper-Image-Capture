#!/usr/bin/env python3
import os
import time
import signal
import sys
from datetime import datetime
import subprocess

CAPTURE_INTERVAL = 200  # Seconds between captures (5 minutes = 300 seconds)
BASE_SAVE_DIRECTORY = "/home/klipper/capture_images"  # Adjusted to new path
CAMERA_DEVICE = "/dev/video0"  # Adjust based on your camera (check with 'ls /dev/video*')
STOP_FILE = "/tmp/stop_capture"

# Create a new directory for this print based on timestamp
PRINT_START_TIME = datetime.now().strftime("%Y%m%d_%H%M%S")
SAVE_DIRECTORY = os.path.join(BASE_SAVE_DIRECTORY, f"print_{PRINT_START_TIME}")

# Ensure the save directory exists
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

# Signal handler to gracefully exit
def signal_handler(sig, frame):
    print("Stopping image capture...")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

# Function to capture an image
def capture_image():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"print_image_{timestamp}.jpg"
    filepath = os.path.join(SAVE_DIRECTORY, filename)
    
    try:
        subprocess.run([
            "fswebcam",
            "-d", CAMERA_DEVICE,
            "-i", "0",         # Added to specify input 0, removes "No input specified" warning
            "-r", "1280x720",  # Resolution (adjust as needed)
            "--no-banner",     # Remove timestamp banner
	    "-S", "10",	       # Skip first 10 frames
	    "--jpeg", "95",    # Improving quality
	    "-p", "MJPEG",     # MJPG
            filepath
        ], check=True)
        print(f"Image saved: {filepath}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to capture image: {e}")

# Main loop
def main():
    print(f"Starting image capture every {CAPTURE_INTERVAL} seconds in {SAVE_DIRECTORY}...")
    while True:
        if os.path.exists(STOP_FILE):
            print("Stop file detected, exiting...")
            break
        capture_image()
        time.sleep(CAPTURE_INTERVAL)

if __name__ == "__main__":
    main()
