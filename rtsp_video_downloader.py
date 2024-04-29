import os
import cv2
import argparse
import threading
from datetime import datetime, timedelta


def get_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--cam_username', action='store', type=str, required=False, default='admin', help="ip_camera's username")
    arg_parser.add_argument('--cam_pass', action='store', type=str, required=False, default='admin', help="ip_camera's password")
    arg_parser.add_argument('--ip', action='store', type=str, required=False, default='192.168.0.1', help="ip_camera's ip address")
    arg_parser.add_argument('--cam_list', nargs='+', help='<Required> Set flag', type=int,required=True)
    arg_parser.add_argument('--save_video', action='store', type=bool, required=False, default=True , help="Save the RTSP video in recordings directory")
    arg_parser.add_argument('--fps', action='store', type=int, required=False, default=4, help="FPS")
    arg_parser.add_argument('--live', action='store', type=bool, required=False, default=False , help="Live record or Tracks playback record")
    arg_parser.add_argument('--start-time', action='store', type=str, required=False, default='20240423T114200', help="playback_start-time")
    arg_parser.add_argument('--end-time', action='store', type=int, required=False, default=5, help="playback_end-time in minutes")
    arg_parser.add_argument('--out_dir', action='store', type=str, required=False, default=datetime.now().strftime("%Y-%m-%d"), help="save_video_dir")

    return arg_parser.parse_args()


def rtsp_record(cam_username, cam_pass, ip, num, desired_fps, save_video, live, start_time, end_time, out_dir):
    # Construct RTSP URL based on whether it's live or playback
    if live:
        RTSP_URL = f'rtsp://{cam_username}:{cam_pass}@{ip}/ISAPI/Streaming/channels/{num}01'
    else:
        RTSP_URL = f'rtsp://{cam_username}:{cam_pass}@{ip}/ISAPI/Streaming/tracks/{num}01?starttime={start_time}Z'

    print(f"RTSP URL: {RTSP_URL}")

    # Set RTSP options
    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;tcp'
    #os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"]="video_codec;h264_cuvid"

    # Start capturing the RTSP stream
    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print('Cannot open RTSP stream.')
        return

    # Create output directory structure
    to_date = datetime.now().strftime("%Y_%m_%d")
    full_out_dir = os.path.join(out_dir, to_date)
    os.makedirs(full_out_dir, exist_ok=True)

    # Setup video writer
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    
    video_filename = f"{datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}_cam_{num}.mp4"
    video_filepath = os.path.join(full_out_dir, video_filename)
    video_codec = cv2.VideoWriter_fourcc(*'XVID')
    video_output = cv2.VideoWriter(video_filepath, video_codec, desired_fps, (frame_width, frame_height))

    print("[INFO]: RTSP Streaming Started.....")

    # Initialize frame timing and counting
    start = datetime.now()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if ret:
            frame_count += 1
            now = datetime.now()
            elapsed_time = (now - start).total_seconds()

            actual_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            frame_skip_ratio = actual_fps / desired_fps if desired_fps > 0 else 1

            if save_video and frame_skip_ratio > 0 and frame_count % int(max(1, frame_skip_ratio)) == 0:
                video_output.write(frame)
                print(f"[INFO]: Saving video frame {frame_count} at {desired_fps} fps....cam {num}")

            if cv2.waitKey(1) & 0xFF == ord('q') or (elapsed_time >= end_time*60):    # Stop recording after end_time minutes = 5 minutes by default
                print("\n [INFO]: Stopping recording...")
                break
        else:
            break

    cap.release()
    video_output.release()
    cv2.destroyAllWindows()
    print('All videos saved successfully.!')


if __name__ =='__main__':
    args = get_parser()

    camera_list =list(range(args.cam_list[0] ,args.cam_list[1]+1))
    print("List of cameras for recording...", camera_list)
    thread_list = []

    for i in range(len(camera_list)):
        thread = threading.Thread(target=rtsp_record,args=(args.cam_username, args.cam_pass, args.ip, camera_list[i], args.fps, args.save_video, args.live, args.start_time, args.end_time, args.out_dir),daemon=False)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()
