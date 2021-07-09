# Finding Lane Lines on the Road

Self-Driving Car Engineer Nanodegree Project 1

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./data/images/solidYellowCurve.jpg "Original"

[image1]: ./data/images/blur_grayscale.jpg "Gray-scaled (blurring applied)"

[image1]: ./data/images/canny_edge.jpg "Canny edge detection"

[image1]: ./data/images/hough_transformed.jpg "Hough transformed"

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

My pipeline consisted of 5 steps. First, I converted the images to grayscale, then I .... 

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...