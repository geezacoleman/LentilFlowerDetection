from trackbar_mgmt import colour_mask, create_trackbars
from sliding_window import sliding_window
import imutils
import json
import cv2
import os

######## ENTER PARAMETERS HERE ##########
IMAGE_PATH = "tares-lentils_brighter.jpg" # path to the input image
SAVE_NAME = "exB_hsv_bright.jpg" # save name for output
SLIDERS = False # toggle the slider adjustment for thresholds
TOTAL_COUNT = 0
#########################################

# if a json file with the saved parameters exists load it
if os.path.exists("parameters.json"):
    with open("parameters.json", 'r') as f:
        paramsDict = json.load(f)
        print(paramsDict)
    print("[INFO] Loaded parameters from file...")
# else create a new one
else:
    paramsDict = {"ch1Min": 0, "ch1Max": 179,
                  "ch2Min": 0, "ch2Max": 55,
                  "ch3Min": 65, "ch3Max": 170}
    print("[INFO] No file found, using default parameters...")

# create the window/trackbars
cv2.namedWindow("Output", cv2.WINDOW_AUTOSIZE)
segmentationWindow = 'Segmentation Params'
cv2.namedWindow(segmentationWindow)
create_trackbars(segmentationWindow, paramsDict)
cv2.waitKey(10000)

# read the image, resize
image = cv2.imread(IMAGE_PATH)
image = imutils.resize(image, width=1200)

# split the image into channels and create the exBR composite image, removing the green channel.
# Result is converted to HSV
b, g, r = cv2.split(image)
merged = cv2.merge((b, b, r))
hsv = cv2.cvtColor(merged, cv2.COLOR_BGR2HSV)
display = image.copy()

# set the sliding window parameters
STEPH = int(image.shape[0] / 10)
WINH = int(image.shape[0] / 10)
STEPW = int(image.shape[1] / 10)
WINW = int(image.shape[1] / 10)

# create sliding windows
for (winID, x, y, imageOut) in sliding_window(hsv, stepSizeH=STEPH, stepSizeW=STEPW, windowSize=(WINW, WINH)):
    cv2.rectangle(display, (x, y), (x + WINW, y + WINH), (0, 255, 0), 2)
    if imageOut.shape[0] != WINH or imageOut.shape[1] != WINW:
        continue

    # if SLIDERS is TRUE open up the masked image and allow user input to change threshold values on sliders
    while SLIDERS:
        thresh, paramsDict = colour_mask(imageOut, segmentationWindow)
        masked = cv2.bitwise_and(imageOut, imageOut, mask=thresh)
        cv2.imshow("slider", masked)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            # save the parameters to file for next time
            with open('parameters.json', 'w+') as f:
                json.dump(paramsDict, f, indent=4)
                print("[INFO] Parameters saved")
            break

    # run the thresholding and masking
    thresh, paramsDict = colour_mask(imageOut, segmentationWindow)
    masked = cv2.bitwise_and(imageOut, imageOut, mask=thresh)

    # find the contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        # filter based on total area
        if cv2.contourArea(c) > 2:
            (Cx, Cy), radius = cv2.minEnclosingCircle(c)
            cv2.circle(display, (int(Cx + x), int(Cy + y)), int(radius), (0, 0, 255), 1)
            TOTAL_COUNT += 1
    tempImage = display.copy()

    # add the count of flowers identfied
    cv2.putText(tempImage, "{} flowers detected".format(TOTAL_COUNT),
                (int(display.shape[1] / 2) - 140, int(display.shape[0] / 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 20, 20), 2)
    cv2.imshow("Output", tempImage)
    cv2.waitKey(200)

# Write the total number of weeds detected on the image and then save it to file
cv2.putText(display, "{} flowers detected".format(TOTAL_COUNT), (int(display.shape[1] / 2) - 140, int(display.shape[0] / 10)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 20, 20), 2)
cv2.imshow("Output", display)
cv2.waitKey(3000)
cv2.imwrite(SAVE_NAME, display)
cv2.destroyAllWindows()
