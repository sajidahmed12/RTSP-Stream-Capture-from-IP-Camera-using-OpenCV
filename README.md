## RTSP Stream Capture from IP Camera using OpenCV & Video Recording tool


IP cameras supports Real Time Streaming Protocol (RTSP) to control audio and video streaming. This is an example how to capture RTSP stream from IP camera using OpenCV and Python.

## Requirements

opencv-python
argparse
datetime

## Usage

``` Running from terminal 
python rtsp_record.py --cam_user admin --password Ab123456 --ip 192.168.100.240:554 --num 402 --view-img True

python rtsp_record.py 

--cam_user      Rtsp Cam Username, default= admin
--password      Rtsp Cam Password, default= admin
--ip            Rtsp Cam Ip-Address, default= 192.168.0.3
--num           Rtsp Cam Channel number, default= 101
--save-video    Rtsp Video-Save, default= True 
--view-img      OpenCV imshow() View Stream default= False 

  ```
