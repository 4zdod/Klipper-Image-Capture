# Klipper Image Capture

This repository contains scripts to capture images at regular intervals during 3D printing using a Raspberry Pi running Klipper. The primary script, `capture_images.py`, works alongside shell scripts (`start_print.sh` and `stop_print.sh`) to start and stop image capture in sync with print jobs, integrating with Klipper's configuration.

## Features
- Captures images using a webcam (e.g., `/dev/video0`) every 200 seconds (configurable).
- Saves images to a timestamped directory under `/home/klipper/capture_images`.
- Integrates with Klipper via custom G-code macros (`START_CAPTURE_SCRIPT` and `STOP_CAPTURE_SCRIPT`).
- Uses `fswebcam` for image capture and supports graceful shutdown via a stop file.

## Prerequisites
- **Hardware**:
  - Raspberry Pi (tested on Raspberry Pi 3).
  - USB webcam (accessible as `/dev/video0`).
  - 3D printer running Klipper.
- **Software**:
  - Raspberry Pi OS (or compatible Linux distribution).
  - Klipper, Fluidd, and Moonraker installed (e.g., via KIAUH).
  - `fswebcam` for capturing images:
    ```bash
    sudo apt update
    sudo apt install fswebcam
  - Python 3 (pre-installed on Raspberry Pi OS).

## Repository Structure
klipper-image-capture/
├── capture_images.py    # Python script to capture images during printing
├── start_print.sh      # Shell script to start image capture
├── stop_print.sh       # Shell script to stop image capture
└── README.md           # This file
