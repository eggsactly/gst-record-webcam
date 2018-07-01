#!/bin/bash 

MAIN_CAM=C920
SECOND_CAM=C270

MAIN_CAM_AUDIO=$(pacmd list-sources | ./get-pulse-index.py $MAIN_CAM)
SECOND_CAM_AUDIO=$(pacmd list-sources | ./get-pulse-index.py $SECOND_CAM)

MAIN_CAM_VIDEO=$(v4l2-ctl --list-devices | ./get-video-device.py $(pacmd list-sources | ./get-pulse-usb-device.py $MAIN_CAM))
SECOND_CAM_VIDEO=$(v4l2-ctl --list-devices | ./get-video-device.py $(pacmd list-sources | ./get-pulse-usb-device.py $SECOND_CAM))

OUTPUT_FILE_NAME=`date +%Y-%m-%d.%H:%M:%S`.mp4

echo "Main cam video $MAIN_CAM_VIDEO"
echo "Main cam audio $MAIN_CAM_AUDIO"

echo "Second cam video $SECOND_CAM_VIDEO"
echo "Second cam audio $SECOND_CAM_AUDIO"

echo "Filename $OUTPUT_FILE_NAME"

# Record video and audio from the main webcam 
gst-launch-1.0 -v v4l2src device=$MAIN_CAM_VIDEO ! video/x-h264,width=1920,height=1080,framerate=30/1 ! tee name=t \
	t. ! queue ! vaapih264dec ! queue ! videoconvert ! videoscale ! video/x-raw,height=480 ! timeoverlay ! queue ! autovideosink \
	t. ! queue ! h264parse ! queue max-size-buffers=0 max-size-bytes=0 max-size-time=1000000000 ! mux. \
	pulsesrc device=$MAIN_CAM_AUDIO ! audioconvert ! queue ! avenc_aac ! mux. \
	mpegtsmux name=mux ! queue ! filesink location=$OUTPUT_FILE_NAME

