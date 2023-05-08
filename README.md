## RTSP Stream Capture from IP Camera using OpenCV

IP cameras supports Real Time Streaming Protocol (RTSP) to control audio and video streaming. This is an example how to capture RTSP stream from IP camera using OpenCV and Python.

## Requirements

- opencv-python
- argparse
- datetime

## Usage

Example: ``python rtsp_record.py --cam_username admin --cam_pass admin12345 --ip 192.168.0.3:554 --fps 25 --flip False --num 101 --view-img True``

``` Running from terminal 
python rtsp_record.py 

--cam_username      Rtsp Cam Username, default= admin
--cam_pass      Rtsp Cam Password, default= admin
--ip            Rtsp Cam Ip-Address, default= 192.168.0.3
--num           Rtsp Cam Channel number, default= 101
--fps           Frame Rate
--flip          Flip video
--save-video    Rtsp Video-Save, default= True 
--view-img      OpenCV imshow() View Stream default= False 

  ```
