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

#variants = True returns a list that includes all variant names from Anna's list (since some of the scripts would have a base name, and then other versions) in the merge
#variants = False returns just a list of the base name scripts from both lists merged together

def scriptcomp(variants = True):
    scripts = list(pd.read_csv('data/scriptlist.csv').Script)
    ascripts = pd.read_csv('data/annascripts.csv').to_dict('list')
    alist = ascripts['EnglishName']
    alist = [k.upper() for k in alist]
    if variants == False:
        matchscr = [get_script(i) for i in annalist]
        a_only = np.asarray(annalist)[np.where(np.asarray(matchscr) == 'None')[0]]

        print('Length of Anna\'s Scripts : ' + str(len(annalist)))
        print('Matching Script Count : ' + str(len(np.unique(matchscr))-1))
        print('Length of Extra Scripts in Anna\'s : ' + str(len(np.where(np.asarray(matchscr) == 'None')[0])))
        
        return np.concatenate((np.asarray(scripts, dtype = object), a_only))
    else:
        scripts = set(scripts)
        alist = set(alist)
        newscr = alist - scripts
        return list(scripts) + list(newscr)
