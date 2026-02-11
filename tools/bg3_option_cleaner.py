import pandas as pd

from collections import OrderedDict
from pathlib import Path

## Should not need to be re-run, here for reproducability. 
## Cleans up some of the excel files for use in the main program,

rand_direct = Path(__file__).resolve().parents[1]

def spell_list():
    ## Read list in
    
    spell_list_raw = pd.read_csv(f'{rand_direct}/lists/bg3_spells_raw.csv')

    ## Clean the duplicates from wikipasting
    spell_list_raw['Name'] = spell_list_raw['Name'].astype(str).apply(
        lambda x: " ".join(list(OrderedDict.fromkeys(x.split(' ')))))

    ## Aggregate
    spell_list_agg = spell_list_raw.groupby(['Class','Level']).agg({'Name':'unique'})
    spell_list_agg.reset_index(inplace=True)
    spell_list_agg['Name'].str.split(" ")

    ## To list
    spell_list_agg['Name'] = [list(x) for x in spell_list_agg['Name']]
    spell_list_clean = spell_list_agg.pivot(index='Class',columns='Level',values='Name')

    spell_list_clean.to_csv(f'{rand_direct}/lists/bg3_spell_list_clean.csv')

def misc_list():
    ## Read list in
    misc_list_raw = pd.read_csv(f'{rand_direct}/lists/misc_choice_list_raw.csv')
    

    ## Clean the duplicates from wikipasting
    misc_list_raw['Choice'] = misc_list_raw['Choice'].astype(str).apply(
        lambda x: " ".join(list(OrderedDict.fromkeys(x.split(' ')))))

    misc_list_agg = misc_list_raw.groupby(['Feature']).agg({'Choice':'unique'})
    misc_list_agg.reset_index(inplace=True)
    misc_list_agg['Choice'].str.split(" ")

    ## To list
    misc_list_agg['Choice'] = [list(x) for x in misc_list_agg['Choice']]
    
    misc_list_agg.to_csv(f'{rand_direct}/lists/bg3_choice_list_clean.csv')

spell_list()
misc_list()