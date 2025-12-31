'''
To do: 
* Fighter - Warlock

* Add in gods

* Rerun option cleaner

* Add in third caster function
'''
import pandas as pd

from math import ceil
from numpy import random
from xhtml2pdf import pisa

from tools.constants import *

class randomize_char:
    def __init__(self):
        '''
        Initialization Function for the randomizer. This Creates the primary lists and tables that are
        filled.
        '''
        ## Character Sheet
        self.character_sheet = pd.DataFrame(index = ['Race','Background','Abilities','Starting Skills'] + [f'Level {i}' for i in range(1,13)]
                                    ,columns=['Selection','Random Features'])
        
        ## Ability Scores
        self.abillity_scores = pd.DataFrame(columns=['Score','Base','Free Bonus','Level 1'])
        self.abillity_scores['Score'] = ['STR','DEX','CON','INT','WIS','CHA']
        self.abillity_scores['Base'] = 8

        ## Skills Cataloging
        self.available_skills = ALL_SKILLS.copy()
        self.character_skills = []

        ## Feats Cataloging
        self.available_feats = FEATS.copy()
        self.character_feats = []

        ## Spells Cataloging
        self.available_spells = SPELL_LIST.loc[:,1]
        self.character_spells = pd.Series(index = SPELL_LIST.index)

        ## Cantrips Cataloging
        self.available_cantrips = SPELL_LIST.loc[:,"Cantrip"]
        self.character_cantrips = pd.Series(index = SPELL_LIST.index)

        ## Specific Lists ------------------------------

        ## Expertise
        self.character_expertise = []

        ## Fighting Styles
        self.available_fighting = FIGHTING_STYLES.copy()
        self.character_fightning = []

        ## Manoeuvres
        self.available_manoeuvres = RANDOM_FEATURES.loc[RANDOM_FEATURES['Feature'] == 'Manoeuvres','Choice'].explode()
        self.character_manoeuvres = []


    ###### Helpers --------------------------------------------------------------------------------------

    def get_spell_list(self,spellclass,lvl):
        '''
        The SPELL_LIST needs to be accessed enough where this is useful
        '''
        spell_list = SPELL_LIST.loc[spellclass,lvl]
        return(spell_list)

    def add_expertise(self,options):
        i = 0
        while i < len(self.character_expertise):
            options = options.remove(self.character_expertise[i])
            i += 1 

        new_expertise = [random.choice(options,2,replace=False)]

        character_expertise += new_expertise

        return(new_expertise)

    def add_to_char(self,available_list,current_list,item):
        if len(item) > 1: ## For multiple items
            for i in range(len(item)):
                self.add_to_char(available_list,current_list,item[i])
        try:
            available_list.remove(item)
            current_list += [item]
        except: 
            available_list = available_list

    def full_caster_progression(self,spellclass,lvl,spell_count = 1):
        ## All spellcasters have similar enough progression that this can save a few lines.
        new_spells = []

        ## Handle Cantrips and starting spells
        if lvl == 1:
            ## Starting cantrip amounts
            starting_cantrip_n = 2
            ## The classes with a bonus cantrip
            if spellclass in ['Cleric','Sorcerer','Wizard']:
                starting_cantrip_n += 1
                if spellclass == 'Sorcerer':
                    starting_cantrip_n += 1 ## For 4 total
            
            ## Add cantrips to character sheet
            starting_cantrips = random.choice(self.available_cantrips[spellclass],starting_cantrip_n,replace=False)
            self.add_to_char(self.available_cantrips[spellclass],self.character_cantrips[spellclass],starting_cantrips)
            new_spells.append([f"Starting Cantrips: {starting_cantrips}"])

            ## Same for spells
            starting_spells = random.choice(self.available_spells[spellclass],spell_count,replace=False)        
            self.add_to_char(self.available_spells[spellclass],self.character_spells[spellclass],starting_spells)
            new_spells.append([f"Starting Spells: {starting_spells}"])
        
        elif lvl in [4,10]: ## Additional cantrip
            bonus_cantrip = random.choice(self.available_cantrips[spellclass],replace=False)
            new_spells.append(f'Bonus cantrip: {bonus_cantrip}')

            ## Add cantrips to character sheet
            self.add_to_char(self.available_cantrips[spellclass],self.character_cantrips[spellclass],bonus_cantrip)
        
        ## Increase spell level
        elif lvl % 2 == 1:
            spell_level = ceil(lvl/2)
            self.available_spells[spellclass] += self.get_spell_list(spellclass,spell_level)

        if lvl > 1: ## Add new spells each level
            new_spell = random.choice(self.available_spells[spellclass],spell_count,replace=False)
            new_spells.append(f'New Spell: {new_spell}')

            self.add_to_char(self.available_spells[spellclass],self.character_spells[spellclass],new_spell)
        
        return new_spells

    def select_feat_opt(self,source):
        '''
        All of the potential feat/ASI options.
        '''
        random_features = []
        # Equal chance of feat or ASI
        feat_type = random.choice(['ASI','Feat'])

        ## Gets the most recent score
        current_scores = self.abillity_scores.iloc[:,-1]
        self.abillity_scores[source] = current_scores ## In case of change

        if feat_type == 'ASI':
            
            randomized = current_scores.sample(frac = 1)
            valid_scores = randomized[randomized != 20]

            if valid_scores.iloc[0] == 19:
                bonus = 1
            else:
                bonus = random.choice([1,2])
            
            valid_scores.iloc[0] += bonus
            valid_scores.iloc[1] += abs(bonus-2) ## In case of a 1,1

            self.abillity_scores[source] = valid_scores.sort_index()
            random_features.append(f"Abillity Score increase: New scores: {(self.abillity_scores[source].values).astype(int)}")
        else:
            feat_choice = random.choice(self.available_feats)
            self.add_to_char(self.available_feats,self.character_feats,feat_choice)

            random_features.append([f"New feat: {feat_choice}"])

            ## Now to handle the feats with options or other bonuses...
            if (feat_choice in ['Actor','Performer']) & (self.abillity_scores.iloc[5,-1].astype(int) < 20): ## increase CHA by 1
                self.abillity_scores.iloc[5,-1] += 1
                if feat_choice == 'Actor': ## Add deception and performance expertise
                    try:
                        self.add_to_char(self.available_skills,self.character_skills,['Deception','Performance'])
                    except:
                        e = 1 ## They may already have it
                    self.add_expertise(['Deception','Performance'])
            
            elif feat_choice in ['Athelte','Lightly Armoured','Moderately Armoured','Weapon Master']: ## Increase STR or DEX by 1
                str_dex = self.abillity_scores.iloc[[0,1],[0,-1]]
                inc_choice = random.choice(str_dex.loc[str_dex[source] < 20,'Score'])

                self.abillity_scores.loc[self.abillity_scores['Score'] == inc_choice,source] += 1
                random_features.append([f"Extra Increase: {inc_choice}"])

                if feat_choice == 'Weapon Master':
                    random_features.append(["If you are so unlucky that you got weapon master and don't have every weapon, you get a freeby. I am not dealing with programming in weapon proficiency for one dogshit feat."])

            elif (feat_choice == 'Durable') &  (self.abillity_scores.iloc[2,-1].astype(int) < 20):
                self.abillity_scores.iloc[2,-1] += 1
            
            elif feat_choice == 'Elemental Adept':
                ele_choice = random.choice(['Acid','Cold','Lightning','Fire','Thunder'])

                random_features.append([f"Element: {ele_choice}"])

            elif (feat_choice in ['Heavily Armoured','Heavy Armor Master']) & (self.abillity_scores.iloc[0,-1].astype(int) < 20):
                self.abillity_scores.iloc[0,-1] += 1
            
            elif 'Magic Initiate:' in feat_choice:
                ## All of the MIs are the same, so this should work
                spell_class = feat_choice.split(': ')[1]

                ## Add cantrips to character sheet
                cantrips = random.choice(self.available_cantrips[spell_class],2,replace=False)
                self.add_to_char(self.available_cantrips[spell_class],self.character_cantrips[spell_class],cantrips)
                
                ## Same for spells
                spell = random.choice(self.available_spells[spell_class])
                self.add_to_char(self.available_spells[spell_class],self.character_spells[spell_class],spell)

                random_features.append([f"Cantrips: {cantrips}, Spell: {spell}"])
            
            elif feat_choice == 'Martial Adept':
                choice_manoeuvres = random.choice(self.available_manoeuvres,2,replace=False)
                self.add_to_char(self.available_manoeuvres,self.character_manoeuvres,choice_manoeuvres)

                random_features.append([f"Manoeuvres: {choice_manoeuvres}"])

            elif feat_choice == 'Resilient':
                res_choice = random.choice(self.abillity_scores['Score'])

                if self.abillity_scores.loc[(self.abillity_scores['Score'] == res_choice),source] < 20:
                    self.abillity_scores.loc[(self.abillity_scores['Score'] == res_choice),source] =+ 1
                
                random_features.append([f"Resilient Score: {res_choice}"])
            
            elif feat_choice == 'Ritual Caster':
                rit_choice = random.choice(['Enhance Leap','Disguise Self','Find Familiar','Longstrider','Speak with Animals','Speak with Dead'],2,replace=False)

                random_features.append([f"Ritual Spells: {rit_choice}"])
            
            elif feat_choice == 'Skilled':
                new_skills = random.choice(self.available_skills,3,replace=False)

                self.add_to_char(self.available_skills,self.character_cantrips,new_skills)
                random_features.append([f"New Skills: {new_skills}"])
            
            elif feat_choice == 'Spell Sniper':
                spell_snip = random.choice(['Bone Chill', 'Eldritch Blast','First Bolt','Ray of Frost','Shocking Grasp','Thorn Whip'])

                random_features.append([f"Bonus Cantrip: {spell_snip}"])

            elif feat_choice == 'Tavern Brawler':
                str_con = self.abillity_scores.iloc[[0,2],[0,-1]]
                inc_choice = random.choice(str_con.loc[str_con[source] < 20,'Score'])
                
                self.abillity_scores.loc[self.abillity_scores['Score'] == inc_choice,source] += 1
                random_features.append([f"Extra Increase: {inc_choice}"])

        return random_features
    
    ###### Character Initialization --------------------------------------------------------------------------------------
    
    def gen_background(self):
        prompt_background = input("Randomize Background? (Y/N):").lower()

        if prompt_background in ["n","no","negative","neg","f","false"]:
            background = input("What Background Are You Choosing?").lower()

            if background in ['dark urge','the dark urge','durge','thedarkurge','darkurge']:
                background = "haunted one"
            try:
                skill_one = BACKGROUND_SKILLS.loc[background,'Skill 1']
                skill_two = BACKGROUND_SKILLS.loc[background,'Skill 2']
            except: 
                print("Not a Valid Background, Try Again (check spelling).")
                bck = self.gen_background()
                return(bck)
                
        else:
            print("Randomizing Background...")
            background = random.choice(BACKGROUNDS)
            skill_one = BACKGROUND_SKILLS.loc[background,'Skill 1']
            skill_two = BACKGROUND_SKILLS.loc[background,'Skill 2']

        ## With skills chosen, remove them from options and add them to chosen skills

        self.add_to_char(self.available_skills,self.character_skills,skill_one)
        self.add_to_char(self.available_skills,self.character_skills,skill_two)

        ## Chose Roleplay Options:
        randfeatures = f'God (Optional): {random.choice(GODS)}, Alignment (Optional): {random.choice(ALIGNMENTS)}'

        return([background,randfeatures])

    def gen_race(self):
        print("Randomizing Race...")
        
        ## Good for removal later
        high_elf_cantrip = random.choice(self.get_spell_list('Wizard','Cantrip'))
        human_skill = random.choice(self.available_skills) ## For later


        race_options = [
            f'Human',
            random.choice([f'High Elf','Wood Elf']),
            'Drow',
            random.choice([f'High Half-Elf','Wood Half-Elf','Drow Half-Elf']),
            'Half-Orc',
            random.choice(['Lightfoot Halfling','Strongheart Halfling']),
            random.choice(['Gold Dwarf','Shield Dwarf','Duegar']),
            random.choice(['Rock Gnome','Forest Gnome','Deep Gnome']),
            random.choice(['Asmodeus Tiefling','Mephistopheles Tiefling','Zariel Tiefling']),
            'Githyanki',
            f'{random.choice(DRACONIC_COLORS)} Dragonborn'
        ]

        race = random.choice(race_options)

        ## Remove available skills
        if race == f'Human':
            self.add_to_char(self.available_skills,self.character_skills,human_skill)
            return([race,f"Skill: {human_skill}"]) ## One of the few with a random feature
        elif ('Elf' in race) or ('Drow' in race):
            if ('Half' not in race):
                self.add_to_char(self.available_skills,self.character_skills,'Perception')
            if ('Wood' in race):
                self.add_to_char(self.available_skills,self.character_skills,'Stealth')
            if ('High' in race):
                return([race,f"Cantrip: {high_elf_cantrip}"]) ## One of the few with a random feature
        elif race == 'Half-Orc':
            self.add_to_char(self.available_skills,self.character_skills,'Intimidation')
        elif race == 'Deep Gnome':
            self.add_to_char(self.available_skills,self.character_skills,'History')

        return([race,'No other random features'])

    def gen_scores(self):
        print("Randomizing Scores...")
        '''
        This is going to randomly sort the list, making it so that a method is 
        possible where one score is higher on average than the others, allowing for
        a primary score. This is meant to be a bone thrown. 
        '''

        randomized = self.abillity_scores['Score'].sample(frac = 1)

        points_avail = 27
        bonus = 2 ## racial bonus, applied to the first two in list
        iters = 0 ## to keep track in case of mismatch
    

        for s in randomized:
            ## So we don't go over
            available_buys = POINT_COST.loc[POINT_COST['Cost'] <= points_avail,'Cost']
            remaining = 6-iters ## to help with later buys

            ## Potential Exceptions
            if iters == 5: ## Makes sure all remaining points are used
                cost = points_avail
            elif points_avail > (remaining - 1) * 9: ## Points can't be higher than 9, so this raises the floor to meet that
                available_buys = POINT_COST.loc[POINT_COST['Cost'] >= points_avail/remaining,'Cost']
                #print(available_buys.shape)
                cost = random.choice(available_buys)
            else:
                cost = random.choice(available_buys)

            # Prevents the last score from being 6 or 8
            if ((iters == 4) & ((points_avail - cost) in [6,8])): 
                available_buys = available_buys[(points_avail - available_buys != 6) & (points_avail - available_buys != 8)]
                cost = random.choice(available_buys)
            if ((iters == 3) & ((points_avail - cost) in [15,17])):
            
                available_buys = available_buys[(points_avail - available_buys != 15) & (points_avail - available_buys != 17)]
                cost = random.choice(available_buys)
            elif ((iters == 2) & ((points_avail - cost) in [26,24])):
            
                available_buys = available_buys[(points_avail - available_buys != 24) & (points_avail - available_buys != 26)]
                cost = random.choice(available_buys)
            
            increase = bonus + POINT_COST.loc[POINT_COST['Cost'] == cost,'Increase'].values[0]
            self.abillity_scores.loc[self.abillity_scores['Score'] == s,'Level 1'] = 8 + increase
            self.abillity_scores.loc[self.abillity_scores['Score'] == s,'Free Bonus'] = f'+{bonus}' 

            ## for next iteration
            points_avail -= cost
            bonus = max(bonus - 1,0)
            iters += 1
        
        final_lvl_1 = (
            f"""
            STR: {self.abillity_scores.iloc[0,3]} ({self.abillity_scores.iloc[0,2]})
            DEX: {self.abillity_scores.iloc[1,3]} ({self.abillity_scores.iloc[1,2]})
            CON: {self.abillity_scores.iloc[2,3]} ({self.abillity_scores.iloc[2,2]})
            INT: {self.abillity_scores.iloc[3,3]} ({self.abillity_scores.iloc[3,2]})
            WIS: {self.abillity_scores.iloc[4,3]} ({self.abillity_scores.iloc[4,2]})
            CHA: {self.abillity_scores.iloc[5,3]} ({self.abillity_scores.iloc[5,2]})
            """
        )

        return([final_lvl_1,'No other random features'])

    def build_all_classes(self):
        '''
        Initialiation for the class table; picks skills and subclasses for all classes.
        '''
    
        ## Basic Class Structure. -------------------------------------------------------------------------

        self.class_info = pd.DataFrame(index=CLASSES, columns = ['Starting Skills','Spellcasting Abillity',
                                                            'Subclass','Current Level'])

        ## Fills in the columns
        self.class_info['Starting Skills'] = [
            ['Animal Handling','Athletics','Intimidation','Nature','Survival','Perception'],
            ALL_SKILLS,
            ['History','Insight','Medicine','Persuasion','Religion'],
            ['Arcana','Animal Handling','Insight','Medicine','Nature','Perception','Religion','Survival'],
            ['Acrobatics','Animal Handling','Athletics','History','Insight','Intimidation','Perception','Survival'],
            ['History','Insight','Religion','Acrobatics','Stealth','Athletics'],
            ['Athletics','Insight','Intimidation','Medicine','Persuasion','Religion'],
            ['Animal Handling','Athletics','Insight','Investigation','Nature','Perception','Stealth','Survival'],
            ['Acrobatics','Athletics','Deception','Insight','Intimidation','Investigation','Perception','Performance','Persuasion','Sleight of Hand','Stealth'],
            ['Arcana','Deception','Insight','Intimidation','Persuasion','Religion'],
            ['Arcana','Deception','History','Intimidation','Investigation','Nature','Religion'],
            ['Arcana','History','Investigation','Insight','Medicine','Religion']
        ]
        self.class_info['Spellcasting Abillity'] = ['CHA','CHA','WIS','WIS','INT','WIS',
                                            'CHA','WIS','INT','CHA','CHA','CHA']
        self.class_info['Current Level'] = 0

        ## Selects the subclasses for each class
        self.class_info['Subclass'] = [random.choice(s) for s in SUBCLASSES]

    def level_one(self):
        '''
        Call the builder functions for level one and selects the first class.
        '''

        self.character_sheet.loc['Background'] = self.gen_background()
        self.character_sheet.loc['Race'] = self.gen_race()
        self.character_sheet.loc['Abilities'] = self.gen_scores()

        self.build_all_classes()

        ## Starting Class
        starting_class = random.choice(CLASSES)
        self.class_info.loc[starting_class,'Current Level'] = 1

        ## Starting Skill Proficiencies, since other than a few options
        ## this does not get repeated past true level 1.
        if starting_class == 'Cleric': ## Because both of the skills are tied to level 1
            skill_count = 0
        elif starting_class == 'Rogue': # Because rogue has one more than Bard and Ranger
            skill_count = 3
        else:
            skill_count = 2
        ## Intersection of available skills
        available_class_skills = list(set(self.available_skills) & set(self.class_info.loc[starting_class,'Starting Skills']))

        ## Adds the starting skills to character sheet
        starting_skills = random.choice(available_class_skills,skill_count,replace=False)
        self.add_to_char(self.available_skills,self.character_skills,starting_skills)

        self.character_sheet.loc['Starting Skills'] = [starting_class,starting_skills]
    
    ###### Difficulty Selection --------------------------------------------------------------------------------------
    def difficulty_select(self):
        '''
        Selects the difficulty the builder will use for class selection. This was built around Hard (Heavy) being the default,
        though Medium is probably a more enjoyable gamplay experience. 
        '''
        difficulty = input("Select Difficulty:\n" \
        "Unarmoured (All Levels are in One Class)\n"\
        "Light (All Levels Use the Same Spellcasting Abillity)\n"\
        "Medium (Random Selection of 4 Classes)\n"\
        "Heavy (No Restrictions)\n"\
        "Custom (Select Number of Classes)").lower()

        starting_class = self.character_sheet.loc['Starting Skills','Selection']
        
        if difficulty == "custom":
            try: ## In case they submit a string
                n = int(input('Custom Selected. Please Select a number from 1 to 12'))
            except: 
                n = 0
            while n not in range(1,13):
                try: ## In case they submit a string
                    n = int(input('Invalid Input. Please Select a number from 1 to 12'))
                except: 
                    n = 0
            if n == 1:
                print('Defined Case: Unarmoured')
                difficulty = "unarmoured"
            elif n == 4:
                print('Defined Case: Medium')
                difficulty = "medium"
            elif n == 12:
                print('Defined Case: Heavy')
                difficulty = "heavy"
            
            else: 
                print(f'Randomizing {n} classes')
                adtl_classes = random.choice(self.class_info.loc[~self.class_info.index.isin([starting_class])].index,(n-1),replace = False)
                chosen_classes = [starting_class] + adtl_classes.tolist()
                self.level_pool = self.class_info.loc[chosen_classes].copy

        if difficulty == "unarmoured":
            print('Unarmoured Selected')
            self.level_pool = self.class_info.loc[starting_class].copy()
        elif difficulty == "light":
            print('Light Selected')
            spell_ab = self.class_info.loc[starting_class,'Spellcasting Abillity']
            self.level_pool = self.class_info[self.class_info['Spellcasting Abillity'] == spell_ab].copy()
        elif difficulty == "heavy":
            print('Heavy Selected')
            self.level_pool = self.class_info.copy()
        else:
            print('Medium Selected or Unknown Input')
            ## Get the three other options
            adtl_classes = random.choice(self.class_info.loc[~self.class_info.index.isin([starting_class])].index,3,replace = False)
            chosen_classes = [starting_class] + adtl_classes.tolist()
            self.level_pool = self.class_info.loc[chosen_classes].copy()

    ###### The big def that runs through each class level and option. ---------------------------------------
    def get_class_features(self,featured_class,lvl):

        random_features = []
        subclass = self.class_info.loc[featured_class,'Subclass']
        ## ASI/feat
        if (lvl in [4,8,12]) or ((featured_class == 'Fighter') & (lvl == 6)) or ((featured_class == 'Rogue') & (lvl == 10)):
            random_features.append(self.select_feat_opt(source=(f'Level {lvl} {featured_class}')))
        
        ## Barbarian class options
        if featured_class == 'Barbarian':
            if (lvl in [1,2,4,5,7,8,9,11,12]) or (subclass != 'Wildheart' & (lvl in [6,10])):
                random_features.append('No other random features')
            elif lvl == 3:
                random_features.append([f"Subclass: {subclass}"])
                if subclass == 'Wildheart':
                    random_features.append([f"Beastial Heart: {random.choice(['Bear','Eagle','Elk','Tiger','Wolf'])}"])
                    self.available_aspects = RANDOM_FEATURES.loc[RANDOM_FEATURES['Feature'] == 'Aspects of the Beast','Choice'].explode()
                    self.character_aspects = []
            else:
                ## Beastial Aspects

                aspect = random.choice(self.available_aspects)
                self.add_to_char(self.available_aspects,self.character_aspects,aspect)
                if aspect == 'Tiger':
                    try:
                        self.add_to_char(self.available_skills,self.character_skills,'Survival')
                    except: 
                        e = 1 ## They may already have survival

                random_features.append([f"Animal Aspect: {aspect}"])       

        ## Bard Class Options
        elif featured_class == 'Bard':
            if lvl == 1:
                ## Intersection of available skills
                available_class_skills = list(set(self.available_skills) & set(self.class_info.loc['Bard','Starting Skills']))

                ## Adds the bonus skill to character sheet
                bonus_skill = random.choice(available_class_skills)
                self.add_to_char(self.available_skills,self.character_skills,bonus_skill)
                random_features.append([f"Additional Skill: {bonus_skill}"])

                ## Starting cantrips and spells
                random_features.append(self.full_caster_progression('Bard',lvl,4))

            elif lvl == 3:
                random_features.append([f"Subclass: {subclass}"])
                random_features.append(f"Expertise: {self.add_expertise(self.character_skills)}")
                if subclass == 'Swords':
                    fs = random.choice(['Dueling','Two-Weapon Fighting'])   
                    random_features.append([f"Fighting Style: {fs}"])
                    self.add_to_char(self.available_fighting,self.character_fightning,fs)
                elif subclass == 'Lore':
                    lore_skills = random.choice(self.available_skills,3,replace=False)
                    self.add_to_char(self.available_skills,self.character_skills,lore_skills)
                    random_features.append(f"Bonus Skills: {lore_skills}")
                        
            elif lvl == 10 or (subclass == 'Lore' & (lvl == 6)):
                ## Not as easy to copy from bg3.wiki unfortunetly
                magical_secrets = ['Bone Chill','Fire Bolt','Sacred Flame','Eldritch Blast','Ray of Frost',
                                'Armor of Agathys','Bless','Guiding Bolt','Magic Missle','Chromatic Orb', 'Hellish Rebuke','Sanctuary','Command','Hex','Thunderous Smite','Entangle',"Hunter's Mark",
                                'Arcane Lock', 'Blur','Darkness','Darkvision','Misty Step','Pass Without Trace','Ray of Enfeeblement','Scorching Ray','Spike Growth','Spiritual Weapon','Web',
                                'Animate Dead', 'Call Lightning','Counterpsell',"Crusader's Mantle",'Daylight','Fireball','Gaseous Form','Grant Flight','Haste','Hunger of Hadar','Lightning Bolt','Mass Healing Word','Remove Curse','Revivify','Sleet Storm','Slow','Spirit Guardians','Vampiric Touch','Warden of Vitality']
                ## Yes, if you make it as lore bard 10 this does reset but I don't feel like fixing it, given how unlikely it is for a duplication
                ## to happen. If it does, then it would be a freeby. 
                if lvl == 10:
                    magical_secrets += ['Banishment','Blight','Death Ward','Dominate Beast','Fire Shield','Guardian of Faith','Ice Storm','Wall of Fire',
                                        'Banishing Smite','Cone of Cold','Conjure Elemental','Contagion','Wall of Stone']
                    
                    random_features.append(f"Expertise: {self.add_expertise(self.character_skills)}")

                add_ms = random.choice(magical_secrets,2,replace=False)
                random_features.append(f'Magical Secrets: {add_ms[0]} and {add_ms[1]}')

            ## Fullcaster Spell Progression
            if lvl > 1:
                random_features.append(self.full_caster_progression('Bard',lvl))
            
        ## Cleric Class Options
        elif featured_class == 'Cleric':
            if lvl == 1:
                ## Subclass and God
                random_features.append(f"Subclass: {subclass}")

                ## Intersection of available skills
                available_class_skills = list(set(self.available_skills) & set(self.class_info.loc['Cleric','Starting Skills']))

                ## Adds the skills to character sheet
                cleric_skills = random.choice(available_class_skills)
                self.add_to_char(self.available_skills,self.character_skills,cleric_skills)
                random_features.append(f"Cleric Skills: {cleric_skills}")

                ## Add cantrips to character sheet
                random_features.append(self.full_caster_progression('Cleric',lvl,0))

                if subclass == 'Knowledge':
                    
                    knowledge_expertise = random.choice(['Arcana','Religion','Nature','History'],2)
                    
                    try:
                        self.add_to_char(self.available_skills,self.character_skills,knowledge_expertise)
                    except:
                            e = 1 ## They may already have it
                    self.add_expertise(knowledge_expertise)
                    random_features.append([f"Knowledge Expertise: {knowledge_expertise}"])
                
                elif subclass == 'Nature':
                    
                    nature_cantrip = random.choice(['Poison Spray','Produce Flame','Shillelagh','Thorn Whip'])
                    random_features.append([f"Bonus Nature Cantrip: {nature_cantrip}"])

                    nature_skill = random.choice(list(set(self.available_skills) & set(['Animal Handling','Nature','Survival'])))
                    self.add_to_char(self.available_skills,self.character_skills,nature_skill)
                    random_features.append([f"Bonus Nature Skill: {nature_skill}"])

            elif lvl in [4,10]:
                random_features.append(self.full_caster_progression('Cleric',lvl,0))
            
            else:
                random_features.append("No other random features, since prepared spells are swapped whenever")
        
        ## Druid Class Options
        elif featured_class == 'Druid':
            if lvl == 1:
                
                ## Cantrips are the only level 1 option.
                random_features.append(self.full_caster_progression('Druid',lvl,0))

            elif lvl == 2:
                random_features.append([f"Subclass: {subclass}"])

                if subclass == 'Land':
                    bonus_cantrip = random.choice(self.available_cantrips['Druid'])
                    random_features.append([f"Bonus Cantrip: {self.starting_cantrips}"])

                    self.add_to_char(self.available_cantrips['Druid'],self.character_cantrips['Druid'],bonus_cantrip)


            elif ((lvl in [3,4,5,7,9]) & (subclass == 'Land')):
                lands = RANDOM_FEATURES.loc[RANDOM_FEATURES['Feature'] == 'Circle Land','Choice']

                random_features.append([f"Land Choice: {random.choice(lands)}"])
            
            elif lvl in [4,10]:
                random_features.append(self.full_caster_progression('Druid',lvl,0))
            
            else:
                random_features.append("No other random features, since prepared spells are swapped whenever")

        ## Fighter Class Options
        elif featured_class == 'Fighter':

            if lvl == 1:
                fs_choice = random.choice(self.available_fighting)

                self.add_to_char(self.available_fighting,self.character_fightning,fs_choice)
                random_features.append(f'Fighting stlye: {fs_choice}')
            elif lvl in [2,5,9] or ((lvl == 11) & (subclass != 'Eldritch Knight')):
                random_features.append("No other random features")
            
            ## Subclass options:
            elif subclass == 'Arcane Archer':
                self.available_shots = RANDOM_FEATURES.loc[RANDOM_FEATURES['Feature'] == 'Arcane Shot','Choice'].explode()
                self.character_shots = []
                if lvl == 3:
                    random_features.append([f"Subclass: {subclass}"])

                    ## Cantrip
                    bonus_cantrip = random.choice(['Guidance','Light','True Strike'])
                    random_features.append([f"Bonus Cantrip: {bonus_cantrip}"])

                    ## Skills
                    try:
                        self.add_to_char(self.available_skills,self.character_skills,'Arcana')
                    except: 
                        e = 1 ## They may already have arcana
                    try:
                        self.add_to_char(self.available_skills,self.character_skills,'Nature')
                    except: 
                        e = 1 ## They may already have nature
                    
                    ## Shots
                    choice_shots = random.choice(self.available_shots,3,replace=False)
                    self.add_to_char(self.available_shots,self.character_shots,choice_shots)
                    random_features.append([f"Arcane Shots: {choice_shots}"])
                elif lvl in [7,10]:
                    choice_shot = random.choice(self.available_shots)
                    self.add_to_char(self.available_shots,self.character_shots,choice_shot)
                    random_features.append([f"Arcane Shot: {choice_shot}"])

            elif subclass == 'Battle Master':
                if lvl == 3:
                    random_features.append([f"Subclass: {subclass}"])

                    choice_manoeuvres = random.choice(self.available_manoeuvres,3,replace=False)
                    self.add_to_char(self.available_manoeuvres,self.character_manoeuvres,choice_manoeuvres)

                    random_features.append([f"Manoeuvres: {choice_manoeuvres}"])
                elif lvl in [7,10]:
                    choice_manoeuvres = random.choice(self.available_manoeuvres,2,replace=False)
                    self.add_to_char(self.available_manoeuvres,self.character_manoeuvres,choice_manoeuvres)

                    random_features.append([f"Manoeuvres: {choice_manoeuvres}"])

            elif subclass == 'Champion':
                if lvl == 3:
                    random_features.append([f"Subclass: {subclass}"])
                elif lvl == 7:
                    random_features.append("No other random features")
                elif lvl == 10:
                    fs_choice = random.choice(self.available_fighting)

                    self.add_to_char(self.available_fighting,self.character_fightning,fs_choice)
                    random_features.append(f'Fighting stlye: {fs_choice}')

            elif subclass == 'Eldritch Knight':
                if lvl == 3:
                    random_features.append([f"Subclass: {subclass}"])

                    ## Spells



        ## Monk Class Options

        ## Paladin Class Options
        elif featured_class == 'Paladin':
            if lvl == 1:
                random_features.append([f"Subclass: {subclass}"])
                
            
            else:
                if lvl == 2:
                    ## Cross section of available fighting styles:
                    available_pally = list(set(self.available_fighting) & set(['Defence','Dueling','Great Weapon Fighting','Protection']))
                    fs_choice = random.choice(available_pally)

                    self.add_to_char(self.available_fighting,self.character_fightning,fs_choice)
                    random_features.append(f'Fighting stlye: {fs_choice}')

                random_features.append("No other random features, since prepared spells are swapped whenever")

        ## Ranger Class Options

        ## Rogue Class Options

        ## Sorcerer Class Options

        ## Warlock Class Options

        ## Wizard Class Options
        if featured_class == 'Wizard':
            if lvl == 1:
                
                ## The additional starting spells at level 1
                s = 6

            else: 
                s = 2
        
            if lvl == 2:
                random_features.append(f"Subclass: {subclass}")
            elif ((lvl == 5) & (subclass == 'Necromancy')):
                try:
                    self.add_to_char(self.available_spells['Wizard'],self.character_spells['Wizard'],'Animate Dead')
                except:
                    e = 1 ## They may already have it

            random_features.append(self.full_caster_progression('Wizard',lvl,s))

        return([f'Level {lvl} {featured_class}',random_features])

    def build_sheet(self):
        '''
        The primary iterator that builds out each level. 
        '''
        starting_class = self.character_sheet.loc['Starting Skills','Selection']

        ## Start with the pre-determined level 1
        self.character_sheet.loc['Level 1',:] = self.get_class_features(starting_class,1)

        ## Level Iterations --------------------------------------------------------------------------
        for level in range(2,13):
            
            if len(self.level_pool.shape) == 1:
                lvl_up_class = starting_class
                lvl_up_class_lvl = level
            else:
                lvl_up_class = random.choice(self.level_pool.index)
                self.level_pool.loc[lvl_up_class,'Current Level'] += 1

                lvl_up_class_lvl = self.level_pool.loc[lvl_up_class,'Current Level']

            self.character_sheet.loc[f'Level {level}',:] = self.get_class_features(lvl_up_class,lvl_up_class_lvl)

###### Functions that help save the character file ----------------

def try_filename(filename,html_source):
    
    ## To not overwtie existing tav files, appends a number.
    ## Stops after 100 in case of errors
    for r in range(100):
        if r == 0:
            filepath = (f'{filename}.pdf')
        else:
            filepath = (f'{filename} ({r}).pdf')
        
        try:
            result_file = open(filepath, "xb")
            pisa.CreatePDF(html_source,result_file)
            result_file.close()
            print(f'Saved as {filepath}')

            break
        except:
            if r == 99:
                print('Too many files with that filename. Please rename a few in this directory or move them.')

## Do the save ask as function in case of poor input
def ask_save(output):

    blind = input('Save each new level on a seperate page for a blind playthrough? (Y/N)')

    filename = './Characters/My Random Tav'

    if blind.lower() in ["y","yes","true",'"t']:
        print("Saving as 12 Pages...")

        ## Inititalize with page break function
        up_to_i = ''

        for i in range(5,18): ## Makes each additional level its own table with a page break
            up_to_i += output.iloc[:i,:].to_html(index = False,classes = 'wide',escape = False)

        html_source = up_to_i
    
    elif blind.lower() in ["n","no","negative","neg","f","false"]:
        print("Saving as Single Page...")
        html_source = output.to_html(index = False, classes='wide',escape = False)
    
    else:
        print("Invalid Input. Try Again")
        ask_save()
    

    ## HTML formatted from MuhsinFatih on stackoverflow.com
    ## https://stackoverflow.com/questions/47704441/applying-styling-to-pandas-dataframe-saved-to-html-file
    
    FORMATTER = '''
    <html>
    <head>
    <style>
        h2 {
            text-align: center;
            font-family: Helvetica, Arial, sans-serif;
        }
        table { 
            margin-left: auto;
            margin-right: auto;
        }
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        th, td {
            padding: 5px;
            text-align: center;
            font-family: Helvetica, Arial, sans-serif;
            font-size: 100%;
        }
        table tbody tr:hover {
            background-color: #dddddd;
        }
        .wide {
            width: 90%; 
        }
        table {
            page-break-after: always;
        }
        table:last-of-type {
            page-break-after: auto;
        }

    </style>
    </head>
    <body>
        '''

    formatted_table = FORMATTER + html_source + '</body></html>'

    try_filename(filename,formatted_table)


###### Run the program --------------------------------------------

tav = randomize_char()

tav.level_one()
tav.difficulty_select()
tav.build_sheet()

print('Randomization Complete')
ask_save(tav.character_sheet.reset_index())