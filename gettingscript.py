from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd
import re



def get_script(note):
    scripts = pd.read_csv('data\scriptlist.csv')
    search = np.asarray(scripts['Script'])
    scr = 'None'
    for i in range(len(search)):
        try:
            scr = re.search(r'(?:^|(?<= ))' + str((search[i])) + '(?:(?= )|$)', note)[0]
        except:
            pass
    return scr
