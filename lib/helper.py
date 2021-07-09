import os
import cv2
import math
import numpy as np

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  
    
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.
    
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)

    image_height = img.shape[0]
    line_img = np.zeros((image_height, img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, _get_best_fit_lines(lines, img.shape), thickness=5)

    return line_img

def _get_best_fit_lines(lines, shape):
    """
    'lines' is an array containig points for hough lines of the image.
        [ [[x1,y1,x2,y2]], [[x1,y1,x2,y2]], [[x1,y1,x2,y2]] ]

    Decide whether each set of points forms a line on the left/right side
    of the image by getting their slopes. Negative slope means the line
    is on the left side of the image (considering that the origin [0,0] 
    is on the top left corner)

    Then, get the average of the left/right lines.
    Average line = (avg slope of lines)*X + (avg y intercepts of lines)
    """
    right_lines = [
        np.polyfit([x1,x2], [y1,y2], 1)
        for line in lines
        for x1,y1,x2,y2 in line
        if ((y2-y1)/(x2-x1)) > 0 and min(x1, x2) > shape[1]/2
    ]
    left_lines = [
        np.polyfit([x1,x2], [y1,y2], 1)
        for line in lines
        for x1,y1,x2,y2 in line
        if ((y2-y1)/(x2-x1)) < 0 and max(x1, x2) < shape[1]/2
    ]

    left_slope, left_intercept = _get_avg_slope_and_intercept(left_lines)
    right_slope, right_intercept = _get_avg_slope_and_intercept(right_lines)

    left_lane_points = _get_points_in_line(shape, left_slope, left_intercept)
    right_lane_points = _get_points_in_line(shape, right_slope, right_intercept)

    return np.array([
        [left_lane_points],
        [right_lane_points]
    ], dtype=np.int32)

def _get_avg_slope_and_intercept(lines):
    slope = 0
    y_intercept = 0
    for line in lines:
        slope += line[0]
        y_intercept += line[1]

    num_lines = len(lines)
    return slope/num_lines, y_intercept/num_lines

def _get_points_in_line(shape, slope, y_intercept):
    y1, y2 = shape[0], shape[0]/1.68
    x1 = (y1 - y_intercept) / slope
    x2 = (y2 - y_intercept) / slope

    return [x1, y1, x2, y2]

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)

def save_img(img, path, filename):
    if not os.path.exists(path):
        os.makedirs(path)

    return cv2.imwrite(f'{path}/{filename}', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

def save_video(clip, path, filename, audio=False):
    if not os.path.exists(path):
        os.makedirs(path)

    clip.write_videofile(f'{path}/{filename}', audio=audio)
    