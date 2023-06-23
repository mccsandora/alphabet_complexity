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

    
def make_picture(code,ttf,font_size=200,size=500):
    """
    Creates picture of character
    Inputs:
        code: hex representation of unicode character
        ttf: location of .ttf file for a font
    Outputs:
        picture: 2d numpy array
    """
    image = Image.new('RGB', (size,size))

    draw = ImageDraw.Draw(image) 
    draw.text((int(size/2),int(size/2)), 
              u(code), 
              font=ImageFont.truetype(ttf, font_size))
    picture = np.mean(255-np.array(image),axis=-1)/255
    picture = remove_ones(picture)
    picture = padd(picture)
    return picture

def remove_ones(arr):
    """
    Removes rows and columns of a 2D numpy array that only contain ones, unless there is a different value in the adjacent row or column.
    Inputs:
        arr: 2D numpy array
    Outputs:
        new_arr: 2D numpy array with specified rows and columns removed
    """
    rows_to_keep = []
    cols_to_keep = []
    
    for i in range(arr.shape[0]):
        if np.all(arr[i,:] == 1):
            if i > 0 and not np.all(arr[i-1,:] == 1):
                rows_to_keep.append(i)
            elif i < arr.shape[0]-1 and not np.all(arr[i+1,:] == 1):
                rows_to_keep.append(i)
        else:
            rows_to_keep.append(i)
            
    for j in range(arr.shape[1]):
        if np.all(arr[:,j] == 1):
            if j > 0 and not np.all(arr[:,j-1] == 1):
                cols_to_keep.append(j)
            elif j < arr.shape[1]-1 and not np.all(arr[:,j+1] == 1):
                cols_to_keep.append(j)
        else:
            cols_to_keep.append(j)
            
    new_arr = arr[np.ix_(rows_to_keep, cols_to_keep)]
    
    return new_arr


def padd(picture,k=10):
    w,h = picture.shape
    h += 2*k
    picture = np.hstack([np.ones((w,k)),
               picture,np.ones((w,k))])
    picture = np.vstack([np.ones((k,h)),
               picture,np.ones((k,h))])
    return picture