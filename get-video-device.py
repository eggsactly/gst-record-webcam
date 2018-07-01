#!/usr/bin/python 

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

# This program is called like this
# v4l2-ctl --list-devices | ./get-video-device.py usb-0000:00:14.0-2.3 
# it will return the v4l2 device for the given usb bus index

import sys

inputString = ""

for line in sys.stdin:
    inputString = inputString + line + "\n"


inputLength = len(inputString)

    
substr = inputString[inputString.find(sys.argv[1]) + len(sys.argv[1]):]
substr = substr[substr.find("\n") + len("\n"):]
substr = substr[:substr.find("\n", len("\n"))]

print substr.strip()


