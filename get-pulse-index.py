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
# pacmd list-sources | ./get-pulse-index.py C270 
# it will return the pulse audio index value for the microphone on the C270 
# webcam

import sys

inputString = ""

for line in sys.stdin:
    inputString = inputString + line + "\n"

indexKey = "index: "
productKey = "device.product.name = "

inputLength = len(inputString)

i = 0

indexStart = inputString.find(indexKey, i)
# This if statement prevents us from going into an infinite loop
if indexStart == -1:
    i = inputLength
indexStart = indexStart + len(indexKey)
indexEnd   = inputString.find("\n", indexStart)

while i < inputLength:
    indexValue = inputString[indexStart:indexEnd]
    i = indexEnd + len("\n")
    nextIndexStart = inputString.find(indexKey, i)
    if nextIndexStart == -1:
        nextIndexStart = inputLength
    
    productStart = inputString.find(productKey, i, nextIndexStart)
    if productStart == -1:
        productStart = 0
        productEnd   = 0
        productValue = ""
    else:
        productStart = productStart + len(productKey)
        productEnd   = inputString.find("\n", productStart)
        productValue = inputString[productStart:productEnd]

    # Print out the index value and leave the program
    if sys.argv[1] in productValue:
        print indexValue
        break

    # Get the next loops index 
    indexStart = inputString.find(indexKey, i)
    # This if statement prevents us from going into an infinite loop
    if indexStart == -1:
        break
    indexStart = indexStart + len(indexKey)
    indexEnd   = inputString.find("\n", indexStart)


    

