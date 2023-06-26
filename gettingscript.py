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

#returned array does not include variants of scripts mentioned in Anna's, just the base script name
def scriptcomp():
    scriptsdf = pd.read_csv('data/scriptlist.csv')
    scripts = list(scriptsdf.Script)
    annascriptsdf = pd.read_csv('data/annascripts.csv')
    annascr = annascriptsdf.to_dict('list')

    annalist = annascr['EnglishName']
    for i in range(len(annalist)):
        annalist[i] = annalist[i].upper() 

    matchscr = [get_script(i) for i in annalist]
    a_only = np.asarray(annalist)[np.where(np.asarray(matchscr) == 'None')[0]]

    print('Length of Anna\'s Scripts : ' + str(len(annalist)))
    print('Matching Script Count : ' + str(len(np.unique(matchscr))-1))
    print('Length of Extra Scripts in Anna\'s : ' + str(len(np.where(np.asarray(matchscr) == 'None')[0])))
    
    return np.concatenate((np.asarray(scripts, dtype = object), a_only))
