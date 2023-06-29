import numpy as np


def pixel_count_complexity(picture):
    """
    Computes fraction of black pixels in image
    """
    return np.mean(picture)


def check_symmetry(picture):
    left_right_sym = 0
    top_bottom_sym = 0

    # check left-right symmetry
    for j in range(len(picture)):
        for i in range(int(np.floor(len(picture[0]) / 2))):
            if picture[j][i] == picture[j][-i]:
                left_right_sym += 1

    # check top-bottom symmetry
    for j in range(int(np.floor(len(picture) / 2))):
        for i in range(len(picture[0])):
            if picture[j][i] == picture[-j][i]:
                top_bottom_sym += 1

    # get symmetry ratios
    left_right_total = len(picture) * np.floor(len(picture[0]) / 2)
    top_bottom_total = np.floor(len(picture) / 2) * len(picture[0])

    sym_lr_ratio = left_right_sym / left_right_total if left_right_total > 0 else 0
    sym_tb_ratio = top_bottom_sym / top_bottom_total if top_bottom_total > 0 else 0

    return sym_lr_ratio, sym_tb_ratio
