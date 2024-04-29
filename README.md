## RTSP Stream Capture from IP Camera using OpenCV

IP cameras support Real Time Streaming Protocol (RTSP) to control audio and video streaming. This is an example of capturing an RTSP stream from an IP camera using OpenCV and Python.

## Requirements for Python

- opencv-python
- threading
- datetime
- argparse
- datetime

## Requirements for C++

- cmake 
- ninja-build 
- libopencv-dev 
- libboost-all-dev

## Python Usage

Example: ``python rtsp_video_downloader.py --cam_list 1 4 --fps 1 --end-time 5``
Running from terminal 

``` 
python rtsp_record.py 
```

## C++ Usage

Create a CMake Configuration 'CMakeLists.txt' (already present in the project).
Generate Build Files with CMake 

```
mkdir build
cd build
cmake -G Ninja ..


```
## Build the project with

`ninja`

## Run Your Executable

```
./rtsp_video_downloader --<cam_list>

```

## Options

```
--help          Show this help message and exit
--cam_username  Rtsp Cam Username, default= admin
--cam_pass      Rtsp Cam Password, default= admin
--ip            Rtsp Cam Ip-Address, default= 192.168.0.3
--cam_list      List of cameras for downloading videos
--fps           Frame Rate
--live          Live record or Tracks playback record
--start-time    playback video _start-time
--end-time      playback video end-time
--out_dir       save_video_dir
  ```
