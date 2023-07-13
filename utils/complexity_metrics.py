import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import distance_transform_edt
from scipy.signal import convolve


def pixel_count_complexity(picture):
    """
    Computes fraction of black pixels in image
    """
    return np.mean(picture)

def apply_distance_transform(image):
    """
    computes the distance transform of the image
    """
    distance_transform = distance_transform_edt(image)

    return distance_transform

def check_symmetry(picture):
    """
    Computes the symmetry of an image by performing 2D convolution.
    Compares black pixels with black pixels and white pixels with white pixels.
    """

    binary_picture = (picture>0).astype(int)
    # flip the image vertically and horizontally
    flipped_lr = binary_picture[:, ::-1]
    flipped_tb = binary_picture[::-1, :]

    # compute the convolution of the original and flipped images
    conv_lr = convolve2d(binary_picture, flipped_lr, mode='same', boundary='fill', fillvalue=0)
    conv_tb = convolve2d(binary_picture, flipped_tb, mode='same', boundary='fill', fillvalue=0)

    #find the maximum overlap and compute symmetry scores
    max_overlap_lr = np.max(conv_lr)
    max_overlap_tb = np.max(conv_tb)

    lr_symmetry = np.mean(conv_lr) / max_overlap_lr if max_overlap_lr > 0 else 0
    tb_symmetry = np.mean(conv_tb) / max_overlap_tb if max_overlap_tb > 0 else 0

    return lr_symmetry, tb_symmetry


def check_symmetry_1d(picture):
    """
    Computes the left-right and top-bottom symmetry of an image by performing 1D convolution.
    Compares black pixels with black pixels and white pixels with white pixels.
    """

    binary_picture = (picture > 0).astype(int)
    
    flipped_lr = binary_picture[::-1]
    flipped_tb = binary_picture[:, ::-1]

    conv_lr = convolve(binary_picture, flipped_lr, mode='same')
    conv_tb = convolve(binary_picture, flipped_tb, mode='same')

    max_overlap_lr = np.max(conv_lr)
    max_overlap_tb = np.max(conv_tb)

    lr_symmetry = np.mean(conv_lr) / max_overlap_lr if max_overlap_lr > 0 else 0
    tb_symmetry = np.mean(conv_tb) / max_overlap_tb if max_overlap_tb > 0 else 0

    return lr_symmetry, tb_symmetry


def check_symmetry2(picture, type = "lr"):
    if type == "lr":
        symm = picture[:,::-1]
        return 1 - np.mean(np.abs(picture - symm))
    else:
        symm = picture.T[:,::-1]
        return 1 - np.mean(np.abs(picture - symm))

def calculate_complexity(normalized_values):

    complexity_score = np.sum(normalized_values)
    return complexity_score
