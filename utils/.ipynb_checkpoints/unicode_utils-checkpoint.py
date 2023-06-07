from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd

def create_df_unicode():
    """
    Parses unicode names list into pandas dataframe
    Data downloaded from https://www.unicode.org/Public/UCD/latest/ucd/
    """
    with open('data/unicode_names_list.txt','r') as f:
        unicode = f.read()

    unicode = unicode.split('\n')
    df_unicode = pd.DataFrame([u.split('\t') 
            for u in unicode if len(u)>0 and u[0] not in '\t;@'],
                columns=['code','note'])

    df_unicode = df_unicode[df_unicode.note.apply(lambda x: x[0]!='<')].reset_index(drop=True)
    df_unicode.note.apply(lambda x: x.split()[0]).value_counts().index.tolist()
    df_unicode['rep'] = df_unicode.code.apply(u)

    return df_unicode


def code_type(code):
    """
    Determines code type of unicode code.
    """
    u = '0x'+code
    for a,b,c in [('0x1F600', '0x1F64F', 'Emoticons'),
                  ('0x1F300', '0x1F5FF', 'Misc Symbols and Pictographs'),
                  ('0x1F680', '0x1F6FF', 'Transport and Map'),
                  ('0x2600', '0x26FF', 'Misc symbols'),
                  ('0x2700', '0x27BF', 'Dingbats'),
                  ('0xFE00', '0xFE0F', 'Variation Selectors'),
                  ('0x1F900', '0x1F9FF', 'Supplemental Symbols and Pictographs'),
                  ('0x1F1E6', '0x1F1FF', 'Flags')]:
        if a<=u<=b:
            return c
    return 'Writing Symbol'

def u(i):
    try:
        return chr(int(i, 16))
    except:
        return i

    
def get_language(note):
    """
    Extracts language from unicode note.
    Assumes first word of note is the language.
    """
    return note.split()[0]

    
def make_picture(code,ttf):
    """
    Creates picture of character
    Inputs:
        code: hex representation of unicode character
        ttf: location of .ttf file for a font
    Outputs:
        picture: 2d numpy array
    """
    image = Image.new('RGB', (100,100))

    draw = ImageDraw.Draw(image) 
    draw.text((50,50), 
              u(code), 
              font=ImageFont.truetype(ttf, 11))
    picture = np.mean(255-np.array(image),axis=-1)/255
    return picture
