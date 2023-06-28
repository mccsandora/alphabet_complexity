from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd
import re


def scriptcomp(variants = True):
    """
    variants = True returns a list that includes all variant names from Anna's list 
    (since some of the scripts would have a base name, and then other versions) in the merge
    variants = False returns just a list of the base name scripts from both lists merged together
    """
    scripts = list(pd.read_csv('data/scriptlist.csv').Script)
    ascripts = pd.read_excel('data/Graphic Complexity Script Data.xlsx').to_dict('list')
    alist = ascripts['EnglishName']
    alist = [k.upper() for k in alist]
    if variants == False:
        matchscr = [get_script(i) for i in alist]
        a_only = np.asarray(alist)[np.where(np.asarray(matchscr) == 'None')[0]]

        print('Length of Anna\'s Scripts : ' + str(len(alist)))
        print('Matching Script Count : ' + str(len(np.unique(matchscr))-1))
        print('Length of Extra Scripts in Anna\'s : ' + str(len(np.where(np.asarray(matchscr) == 'None')[0])))
        
        return np.concatenate((np.asarray(scripts, dtype = object), a_only))
    else:
        scripts = set(scripts)
        alist = set(alist)
        newscr = alist - scripts
        allscripts = list(scripts) + list(newscr)
        allscripts.sort(key=lambda x: -len(x))
        return allscripts
    

def get_script(note):
    
    scr = 'None'
    for s in scripts:
        try:
            scr = re.search(r'(?:^|(?<= ))' + s + '(?:(?= )|$)', note)[0]
        except:
            pass
    return scr

def create_scriptranges():
    df_gcsd = pd.read_excel('data/Graphic Complexity Script Data.xlsx').fillna('')

    scriptranges=[]
    for d,D in df_gcsd.iterrows():
        try:
            ranges = D.Range
            if len(ranges.strip())>0:
                ranges = ranges.replace(';',',').split(', ')
                en = D.EnglishName
                for r in ranges:
                    if 'excl' not in r:
                        if '-' in r:
                            rs = r.split('-')
                            scriptranges.append(('0x'+rs[0],'0x'+rs[1],en))
                        else:
                            scriptranges.append(('0x'+r,'0x'+r,en))
        except Exception as e:
            print(e,ranges)
    
    return scriptranges

scripts = scriptcomp()
scriptranges = create_scriptranges()

def script_type(D):
    """
    Determines code type of unicode code.
    """
    script = get_script(D.note)
    if script == 'None':
        u = '0x'+D.code
        for a,b,c in scriptranges:
            if a<=u<=b:
                return c
    return script