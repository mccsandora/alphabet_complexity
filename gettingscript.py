from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd
import re



def get_script(note):
    txt = open("data/scrlist.txt", "r")
    search = txt.read()
    scr = 'None'
    try:
        scr = re.search(search, note)[0]
    except:
        pass
        
    return scr
