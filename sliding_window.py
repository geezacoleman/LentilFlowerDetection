
# returns a new part of the image based on an input, stepsize and window size
# check out Pyimagesearch for the full tutorial on sliding windows and pyramids. This has been adapted from there.
def sliding_window(image, stepSizeW, stepSizeH, windowSize):
    window_id = 0
    for y in range(0, image.shape[0], stepSizeH):
        for x in range(0, image.shape[1], stepSizeW):
            window_id += 1
            yield (window_id, x, y, image[y:y + windowSize[1], x:x + windowSize[0]])
