import cv2
import os
import argparse
from datetime import datetime


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--cam_user', action='store', type=str, required=False, default='admin', help="ip_camera's username")
arg_parser.add_argument('--password', action='store', type=str, required=True, default='admin', help="ip_camera's password")
arg_parser.add_argument('--ip', action='store', type=str, required=False, default='192.168.1000.3', help="ip_camera's ip address")
arg_parser.add_argument('--num', action='store', type=str, required=False, default=101 , help="ip_camera's channel number")
arg_parser.add_argument('--save_video', action='store', type=bool, required=False, default=True , help="Save the RTSP video in recordings directory")
arg_parser.add_argument('--view-img', action='store', type=bool, required=False, default=False , help="View the RTSP video in openCV imshow() mode")
args = arg_parser.parse_args()

#example
#RTSP_URL = 'rtsp://admin:admin12345@192.168.0.3/Streaming/channels/101'

RTSP_URL = 'rtsp://'+str(args.cam_user)+':'+str(args.password)+'@'+str(args.ip)+'/Streaming/channels/'+str(args.num)

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;tcp' 

cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print('Cannot open RTSP stream. Possibly the url/video is broken')
    exit(-1)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = 20

if not os.path.exists("recording"):
    os.makedirs("recording")

video_filename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
video_codec = cv2.VideoWriter_fourcc(*'XVID')
video_output = cv2.VideoWriter('recording/'+video_filename+'.mp4', video_codec, fps, (frame_width, frame_height))

frame_count = 0
print("[INFO]: RTSP Streaming Started.....")
while True:
    ret, frame = cap.read()
   
    if ret == True:
        frame_count += 1
        if args.save_video:
            video_output.write(frame)
            print("[INFO]: Saving video frames...."+str(frame_count))
        if args.view_img:
            cv2.namedWindow("RTSP Video Frame", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
            cv2.imshow("RTSP Video Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO]: Saving video frames stopped!!!..."+str(frame_count))        
            break
    else:
        break

cap.release()
video_output.release()
cv2.destroyAllWindows()
print('Video was saved!')
