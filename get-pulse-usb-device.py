#!/usr/bin/python 

# This program is called like this
# pacmd list-sources | ./pacmd-parse.py C270 
# it will return the pulse audio index value for the microphone on the C270 
# webcam

import sys

inputString = ""

for line in sys.stdin:
    inputString = inputString + line + "\n"

indexKey = "index: "
productKey = "device.product.name = "
usbKey = "alsa.long_card_name = "

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

    usbStart = inputString.find(usbKey, i, nextIndexStart)
    if usbStart == -1:
        usbproductStart = 0
        usbEnd   = 0
        usbValue = ""
    else:
        usbStart = usbStart + len(usbKey)
        usbEnd   = inputString.find("\n", usbStart)
        usbValue = inputString[usbStart:usbEnd]

    usbValue = usbValue[usbValue.find(" at ")+len(" at "):]
    usbValue = usbValue[:usbValue.find(" ")]
    usbValue = usbValue[:usbValue.find(",")]
    

    # Print out the index value and leave the program
    if sys.argv[1] in productValue:
        print usbValue
        break

    # Get the next loops index 
    indexStart = inputString.find(indexKey, i)
    # This if statement prevents us from going into an infinite loop
    if indexStart == -1:
        break
    indexStart = indexStart + len(indexKey)
    indexEnd   = inputString.find("\n", indexStart)


    

