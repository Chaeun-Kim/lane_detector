# Finding Lane Lines on the Road

Self-Driving Car Engineer Nanodegree Project 1

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)
[original]: ./data/images/solidYellowCurve.jpg "Original"
[grayscale]: ./data/images/blur_grayscale.jpg "Gray-scaled (blurring applied)"
[canny]: ./data/images/canny_edge.jpg "Canny edge detection"
[hough_no_extent]: ./data/images/hough_no_extent.jpg "Hough without extension"
[hough]: ./data/images/hough_transformed.jpg "Hough transformed"
[result]: ./data/test_images_output/solidYellowCurve.jpg "Hough transformed"

---

## Contents

* `/data` - a directory consisted of test image/video files and test outputs
* `/lib` - a library directory with `helper.py`
	* `helper.py` - helper functions
* `detector.py` - main script which will detect road lanes on images/videos

## Running the lane detector

Clone this repo, and simply run the following commands at the root

* `pip install -r requirements.txt`
* `python detector.py`


## Reflection

### Pipeline Overview

1. Preprocess the image
	* convert the image to grayscale
	* blur the grayscale image using Gaussian function
2. Detect all the edges in the grayscale image using Canny algorithm
3. Ignore the edges outside of the region of interest
4. Detect relevant line from the edges
5. Draw out the relevant lines (lanes we care about) on the original image

#### Preprocessing 

![alt text][original]

Given the above image, the pipeline will try to detect the most relevant lanes on the road. For this particular case, those lanes would be the yellow lane on the left and the nearest white lanes.

Before the pipeline detects lines on an image, it will convert the image to grayscale. Doing that amplifies the contrast of colors of lanes on the road, and helps us use less computing power with less colors on each pixel.

We then use the Gaussian function to blur out the grayscale image to reduce noise. The result looks like below.

![alt text][grayscale]

#### Canny Algorithm

With the blurred grayscale image, the pipeline uses Canny algorithm to detect all the edges on the image, including edges of the cars, lanes, and all surroundings.

Simply put, Canny algorithm will detect pixels with rapid changes in gradient as edges.

Not shown in the image below, but in general, the lanes we most care about are always going to within certain boundaries of the image. The pipeline will only consider the edges in the region from now on. 

![alt text][canny]

#### Hough Transform

Now with the edges, we find lanes using Hough transform. 

Using the edges as points in cartesian coordinates, the pipeline will detect the best fit lines for those points using Hough transform. We can consider the detected lines as lanes.

However, if the lane was a dotted lane, like the white dotted lane on the right side of the image, the detected line might also be broken like below.

![alt text][hough_no_extent]

To reduce this noise, I first split the dected lines into left/right lane by checking the slope of each line. If the slope was negative that means the line is probably the left lane, and if positive right lane (the origin point [0,0] in images is top left corner).

Then I am averaging all of left/right lines and make one single line.

![alt text][hough]

Then draw them on to the original image

![alt text][result]


### Potential Shortcomings

This lane detector would not work very well under certain circumstances:
* Not sunny weather; rainy, snowy, stormy, etc...
* Roads with a lot of shadow
* Roads that are not just plain black cement

The dectector is also not very performant. It probably is too slow to be used in real-life situations.

### Possible Improvements

Currently we use the image in RGB color space. But I think we can try using different color space to better contrast lanes from the road and reduce noise further. Not sure totally sure how to improve on the performance, but I belive some processing could be skipped if certain condition (i.e. continuation of similar road condition?) is met.
