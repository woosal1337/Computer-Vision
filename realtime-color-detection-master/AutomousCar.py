import cv2
import math
import numpy as np
import sys
from matplotlib import pyplot as plt

def hist_match(source, template):
    """
    Adjust the pixel values of a grayscale image such that its histogram
    matches that of a target image

    Arguments:
    -----------
        source: np.ndarray
            Image to transform; the histogram is computed over the flattened
            array
        template: np.ndarray
            Template image; can have different dimensions to source
    Returns:
    -----------
        matched: np.ndarray
            The transformed output image
    """

    oldshape = source.shape
    source = source.ravel()
    template = template.ravel()

    # get the set of unique pixel values and their corresponding indices and
    # counts
    s_values, bin_idx, s_counts = np.unique(source, return_inverse=True,
                                            return_counts=True)
    t_values, t_counts = np.unique(template, return_counts=True)

    # take the cumsum of the counts and normalize by the number of pixels to
    # get the empirical cumulative distribution functions for the source and
    # template images (maps pixel value --> quantile)
    s_quantiles = np.cumsum(s_counts).astype(np.float64)
    s_quantiles /= s_quantiles[-1]
    t_quantiles = np.cumsum(t_counts).astype(np.float64)
    t_quantiles /= t_quantiles[-1]

    # interpolate linearly to find the pixel values in the template image
    # that correspond most closely to the quantiles in the source image
    interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)
    return interp_t_values[bin_idx].reshape(oldshape)

# Read original image
im_o = cv2.imread('/media/Lexar/color_transfer_data/5/frame10.png')
im = im_o
cv2.imshow('Org',im)
cv2.waitKey()

B = im[:,:, 0]
G = im[:,:, 1]
R = im[:,:, 2]

R= np.array(R).astype('float')
G= np.array(G).astype('float')
B= np.array(B).astype('float')

# Extract pixels that correspond to pure white R = 255,G = 255,B = 255
B_white = R[168, 351]
G_white = G[168, 351]
R_white = B[168, 351]

print (B_white)
print (G_white)
print (R_white)

# Compensate for the bias using normalization statistics
R_balanced = R / R_white
G_balanced = G / G_white
B_balanced = B / B_white

R_balanced[np.where(R_balanced > 1)] = 1
G_balanced[np.where(G_balanced > 1)] = 1
B_balanced[np.where(B_balanced > 1)] = 1

B_balanced=B_balanced * 255
G_balanced=G_balanced * 255
R_balanced=R_balanced * 255

B_balanced= np.array(B_balanced).astype('uint8')
G_balanced= np.array(G_balanced).astype('uint8')
R_balanced= np.array(R_balanced).astype('uint8')

im[:,:, 0] = (B_balanced)
im[:,:, 1] = (G_balanced)
im[:,:, 2] = (R_balanced)

# Notice saturation artifacts 
cv2.imshow('frame',im)
cv2.waitKey()

# Extract the Y plane in original image and match it to the transformed image 
im_o = cv2.cvtColor(im_o, cv2.COLOR_BGR2YCR_CB)
im_o_Y = im_o[:,:,0]

im = cv2.cvtColor(im, cv2.COLOR_BGR2YCR_CB)
im_Y = im[:,:,0]

matched_y = hist_match(im_o_Y, im_Y)
matched_y= np.array(matched_y).astype('uint8')
im[:,:,0] = matched_y

im_final = cv2.cvtColor(im, cv2.COLOR_YCR_CB2BGR)
cv2.imshow('frame',im_final)
cv2.waitKey()