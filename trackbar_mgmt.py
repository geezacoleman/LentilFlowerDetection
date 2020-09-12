import numpy as np
import cv2


def nothing(x):
    pass

def colour_mask(image, winName):
    ch1Min = cv2.getTrackbarPos('ch1Min', winName)
    ch1Max = cv2.getTrackbarPos('ch1Max', winName)
    ch2Min = cv2.getTrackbarPos('ch2Min', winName)
    ch2Max = cv2.getTrackbarPos('ch2Max', winName)
    ch3Min = cv2.getTrackbarPos('ch3Min', winName)
    ch3Max = cv2.getTrackbarPos('ch3Max', winName)

    lowerThresh = np.array([ch1Min, ch2Min, ch3Min])
    upperThresh = np.array([ch1Max, ch2Max, ch3Max])

    thresh = cv2.inRange(image, lowerThresh, upperThresh)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    paramsDict = {"ch1Min": ch1Min, "ch1Max": ch1Max,
                  "ch2Min": ch2Min, "ch2Max": ch2Max,
                  "ch3Min": ch3Min, "ch3Max": ch3Max}

    return thresh, paramsDict

def create_trackbars(winName, paramsDict):
    cv2.createTrackbar('ch1Min', winName, paramsDict['ch1Min'], 179, nothing)
    cv2.createTrackbar('ch1Max', winName, paramsDict['ch1Max'], 179, nothing)
    cv2.createTrackbar('ch2Min', winName, paramsDict['ch2Min'], 255, nothing)
    cv2.createTrackbar('ch2Max', winName, paramsDict['ch2Max'], 255, nothing)
    cv2.createTrackbar('ch3Min', winName, paramsDict['ch2Min'], 255, nothing)
    cv2.createTrackbar('ch3Max', winName, paramsDict['ch3Max'], 255, nothing)
