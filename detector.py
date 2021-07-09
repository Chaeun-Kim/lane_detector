import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from moviepy.editor import VideoFileClip

from lib.helper import (
	grayscale, canny, gaussian_blur, region_of_interest, 
	draw_lines, hough_lines, weighted_img, save_img, save_video
)

GAUSSIAN_KERNEL = 5
CANNY_LOW_THRESHOLD = 50
CANNY_HI_THRESHOLD = 150

DATA_DIR = f'{os.getcwd()}/data'

IMAGE_DIR = f'{DATA_DIR}/images'
OUT_IMAGE_DIR = f'{DATA_DIR}/test_images_output'

VIDEO_DIR = f'{DATA_DIR}/videos'
OUT_VIDEO_DIR = f'{DATA_DIR}/test_videos_output'

def process_image(image):
	"""
	Find lanes on the given image
	"""
	height = image.shape[0]
	width = image.shape[1]

	# make the image gray
	gray_image = grayscale(image)
	# apply gaussian noise filtering
	blur_gray = gaussian_blur(gray_image, GAUSSIAN_KERNEL)

	# Canny transform to detect lines
	lines = canny(blur_gray, CANNY_LOW_THRESHOLD, CANNY_HI_THRESHOLD)

	# points of the important polygon area
	masking_region = np.array([[
		[0,height],
		[width/2,height/1.68],
		[width,height]
	]], dtype=np.int32)
	masked_lines = region_of_interest(lines, masking_region)

	# get hough transformed lines
	detected_lines = hough_lines(masked_lines, 2, np.pi/180, 50, 5, 10)

	# return the orginal image with hough lines drawn
	return weighted_img(detected_lines, image)

def find_lanes_on_images():
	"""
	Go through images in the /data/images/ directory and
	find the lanes in each image and save off the output
	"""
	for image_file in os.listdir(IMAGE_DIR)[-1:]:
		image = mpimg.imread(f'{IMAGE_DIR}/{image_file}')

		result = process_image(image)
		if not save_img(result, OUT_IMAGE_DIR, image_file):
			print("Fail to save the image.")
			sys.exit()

def find_lanes_on_videos():
	"""
	Go through videos in the /data/videos/ directory and
	trace the lanes in each video and save off the output
	"""
	for video in os.listdir(VIDEO_DIR)[-1:]:
		clip = VideoFileClip(f'{VIDEO_DIR}/{video}')
		processed_clip = clip.fl_image(process_image)
		save_video(processed_clip, OUT_VIDEO_DIR, video)

# First part of Project 1 - lanes on images
find_lanes_on_images()
# Second part of Project 1 - lanes on a videos
find_lanes_on_videos()
