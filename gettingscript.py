from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd
import re


scripts = pd.read_csv('data/scriptlist.csv')
scripts = np.asarray(scripts['Script'])
    
    
def get_script(note):
    
    scr = 'None'
    for s in scripts:
        try:
            scr = re.search(r'(?:^|(?<= ))' + s + '(?:(?= )|$)', note)[0]
        except:
            pass
    return scr
