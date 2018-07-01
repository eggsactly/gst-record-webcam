#!/usr/bin/python 

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


