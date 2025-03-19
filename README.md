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
  - `fswebcam` for capturing images: ```bash sudo apt update sudo apt install fswebcam ```
  - Python 3 (pre-installed on Raspberry Pi OS).
## Repository Structure
```plaintext
klipper-image-capture/
├── capture_images.py    # Python script to capture images during printing
├── start_print.sh      # Shell script to start image capture
├── stop_print.sh       # Shell script to stop image capture
└── README.md           # This file
```
## Installation
1. **Clone the Repository**: ```bash git clone https://github.com/<your-username>/klipper-image-capture.git cd klipper-image-capture ```
2. **Set Permissions**: Ensure the scripts are executable: ```bash chmod +x capture_images.py start_print.sh stop_print.sh ```
3. **Move Files to Klipper Directory**: Place the scripts in `/home/klipper/capture_images/`: ```bash mkdir -p /home/klipper/capture_images cp * /home/klipper/capture_images/ ```
4. **Verify Camera Access**: Ensure the `klipper` user can access the webcam: ```bash sudo usermod -aG video klipper ls /dev/video0 ```
## Configuration
### Modify Klipper Configuration
#### Add the following to your `printer.cfg` (e.g., `/home/klipper/printer_data/config/printer.cfg`) to integrate the scripts with Klipper: 
```[shell_command start_capture]
command: /bin/bash /home/klipper/capture_images/start_print.sh
timeout: 30.0
verbose: True

[shell_command stop_capture]
command: /bin/bash /home/klipper/capture_images/stop_print.sh
timeout: 30.0
verbose: True

[gcode_macro START_CAPTURE_SCRIPT]
description: "Start image capture"
gcode:
    RUN_SHELL_COMMAND CMD=start_capture
    {action_respond_info("Started image capture.")}

[gcode_macro STOP_CAPTURE_SCRIPT]
description: "Stop image capture"
gcode:
    RUN_SHELL_COMMAND CMD=stop_capture
    {action_respond_info("Stopped image capture.")}

[gcode_macro PRINT_START]
description: "Start Print Macro"
gcode:
    M190 S{params.BED|default(60)}
    M104 S{params.EXTRUDER|default(200)}
    M109 S{params.EXTRUDER|default(200)}
    G28
    G92 E0
    G1 Z5 F300
    G1 X20 Y330 F3000
    START_CAPTURE_SCRIPT

[gcode_macro PRINT_END]
description: "End Print Macro"
gcode:
    G91
    G1 Z10 F300
    G90
    G1 X20 Y330 F3000
    M104 S0
    M140 S0
    M107
    M84
    STOP_CAPTURE_SCRIPT``` 
#### Restart Klipper after editing: 
```bash sudo systemctl restart klipper```
### Customize `capture_images.py` (Optional)
- **Capture Interval**: Adjust `CAPTURE_INTERVAL` (default: 200 seconds) in `capture_images.py`.
- **Save Directory**: Change `BASE_SAVE_DIRECTORY` if desired.
- **Camera Device**: Update `CAMERA_DEVICE` if your webcam isn’t `/dev/video0`.
## Usage
1. Start a print via Fluidd or Mainsail. - The `PRINT_START` macro triggers `start_print.sh`, which runs `capture_images.py` in the background. - Images are saved to `/home/klipper/capture_images/print_<timestamp>/`.
2. End the print. - The `PRINT_END` macro triggers `stop_print.sh`, stopping the image capture.
3. Access images: ```bash ls /home/klipper/capture_images/print_<timestamp>/ ```
## Troubleshooting
- **Camera Not Found**: Verify the device with `ls /dev/video*` and update `CAMERA_DEVICE` in `capture_images.py`.
- **`RUN_SHELL_COMMAND` Errors**: Ensure your Klipper installation supports the `shell_command` extension. Update Klipper via KIAUH if needed: ```bash cd ~/kiauh ./kiauh.sh ```
- **Permission Issues**: Ensure the `klipper` user has write access to `/home/klipper/capture_images`: ```bash sudo chown -R klipper:klipper /home/klipper/capture_images chmod -R 755 /home/klipper/capture_images ```
- **High CPU Usage**: Check resource usage with: ```bash top ``` Adjust `CAPTURE_INTERVAL` or image resolution if needed.
## Contributing
Feel free to submit issues or pull requests to improve this project. Suggestions for better integration with Klipper or additional features (e.g., timelapse generation) are welcome!
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
## Acknowledgments
- Built with inspiration from the Klipper community.
- Thanks to the developers of `fswebcam` and Klipper.
