import glob
import pandas as pd
from fontTools.ttLib import TTFont

fonts = glob.glob('data/ttfs/*.ttf')
fonts = [(f,len(TTFont(f).getBestCmap())) for f in fonts]
fonts.sort(key=lambda x: -x[1])
fonts = [f[0] for f in fonts]


df_gcsd = pd.read_excel('data/Graphic Complexity Script Data.xlsx')
lang2font = dict(zip(df_gcsd.EnglishName.apply(lambda x: x.lower()),
        df_gcsd.Font.fillna('No available font')))
lang2font = {k:'data/ttfs/'+v if '.' in v else v 
 for k,v in lang2font.items()}


code2font=dict()
for f in fonts:
    font = TTFont(f)
    code_support = font.getBestCmap()
    for c in code_support:
        code2font[c] = code2font.get(c,[])+[f]
        
        
def get_preferred_font(D):
    i = int(D.code,16)
    l = D.script.lower()
    if i in code2font:
        return code2font[i][0]
    if l in lang2font:
        return lang2font[l]
    return '?'