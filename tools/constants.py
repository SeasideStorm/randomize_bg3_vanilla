'''
For organization, all the various constants that are used throughout the
program are stored here, to be called later. 

'''
import pandas as pd
from pathlib import Path
import ast


ALL_SKILLS = ['Athletics',
            'Acrobatics','Sleight of Hand','Stealth',
            'Arcana','History','Investigation','Nature','Religion',
            'Animal Handling','Insight','Medicine','Perception', 'Survival',
            'Deception','Intimidation','Performance','Persuasion']

ALIGNMENTS = ['LG','NG','CG',
              'LN','TN','CN',
              'LE','NE','CE']

BACKGROUNDS =['acolyte','charlatan','criminal','entertainer',
            'folk hero','guild artisan','haunted one','noble',
            'outlander','sage','soldier','urchin']

BACKGROUND_SKILLS = pd.DataFrame(data = [
    ['Insight','Religion'], ['Deception', 'Sleight of Hand'],['Deception','Stealth'],
    ['Acrobatics', 'Performance'], ['Animal Handling', 'Survival'],['Insight','Persuasion'],
    ['Medicine','Intimidation'],['History','Persuasion'],['Atheltics','Survival'],['Arcana','History'],
    ['Athletics','Intimidation'],['Sleight of Hand','Stealth']],index = BACKGROUNDS, columns=['Skill 1','Skill 2'])

CLASSES = ['Barbarian','Bard','Cleric','Druid','Fighter','Monk',
        'Paladin','Ranger','Rogue','Sorcerer','Warlock','Wizard']

DRACONIC_COLORS = ['Black','Blue','Brass','Bronze','Copper','Gold','Green','Red','Silver','White']

FEATS = ['Alert','Actor','Athlete','Charger','Crossbow Expert','Defensive Duelist','Dual Wielder',
            'Dungeon Delver','Durable','Elemental Adept','Great Weapon Master','Heavily Armored', 'Heavy Armor Master'
            'Lightly Armored','Lucky','Mage Slayer','Magic Initiate: Bard','Magic Initiate: Cleric',
            'Magic Initiate: Druid','Magic Initiate: Sorcerer','Magic Initiate: Warlock','Magic Initiate: Wizard',
            'Martial Adept','Medium Armor Master','Mobile','Moderately Armoured','Performer','Polearm Master','Resillient',
            'Ritual Caster','Savage Attacker','Sentinel','Sharpshooter','Shield Master','Skilled','Spell Sniper',
            'Tavern Brawler', 'Tough','War Caster', 'Weapon Master']

FIGHTING_STYLES = ['Archery','Defense','Dueling','Great Weapon Fighting','Protection','Two-Weapon Fighting']

GODS = ['Bahamut', 'Corellon Larethian','Eilistraee', 'Garl Glittergold', 'Gruumsh','Helm','Ilmater',
        'Kelemvor', 'Lathander','Lolth','Mielikki','Moradin','Mystra','Oghma','Selune','Talos','Tempus',
        'Tiamat','Tymora','Tyr','Yondalla']

POINT_COST = pd.DataFrame(data = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,7],[7,9]], columns= ['Increase','Cost'])

SUBCLASSES = [
    ['Berserker','Wild Magic','Wildheart','Giant'],
    ['Lore','Valour','Swords','Glamour'],
    ['Life','Light','Trickery','Knowledge','Nature','Tempest','War','Death'],
    ['Land','Moon','Spores','Stars'],
    ['Battle Master','Eldritch Knight','Champion','Arcane Archer'],
    ['Four Elements','Open Hand','Shadow','Drunken Master'],
    ['Ancients','Devotion','Vengence','Crown'],
    ['Hunter','Beast Master','Gloom Stalker','Swarmkeeper'],
    ['Thief','Arcane Trickster','Assassin','Swashbuckler'],
    ['Wild Magic','Draconic Bloodline','Storm Sorcery','Shadow Magic'],
    ['Fiend','Great Old One','Archfey','Hexblade'],
    ['Abjuration','Evocation','Necromancy','Conjuration','Enchantment','Divination','Illusion','Transmutation','Bladesinging']
]

## Converter functions for the lists
rand_direct = Path(__file__).resolve().parents[1]
def convert_string_to_list(value):
   
    new_c = value.copy()

    for i in range(len(value)):
        if pd.isna(value.iloc[i]) == False:
            new_c.iloc[i] = ast.literal_eval(value.iloc[i])
        else:
            new_c.iloc[i] = []
    return (new_c)


spell_list_str= pd.read_csv(f'{rand_direct}/lists/bg3_spell_list_clean.csv',index_col=0)
spell_list_str.columns = [f"SL{x}" for x in spell_list_str.columns]
SPELL_LIST = spell_list_str.apply(lambda x: convert_string_to_list(x),axis = 0)


random_features_str = pd.read_csv(f'{rand_direct}/lists/bg3_choice_list_clean.csv',index_col=0)
random_features_str['Choice'] = convert_string_to_list(random_features_str.Choice)
RANDOM_FEATURES = random_features_str.copy()
