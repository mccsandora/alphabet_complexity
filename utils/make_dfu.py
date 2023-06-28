import os
from utils.unicode_utils import create_df_unicode, code_type, make_picture_twotry, is_box
from utils.script_utils import script_type
from utils.font_utils import get_preferred_font
from tqdm.auto import tqdm
tqdm.pandas()

def make_dfu():
    df_unicode = create_df_unicode()

    dfu=df_unicode[df_unicode.code.apply(code_type)=='Writing Symbol'].reset_index(drop=True)

    dfu['script'] = dfu.apply(script_type,axis=1)
    print('Deleting',(dfu.script=='None').sum(),
          'rows where script was not found. On inspection, these characters are not linguistic.')
    print()
    dfu = dfu[dfu.script!='None']
    
    dfu['preferred_font'] = dfu.apply(get_preferred_font,axis=1)

    print('Scripts with no available fonts:')
    print(dfu[dfu.preferred_font=='No available font'].script.value_counts())
    print()
    print('Scripts for codes with no matching fonts:')
    print(dfu[dfu.preferred_font=='?'].script.value_counts())
    print()

    missing_fonts=[]
    for f in dfu.preferred_font.unique():
        if not os.path.exists(f):
            if f not in ['?','No available font']:
                missing_fonts.append(f)

    print('Fonts that still need to be downloaded:')
    print('\n'.join(missing_fonts))
    mf = dfu.preferred_font.isin(missing_fonts+['?','No available font'])
    print('Deleting',mf.sum(),'rows with no font support.')
    dfu = dfu[~mf]
    
    print('Creating pictures')
    dfu['picture'] = dfu.progress_apply(lambda D:
                        make_picture_twotry(D.code,D.preferred_font),
                                   axis=1)
    print('Checking whether pictures are boxes')
    ib = dfu.picture.progress_apply(is_box)
    print('Found',ib.sum(),'boxes')
    dfu = dfu[~ib]
    print('Final df has',len(dfu),'characters from',dfu.script.nunique(),'different scripts.')
    return dfu.reset_index(drop=True)