# Lentil Flower Detection
A recent post on [Twitter](https://twitter.com/CropDoctor54/status/1303944641021005824) about detecting purple flowers in crop had me thinking how that might look in practice. So I put together this rough code that swaps the green channel for an additional blue channel and then uses the HSV colour space to threshold based on saturation and value.

### Colour Spaces
Colour spaces are methods for representing colours in different ways. The standard one you might be familiar with is Red Green Blue or RGB. Others include HSV (hue saturation value), [L*a*b*](https://en.wikipedia.org/wiki/CIELAB_color_space) and [Y'CbCr](https://en.wikipedia.org/wiki/YCbCr). In the end, a type of ExB (to pick out the purple flowers) worked quite well, splitting the RGB image into channels, then merging them back together as (B, B, R) to remove the green. Blue then became oversaturated and a subsequent transforation to HSV meant thresholding on saturation worked well.

There are a couple of mis detections in the darker regions. Initially I tried straight HSV, Lab and YCrCb colour spaces for thresholding, however, none had any decent performance.

This would likely fall down if conditions/lighting changed, so it's more of a coding exercise for my PhD than anything.

Some interesting colour space resources:
[PyImageSearch Colour Detection](https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/)
[Rubix Cube Colour Detection](https://www.learnopencv.com/color-spaces-in-opencv-cpp-python/)

or a fantastic video from Captain Disillusion on [colour](https://www.youtube.com/watch?v=FTKP0Y9MVus)

### Sliding Windows
The code for the sliding windows is adapted from Adrian Rosebrock's PyImageSearch tutorial on ["Sliding Windows for Object Detection with Python and OpenCV"](https://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/). I would highly recommend his tutorials and blog posts on all sorts of computer vision related material!

#### Reference
Adrian Rosebrock, Sliding Windows for Object Detection with Python and OpenCV, PyImageSearch, https://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/, accessed on 12 September 2020.
