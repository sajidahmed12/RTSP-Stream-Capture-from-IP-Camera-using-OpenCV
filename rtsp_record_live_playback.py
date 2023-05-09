import cv2
import os
import threading
import argparse
from datetime import datetime

## run commmand:  python rtsp_record.py 

def get_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--cam_username', action='store', type=str, required=False, default='admin', help="ip_camera's username")
    arg_parser.add_argument('--cam_pass', action='store', type=str, required=False, default='admin', help="ip_camera's password")
    arg_parser.add_argument('--ip', action='store', type=str, required=False, default='192.168.0.1', help="ip_camera's ip address")
    #arg_parser.add_argument('--num', action='store', type=str, required=False, default=3101 , help="ip_camera's channel number")
    arg_parser.add_argument('--fps', action='store', type=int, required=False, default=25 , help="FPS")
    #arg_parser.add_argument('--flip', action='store', type=bool, required=False, default=False , help="Flip video while recording")
    arg_parser.add_argument('--save-video', action='store', type=bool, required=False, default=True , help="Save the RTSP video in recordings directory")
    arg_parser.add_argument('--live', action='store', type=bool, required=False, default=True , help="Live record or Tracks playback record")
    arg_parser.add_argument('--start-time', action='store', type=str, required=False, default='20230501T154200', help="playback_start-time")
    arg_parser.add_argument('--end-time', action='store', type=str, required=False, default='46500', help="playback_start-time")
    arg_parser.add_argument('--view-img', action='store', type=bool, required=False, default=True , help="View the RTSP video in openCV imshow() mode")

    return arg_parser.parse_args()


def rtsp_record(cam_username, cam_pass, ip, num, fps,save_video, live, start_time, end_time, view_img):
    
    if live:
        RTSP_URL = 'rtsp://'+str(cam_username)+':'+str(cam_pass)+'@'+str(ip)+'/Streaming/channels/'+str(num)
        print("RTSP LIVE URL: "+RTSP_URL)
    if not live:
        RTSP_URL = 'rtsp://'+str(cam_username)+':'+str(cam_pass)+'@'+str(ip)+'/Streaming/tracks/'+str(num)+'?starttime='+start_time+'Z'
        print("RTSP Playback URL: "+RTSP_URL)

    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;tcp' 
    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print('Cannot open RTSP stream. Possibly the url/video is broken')
        exit(-1)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    if not os.path.exists("recording"):
        os.makedirs("recording")

    video_filename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")+"_cam_"+str(num)
    video_codec = cv2.VideoWriter_fourcc(*'XVID')
    video_output = cv2.VideoWriter('recording/'+video_filename+'.mp4', video_codec, fps, (frame_width, frame_height))

    frame_count = 0
    print("[INFO]: RTSP Streaming Started.....")
    while True:
        ret, frame = cap.read()
        if num == 3201 or num ==3301:
            frame = cv2.flip(frame,0)

        if ret == True:
            frame_count += 1
            if save_video:
                video_output.write(frame)
                print("[INFO]: Saving video frames...."+str(frame_count))
            else:
                print("[INFO]: no saving......")
            if not view_img:
                cv2.namedWindow("RTSP Video Frame: Cam "+str(num), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                cv2.imshow("RTSP Video Frame: Cam "+str(num), frame)

            #if cv2.waitKey(1) & 0xFF == ord('q'):
            if cv2.waitKey(1) and frame_count == end_time:
                print("[INFO]: Saving video frames stopped!!!..."+str(frame_count))        
                break
        else:
            break

    cap.release()
    video_output.release()
    cv2.destroyAllWindows()
    print('Video was saved!')

if __name__ =='__main__':
    args = get_parser()

    camera_list =[101,201,301, 401,501,601,701,801]
    thread_list = []

    for i in range(len(camera_list)):
        thread = threading.Thread(target=rtsp_record,args=(args.cam_username, args.cam_pass, args.ip, camera_list[i], args.fps, args.save_video, args.live, args.start_time, args.end_time, args.view_img),daemon=False)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()
