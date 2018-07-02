#!/bin/bash 

# This file is part of gst-record-webcam.
#
#   gst-record-webcam is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   gst-record-webcam is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with gst-record-webcam.  If not, see <https://www.gnu.org/licenses/>.


MAIN_CAM=C920
SECOND_CAM=C270

MAIN_CAM_AUDIO=$(pacmd list-sources | ./get-pulse-index.py $MAIN_CAM)
SECOND_CAM_AUDIO=$(pacmd list-sources | ./get-pulse-index.py $SECOND_CAM)

MAIN_CAM_VIDEO=$(v4l2-ctl --list-devices | ./get-video-device.py $(pacmd list-sources | ./get-pulse-usb-device.py $MAIN_CAM))
SECOND_CAM_VIDEO=$(v4l2-ctl --list-devices | ./get-video-device.py $(pacmd list-sources | ./get-pulse-usb-device.py $SECOND_CAM))

OUTPUT_FILE_NAME=`date +%Y-%m-%d.%H:%M:%S`.mp4

AUDIO_QUEUE_SECONDS=1
AUDIO_RECORD_RATE=44100
AUDIO_DELAY_NS=1000000000

AUDIO_QUEUE_NS=$(expr 1000000000 \* $AUDIO_QUEUE_SECONDS)


echo "Main cam video:   $MAIN_CAM_VIDEO"
echo "Main cam audio:   $MAIN_CAM_AUDIO"

echo "Second cam video: $SECOND_CAM_VIDEO"
echo "Second cam audio: $SECOND_CAM_AUDIO"

echo "Filename:         $OUTPUT_FILE_NAME"

echo "AUDIO_QUEUE_NS:   $AUDIO_QUEUE_NS"

# Record video and audio from the main webcam 
gst-launch-1.0 -v \
    v4l2src device=$MAIN_CAM_VIDEO ! video/x-raw,width=1920,height=1080,framerate=30/1 ! queue ! mix. \
    v4l2src device=$SECOND_CAM_VIDEO ! video/x-raw, width=640,height=480,framerate=30/1 ! queue ! mix. \
    videomixer name=mix sink_1::xpos=1280 sink_1::ypos=600 sink_1::zorder=2 ! queue max-size-buffers=0 max-size-bytes=0 max-size-time=1000000000 ! queue ! videoconvert ! video/x-raw,width=1920,height=1080 ! tee name=t \
	t. ! queue ! videoscale ! video/x-raw,height=480 ! timeoverlay ! queue leaky=upstream ! autovideosink sync=false \
	t. ! queue ! vaapih264enc ! h264parse ! queue max-size-buffers=0 max-size-bytes=0 max-size-time=1000000000 ! mux. \
	pulsesrc device=$MAIN_CAM_AUDIO ! audioconvert ! audio/x-raw, rate=$AUDIO_RECORD_RATE ! queue max-size-buffers=0 max-size-bytes=0 max-size-time=$AUDIO_QUEUE_NS ! avenc_aac ! aacparse ! queue ! mux. \
	pulsesrc device=$SECOND_CAM_AUDIO ! audioconvert ! audio/x-raw, rate=$AUDIO_RECORD_RATE ! queue max-size-buffers=0 max-size-bytes=0 max-size-time=$AUDIO_QUEUE_NS ! avenc_aac ! aacparse ! queue ! mux. \
	mpegtsmux name=mux ! queue max-size-buffers=0 max-size-bytes=0 max-size-time=0 ! filesink location=$OUTPUT_FILE_NAME

