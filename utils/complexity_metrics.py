import numpy as np
from scipy.ndimage import distance_transform_edt


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
    Computes the symmetry of the image     
    """

    lr_symm = 1 - np.mean(np.abs(picture - picture[:, ::-1]))
    tb_symm = 1 - np.mean(np.abs(picture - picture[::-1, :]))
    return lr_symm, tb_symm



def check_symmetry2(picture, type = "lr"):
    if type == "lr":
        symm = picture[:,::-1]
        return 1 - np.mean(np.abs(picture - symm))
    else:
        symm = picture.T[:,::-1]
        return 1 - np.mean(np.abs(picture - symm))

