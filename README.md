## RTSP Stream Capture from IP Camera using OpenCV

This example demonstrates how to capture an RTSP stream from an IP camera using OpenCV and Python.

### Requirements

- opencv-python
- threading
- datetime
- argparse
- datetime

### Usage

Example:
```bash
python rtsp_record.py --cam_username admin --cam_pass admin12345 --ip 192.168.0.3:554 --fps 25 --flip False --num 101 --view-img True
```

### Running from Terminal

```bash
python rtsp_record.py 
--cam_username      # Rtsp Cam Username, default= admin
--cam_pass          # Rtsp Cam Password, default= admin12345
--ip                # Rtsp Cam IP Address, default= 192.168.0.3
--num               # Rtsp Cam Channel number, default= 101
--fps               # Frame Rate
--flip              # Flip video, default= False
--save-video        # Rtsp Video-Save, default= True 
--view-img          # OpenCV imshow() View Stream, default= False 
```

### Notes

- `--cam_username`: RTSP camera username, default is set to "admin".
- `--cam_pass`: RTSP camera password, default is set to "admin12345".
- `--ip`: RTSP camera IP address, default is set to "192.168.0.3".
- `--num`: RTSP camera channel number, default is set to "101".
- `--fps`: Frame rate.
- `--flip`: Flip video, default is set to False.
- `--save-video`: Option to save the RTSP video, default is set to True.
- `--view-img`: Option to view the stream using OpenCV's imshow() function, default is set to False.
