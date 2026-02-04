# Introduction

Last updated: 

Current Version: 0.1.0 (Open Beta)

Primary contact: SeasideStorm on Discord or Reddit

One of the things I love about Baldur's Gate 3 is just how many options there are when it comes to character creation, and the freedom you get when making your builds. That being said though, sometimes it is easy to get lost in the optimization of everything and figure out how to make the 'best' character to beat the game. So I asked myself, what if you didn't get that choice? What if, in true D&D fasion, your character's build was up to the dice? Well wonder no more, as I have created this here tool to randomize any custom character you want!! There are many levels to choose from, to just picking a single class and getting random features to a full 12-class mayhem.  

# Installation
Everything you need is in the .zip release, which includes the .exe to run. All you need to do in unzip the file into a folder of your choice, though I would recomend against keeping this in downloads. Documents is a decent place for it, or you can even put it next to your BG3 folder if you want. Just note that wherever the application is, that is where your character sheet will go. The prompts will all be done through the terminal, but that is just the interface this program uses and won't do anything to your computer. You need no coding experience to work with this, just a keyboard and mouse!

# Usage
Once installed, the program can be run with a simple double click in file explorer. This will open up the terminal (os agnostic) and start the randomization.

## User Inputs
During the randomization, there will several keyboard inputs to help determine the way the randomization is handled. Inputs are not case-sensitive.

#### Randomize Background? (Y/N):
##### Acceptable inputs: Yes/Y/No/N
##### Default: Yes
During the background generation, which is also needed to determien starting skills, it is possible to set a background. The primary reason for this is for **Dark Urge** playthroughs, since that is technically both an origin character and a background. This is the only difference between Durge and Tav a character creation, and it is the most popular way to play on repeat playthroughs so the skills gained from that background needed to be considered. 

A 'yes' or invalid input skips the next question and randomly selects a background (haunted one is included in the options). A 'no' prompts the user to select which background they want.


#### What Background Are You Choosing?
##### Acceptable inputs: Background name
##### Default: None, Restarts Background prompt

> For dark urge playthroughs, the correct background (and thus input) would be "Haunted One". However, it is a special enough case that the following inputs were added in as possible options: "Dark Urge", "The Dark Urge" and "Durge". 

Selects which background to use for generation. If no background is recognized, re-asks the user if they would like to randomize their background.

#### Select Difficulty
##### Acceptable inputs: Unarmoured/Light/Medium/Heavy/Custom
##### Default: Medium

Selects the difficulty the builder will use for class selection. This was built around Hard (Heavy) being the default, though Medium is probably a more enjoyable gamplay experience. I named them after the different armour types in BG3 because I felt it worked well. 

> Unarmoured: All levels use the same class, just randomizing features.
>
> Light: Classes chosen at each level up are randomized, the pool of available classes all share the same [spellcasting modifier]('https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://bg3.wiki/wiki/Spells&ved=2ahUKEwj-g8PW_smRAxUsg4kEHbIMNkoQFnoECBwQAQ&usg=AOvVaw1-N_7_9wJmsIGDOUdc_qk7') as the starting class.
>
> Medium: Randomly chooses a pool of 3 classes in addition to the starting class that each level can pull from.
>
> Heavy: The pool includes all 12 classes.
>
> Custom: The pool includes x classes, where x is inclusive of the starting class.

#### Custom Selected. Please Select a number from 1 to 12
##### Acceptable inputs: 1-12
##### Default: None, asks again

The x for how many classes the pool should include. An x value of 1, 4, or 12 defualts the appropriate defined difficulty.

#### Save each new level on a seperate page for a blind playthrough? (Y/N)
##### Acceptable inputs: Yes/Y/No/N
##### Default: None, asks again

Asks if the output should be a single page that lists all 12 levels, so you know what you are getting yourself into and can build around it with items, or if it should be 'blind'. This prints 12 pages, with each page including up to that level so you don't know what you get at each level until you level up. 


## Completed Randomization
Once the character is generated, it will go into a 'characters' folder as a PDF document named 'My Randomized Tav'. From here you can open the document and use it to base your next BG3 character on!

You will also notice that regardless of classes chosen, in the background section a God and Alignment is chosen. These are super optional bits of flavor, and are just there if you really want to get into the roleplay aspect when it comes to choices and dialouge options.

# Caveats and Limitations

## Feats

#### ASI Weights
Rather than weighting abillity score increase as a feat (like it techically is), I instead weighted it as as an abillity score OR feat. This means that instead of having a 1/41 chance at an abillity score increase (which are usually pretty useful), it is 1/2. This does mean that feats have an individual 1/80 chance to be chosen, which isn't ideal. This is of course mitigated by the fact that the ability score allocation is random, so you want more of them to hopefully go to the right place. Future versions may adjust the weight (maybe 1:2 instead of 1:1).

#### Prerequisites
It is worth noting that currently, none of the feats take prerequisites into account when determining if a feat can be taken or not. This felt like such an outlier, given how few feats in vanilla have prerequeisites, that would take a good bit to work around. If you happen to roll a feat that you don't meet the conditions for, I recommend picking another similar feat. If the rolled feat is a half feat (like the armor master feats), choose a feat that can give the same abillity score bonus for continuity.

#### Weapon Master and Weapon/Armor Proficiency
Because Weapon Master is the only instance where weapon proficiency matters, I have opted to ignore this mechanic entirely. If you are so unlucky that you got Weapon Master and don't have every weapon, you get a freeby to choose whatever weapons you want. I am not dealing with programming in weapon proficiency for one dogshit feat. 

## Multiclasting
It is worth noting that when it comes to multiclassing casters (multiclasting) that share spells on their spell lists, this does not remove chosen spells from the possible spell options list. For example, getting Mage Hand from Wizard doesn't mean it is blacklisted from Sorcerer. This is is to 
be consistent with base game where you can have multiple spells from different casting
stats. If you get a duplicate you don't want, you can either keep it for an extra challenge or have it be free choice. 

## Mods
Unsurprisingly, this is only built to handle the base game (as of Patch 8), unless you count mods that add the option to select a deity with any class since that is a 'flavor' option this code can generate along with alignment. Any mods that add classes, subclasses, spells, feats, new deities, etc. would not be natively supported. That being said, modded subclasses, deities, and feat can easily be added by adding them to their respective list in constants -- however this will only add the name, and not any other options that may come from said subclass. Similarly, new spells can be added to the 'raw' list, and then 'bg3_option_cleaner.py' can be run. If you do not have the ability to do that, reach out to me via Discord or Reddit with the new constants and I will do my best to get you a modded version.

# Coding Etiqutte: Why 'If'?
Any coder that looks at the base file may be horrified to see that this whole thing is built on If/Else conditional statements, so I would like to explain why I have done so. For something like this a lookup table would likely be best, with all classes and level initialized randomly at the start then use the difficulty selection to cut that down to the proper subset and call each column/row to fill out the character sheet. The reason why this can't be, or at least wasn't, done is due to multiple similar features needing to know what comes before them to make an educated desicion. 

Take expertise as an example. It can only choose from the current skills proficiency list, and can only select those that don't have expertise. Without using if/else, I could not figure out a way that would allow expertise to pick from the proper selection of available skills and thus needed to be done iteratively. If there are other suggestions that can improve the readability and functionality of the code I am more than happy to hear them! This just seemed like the best way to handle the complexity of choices in a game like BG3. 

# Editing
This is in a very rough state, and likely still has a lot of bugs that would be impossible (or at the very least impractical) for me to catch on my own. As such, if you have the skills to do so! Just make a branch on this repository with any edits and create a pull request that I will approve. There is also the future improvements list down below if you have the time and want to help out!

For any other modifications/edits/usages/etc. just follow the license and credit!

# Future Improvements
I have been working on this on and off for a bit, and now that it is in an at least usable state I may just let it stew for a bit. That being said, these are some of the ideas I would love to implement so the community can stay tuned for what is to come or help out if they have ideas!

These are in no particular order.

* Clean the HTML output.
    * Potential with a more 'BG3' theme.
* Add a better user interface, either as an improvement to the .exe or (even better) as some type of web tool.
* Streamline mod compatibility.
* Add in feat prerequisites.
    * Would also need to add in weapon/armor proficiency. 
* New difficuly setting that puts restrictions on ability scores, making it easier to have a primary stat increased and have a class related to the primary stat.
* Figure out if it is cleaner and less memory intensive to keep each level as if/else statements, or if there should be a 12x12 table initialized that has all the random options, and each level calls the appropriate .iloc.
* Add in option for third caster's free wizard spell to ONLY pick from the expanded wizard spell list, not including the third caster's spell list. 
* Find a way to save a seed for reproducability.

# Acknowledgments
* Massive shoutout to the folks at bg3.wiki, if I didn't have their tables to copy from I would have lost my mind. 
* This was my first time working with an HTML output, so I want to thank MuhsinFatih on Stackoverflow for the code snippet they pasted on [this](https://stackoverflow.com/questions/47704441/applying-styling-to-pandas-dataframe-saved-to-html-file) page, since that is how I got the tables to look more readable when printed. 

