import cv2
import argparse
import os



parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str, default='./', help='file/dir/URL/glob')
arg = parser.parse_args()

# Read the video from specified path
cam = cv2.VideoCapture(arg.source+f"*.mp4")

try:
	
	# creating a folder named data
	if not os.path.exists('video_images'):
		os.makedirs('video_images')

# if not created then raise error
except OSError:
	print ('Error: Creating directory of data')

# frame
currentframe = 0

while(True):
	
	# reading from frame
	ret,frame = cam.read()

	if ret:
		# if video is still left continue creating images
		name = './video_images/frame' + str(currentframe) + '.jpg'
		print ('Creating...' + name)

		# writing the extracted images
		cv2.imwrite(name, frame)

		# increasing counter so that it will
		# show how many frames are created
		currentframe += 1
	else:
		break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
