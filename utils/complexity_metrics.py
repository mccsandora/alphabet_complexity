import numpy as np

def pixel_count_complexity(picture):
    """
    Computes fraction of black pixels in image
    """
    return np.mean(picture)


def check_symmetry(picture):
    symm = 0
    for j in range(len(picture)):   
        for i in range(int(np.floor(len(picture[0])/2))):
            if picture[j][i] == picture[j][-i]:
                   symm += 1
            else: symm += 0
    try: symm /= (len(picture)*(len(picture[0])/2))
    except: symm = 0
    return symm
