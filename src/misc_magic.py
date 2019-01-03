#!/usr/bin/python
import random
import logging
from interp import interp
from get_quantity import get_quantity

def set_misc_subtype(item):
    logging.debug("Getting misc subtype")
    if item['name'] == 'Bracers of Defense':
        get_misc_bracer_type(item)
    elif item['name'] == "Bucknard's Everfull Purse":
        get_misc_purse_type(item)
    elif item['name'] == "Cloak of Protection":
        get_misc_cloak_type(item)
    elif item['name'] == "Crystal Ball (M)":
        get_misc_ball_type(item)
    elif item['name'] == "Figurine of Wondrous Power":
        get_misc_figurine_type(item)
    elif item['name'] == "Girdle of Giant Strength (CFT)":
        get_misc_girdle_type(item)
    elif item['name'] == "Ioun Stones":
        get_ioun_stone_type(item)
    elif item['name'] == "Instrument of the Bards":
        get_instrument_type(item)
    elif item['name'] == "Iron Flask":
        get_flask_type(item)
    elif item['name'] == "Jewel of Flawlessness":
        get_jewel_type(item)
    elif item['name'] == "Medallion of ESP":
        get_medallion_type(item)
    elif item['name'] == "Necklace of Missiles":
        get_missile_type(item)
    elif item['name'] == "Necklace of Prayer Beads (C)":
        get_prayer_type(item)
    elif item['name'] == "Nolzur's Marvelous Pigments":
        get_pigment_type(item)
    elif item['name'] == "Pearl of Power (M)":
        get_pearl_type(item)
    elif item['name'] == "Quaal's Feather Token":
        get_token_type(item)
    elif item['name'] == "Amulet Versus Undead":
        get_amulet_type(item)
    elif item['name'] == "Beads of Force":
        get_bead_type(item)
    elif item['name'] == "Dust of Illusion":
        get_illusion_type(item)
    elif item['name'] == "Dust of Tracelessness":
        get_dust_type(item)
    elif item['name'] == "Egg of Desire":
        get_egg_type(item)
    elif item['name'] == "Scarab Versus Golems":
        get_scarab_type(item)
    elif item['name'] == "Sovereign Glue":
        get_glue_type(item)
    elif item['name'] == "Zagyg's Spell Component Case":
        get_case_type(item)
	

def get_ioun_stone_type(item):
   rand = random.randint(1,20)
   if rand <= 1:
       item['name'] = item['name'] + " pale blue rhomboid (+1 str)"
   elif rand <= 2:
       item['name'] = item['name'] + " scarlet & blue sphere (+1 int)"
   elif rand <= 3:
       item['name'] = item['name'] + " blue sphere (+1 wis)"
   elif rand <= 4:
       item['name'] = item['name'] + " red sphere (+1 dex)"
   elif rand <= 5:
       item['name'] = item['name'] + " pink rhomboid (+1 con)"
   elif rand <= 6:
       item['name'] = item['name'] + " pink & green sphere (+1 cha)"
   elif rand <= 7:
       item['name'] = item['name'] + " pale green prism (+1 lvl)"
   elif rand <= 8:
       item['name'] = item['name'] + " clear spindle (food/water)"
   elif rand <= 9:
       item['name'] = item['name'] + " iridescent spindle (air)"
   elif rand <= 10:
       item['name'] = item['name'] + " pearly white spindle (regen)"
   elif rand <= 11:
       item['name'] = item['name'] + " pale lavender ellipsoid (absorb 4th)"
   elif rand <= 12:
       item['name'] = item['name'] + " lavender and green ellipsoid (absorb 8th)"
   elif rand <= 13:
       item['name'] = item['name'] + " purple prism (stores spells)"
   elif rand <= 14:
       item['name'] = item['name'] + " rose prism (+1 protection)"
   elif rand <= 20:
       item['name'] = item['name'] + " dull gray (burned out)"
    
def get_instrument_type(item):
    rand = random.randint(1,20)
    if rand <= 5:
        item['name'] = item['name'] + " - Fochlucan Bandore"
    elif rand <= 10:
        item['name'] = item['name'] + " - Mac-Fuirmidh Cittern"
        item['xplo'] = item['xplo'] * 2
        item['gplo'] = int(item['gplo'])  * 2 
    elif rand <= 12:
        item['name'] = item['name'] + " - Doss Lute"
        item['xplo'] = item['xplo'] * 3
        item['gplo'] = int(item['gplo'])  * 3 
    elif rand <= 15:
        item['name'] = item['name'] + " - Canaith Mandolin"
        item['xplo'] = item['xplo'] * 4
        item['gplo'] = int(item['gplo'])  * 4 
    elif rand <= 17:
        item['name'] = item['name'] + " - Cli Lyre"
        item['xplo'] = item['xplo'] * 5
        item['gplo'] = int(item['gplo'])  * 5 
    elif rand <= 19:
        item['name'] = item['name'] + " - Anstruth Harp"
        item['xplo'] = item['xplo'] * 6
        item['gplo'] = int(item['gplo'])  * 6 
    elif rand <= 20:
        item['name'] = item['name'] + " - Ollamh Harp"
        item['xplo'] = item['xplo'] * 7
        item['gplo'] = int(item['gplo'])  * 7 

def get_flask_type(item):
    rand = random.randint(1,100)
    if rand > 50:
        item['xplo'] = item['xphi']
        item['gplo'] = item['gphi']
    	if rand <= 54:
    	    item['name'] = item['name'] + " (air elemental)"
    	elif rand <= 56:
    	    item['name'] = item['name'] + " (demon (type I-III))"
    	elif rand <= 57:
    	    item['name'] = item['name'] + " (demon (type IV-VI))"
    	elif rand <= 59:
    	    item['name'] = item['name'] + " (devil (lesser))"
    	elif rand <= 60:
    	    item['name'] = item['name'] + " (devil (greater))"
    	elif rand <= 65:
    	    item['name'] = item['name'] + " (djinni)"
    	elif rand <= 69:
    	    item['name'] = item['name'] + " (efreeti)"
    	elif rand <= 72:
    	    item['name'] = item['name'] + " (fire elemental)"
    	elif rand <= 76:
    	    item['name'] = item['name'] + " (invisible stalker)"
    	elif rand <= 81:
    	    item['name'] = item['name'] + " (mezzodaemon)"
    	elif rand <= 85:
    	    item['name'] = item['name'] + " (night hag)"
    	elif rand <= 86:
    	    item['name'] = item['name'] + " (nycadaemon)"
    	elif rand <= 89:
    	    item['name'] = item['name'] + " (rakshasa)"
    	elif rand <= 93:
    	    item['name'] = item['name'] + " (salamander)"
    	elif rand <= 97:
    	    item['name'] = item['name'] + " (water elemental)"
    	elif rand <= 99:
    	    item['name'] = item['name'] + " (wind walker)"
    	elif rand <= 100:
    	    item['name'] = item['name'] + " (xorn)"
    else:
        item['name'] = item['name'] + " (empty)"

def get_jewel_type(item):
    rand = random.randint(10,100)
    item['gplo'] = int(item['gplo'])*rand
    item['name'] = item['name'] + " ({} faucets)".format(rand)
 
def get_medallion_type(item):
    rand = random.randint(1,20)
    item['xplo'] = interp(item['xplo'],item['xphi'],rand,100) 
    item['gplo'] = interp(item['gplo'],item['gphi'],rand,100) 
    if rand <=15:
        item['name'] = item['name'] + " (30')"
    elif rand <= 18:
        item['name'] = item['name'] + " (30'+ empathy)"
    elif rand <= 19:
        item['name'] = item['name'] + " (60')"
    elif rand <= 20:
        item['name'] = item['name'] + " (90')"
    
def get_missile_type(item):
    rand = random.randint(1,20)
    if rand <= 4:
        item['name'] = item['name'] + " (1x5HD,2x3)"
        item['gplo'] = int(item['gplo'])*11
        item['xplo'] = int(item['xplo'])*11
    elif rand <= 8:
        item['name'] = item['name'] + " (1x6HD,2x4,2x2)"
        item['gplo'] = int(item['gplo'])*18
        item['xplo'] = int(item['xplo'])*18
    elif rand <= 12:
        item['name'] = item['name'] + " (1x7HD,2x5,4x3)"
        item['gplo'] = int(item['gplo'])*29
        item['xplo'] = int(item['xplo'])*29
    elif rand <= 16:
        item['name'] = item['name'] + " (1x8HD,2x6,2x4,4x2)"
        item['gplo'] = int(item['gplo'])*36
        item['xplo'] = int(item['xplo'])*36
    elif rand <= 18:
        item['name'] = item['name'] + " (1x9HD,2x7,2x5,2x3)"
        item['gplo'] = int(item['gplo'])*39
        item['xplo'] = int(item['xplo'])*39
    elif rand <= 19:
        item['name'] = item['name'] + " (1x10HD,2x8,2x6,4x4)"
        item['gplo'] = int(item['gplo'])*54
        item['xplo'] = int(item['xplo'])*54
    elif rand <= 20:
        item['name'] = item['name'] + " (1x11HD,2x9,2x7,2x5,2x3)"
        item['gplo'] = int(item['gplo'])*59
        item['xplo'] = int(item['xplo'])*59
    
def get_prayer_type(item):
    rand = random.randint(3,6)
    for x in xrange(rand): 
        rand = random.randint(1,20)
        if rand <= 5:
            item['name'] = item['name'] + ", atonement"
        elif rand <=10: 
            item['name'] = item['name'] + ", blessing"
        elif rand <=15: 
            item['name'] = item['name'] + ", curing"
        elif rand <=17: 
            item['name'] = item['name'] + ", karma"
        elif rand <=18: 
            item['name'] = item['name'] + ", summons"
        elif rand <=20:
            item['name'] = item['name'] + ", wind walk"
    item['gplo'] = int(item['gplo'])*rand
    item['xplo'] = int(item['xplo'])*rand
 
def get_pigment_type(item):
    rand = random.randint(1,4)
    item['name'] = item['name'] + " (x{})".format(rand)
    item['gplo'] = int(item['gplo'])*rand
    item['xplo'] = int(item['xplo'])*rand
    
def get_pearl_type(item):
    rand = random.randint(1,100)
    if rand <= 25:
        item['name'] = item['name'] + " (1st lvl)"
    elif rand <=45: 
        item['name'] = item['name'] + " (2nd lvl)"
        item['gplo'] = int(item['gplo'])*2
        item['xplo'] = int(item['xplo'])*2
    elif rand <=60: 
        item['name'] = item['name'] + " (3rd lvl)"
        item['gplo'] = int(item['gplo'])*3
        item['xplo'] = int(item['xplo'])*3
    elif rand <=75: 
        item['name'] = item['name'] + " (4th lvl)"
        item['gplo'] = int(item['gplo'])*4
        item['xplo'] = int(item['xplo'])*4
    elif rand <=85: 
        item['name'] = item['name'] + " (5th lvl)"
        item['gplo'] = int(item['gplo'])*5
        item['xplo'] = int(item['xplo'])*5
    elif rand <=92: 
        item['name'] = item['name'] + " (6th lvl)"
        item['gplo'] = int(item['gplo'])*6
        item['xplo'] = int(item['xplo'])*6
    elif rand <=96: 
        item['name'] = item['name'] + " (7th lvl)"
        item['gplo'] = int(item['gplo'])*7
        item['xplo'] = int(item['xplo'])*7
    elif rand <=98: 
        item['name'] = item['name'] + " (8th lvl)"
        item['gplo'] = int(item['gplo'])*8
        item['xplo'] = int(item['xplo'])*8
    elif rand <=99: 
        item['name'] = item['name'] + " (9th lvl)"
        item['gplo'] = int(item['gplo'])*9
        item['xplo'] = int(item['xplo'])*9
    elif rand <=100: 
        rand1 = random.randin(1,6)
        item['name'] = item['name'] + " (2x{} lvl)".format(rand1)
        item['gplo'] = int(item['gplo'])*2*rand1
        item['xplo'] = int(item['xplo'])*2*rand1

def get_token_type(item):
    rand = random.randint(1,20)
    if rand <= 4:
        item['name'] = item['name'] + ", anchor"
    elif rand <= 7:
        item['name'] = item['name'] + ", bird"
    elif rand <= 10:
        item['name'] = item['name'] + ", fan"
    elif rand <= 13:
        item['name'] = item['name'] + ", swan boat"
    elif rand <= 18:
        item['name'] = item['name'] + ", tree"
    elif rand <= 20:
        item['name'] = item['name'] + ", whip"
    item['xplo'] = interp(item['xplo'],item['xphi'],rand,20) 
    item['gplo'] = interp(item['gplo'],item['gphi'],rand,20) 

def get_amulet_type(item):
    rand = random.randint(1,100)
    if rand <= 30:
        item['name'] = item['name'] + " (5th lvl)"
        item['gplo'] = int(item['gplo'])*5
        item['xplo'] = int(item['xplo'])*5
    elif rand <=55: 
        item['name'] = item['name'] + " (6th lvl)"
        item['gplo'] = int(item['gplo'])*6
        item['xplo'] = int(item['xplo'])*6
    elif rand <=75: 
        item['name'] = item['name'] + " (7th lvl)"
        item['gplo'] = int(item['gplo'])*7
        item['xplo'] = int(item['xplo'])*7
    elif rand <=90: 
        item['name'] = item['name'] + " (8th lvl)"
        item['gplo'] = int(item['gplo'])*8
        item['xplo'] = int(item['xplo'])*8
    elif rand <=100: 
        item['name'] = item['name'] + " (9th lvl)"
        item['gplo'] = int(item['gplo'])*9
        item['xplo'] = int(item['xplo'])*9
 
def get_bead_type(item):
    get_quantity(item,5,8)

def get_illusion_type(item):
    get_quantity(item,11,20)
 
def get_dust_type(item):
    rand = random.randint(13,24)
    item['name'] = item['name'] + " (x{})".format(rand)
    item['gplo'] = int(item['gplo'])*rand
    item['cnt'] = rand
    
def get_egg_type(item):
    rand = random.randint(1,20)
    if rand <= 4:
        item['name'] = item['name'] + " (black)"
        item['gplo'] = 5000
        item['xplo'] = 500
    elif rand <=8: 
        item['name'] = item['name'] + " (bone)"
        item['gplo'] = 1000
        item['xplo'] = 900 
    elif rand <=12: 
        item['name'] = item['name'] + " (crystal)"
        item['gplo'] = 9000
        item['xplo'] = 800
    elif rand <=16: 
        item['name'] = item['name'] + " (golden)"
        item['gplo'] = 4000
        item['xplo'] = 600
    elif rand <=20: 
        item['name'] = item['name'] + " (scarlet)"
        item['gplo'] = 3500
        item['xplo'] = 700
 
def get_scarab_type(item):
    rand = random.randint(1,100)
    if rand <= 30:
        item['name'] = item['name'] + " (flesh)"
        item['xplo'] = 400 
        item['gplo'] = 3200 
    elif rand <=55: 
        item['name'] = item['name'] + " (clay)"
        item['xplo'] = 500
        item['gplo'] = 3500
    elif rand <=75: 
        item['name'] = item['name'] + " (stone)"
        item['xplo'] = 600
        item['gplo'] = 4000 
    elif rand <=85: 
        item['name'] = item['name'] + " (iron)"
        item['xplo'] = 800
        item['gplo'] = 5000
    elif rand <=95: 
        item['name'] = item['name'] + " (flesh,clay,wood)"
        item['xplo'] = 900
        item['gplo'] = 6000
    elif rand <=100: 
        item['name'] = item['name'] + " (any)"
        item['xplo'] = 1250
        item['gplo'] = 12500 
    
def get_glue_type(item):
    get_quantity(item,1,10)
     
def get_case_type(item):
    rand = random.randint(1,20)
    if rand <= 3:
        item['name'] = item['name'] + " (2/day)"
        item['xplo'] = int(item['xplo'])*2
        item['gplo'] = int(item['gplo'])*2
    elif rand <= 6:
        item['name'] = item['name'] + " (3/day)"
        item['xplo'] = int(item['xplo'])*3
        item['gplo'] = int(item['gplo'])*3
    elif rand <= 10:
        item['name'] = item['name'] + " 4/day)"
        item['xplo'] = int(item['xplo'])*4
        item['gplo'] = int(item['gplo'])*4
    elif rand <= 15:
        item['name'] = item['name'] + " (5/day)"
        item['xplo'] = int(item['xplo'])*5
        item['gplo'] = int(item['gplo'])*5
    elif rand <= 19: 
        item['name'] = item['name'] + " (6/day)"
        item['xplo'] = int(item['xplo'])*6
        item['gplo'] = int(item['gplo'])*6
    elif rand <= 20: 
        item['name'] = item['name'] + " (7/day)"
        item['xplo'] = int(item['xplo'])*7
        item['gplo'] = int(item['gplo'])*7


def get_misc_girdle_type(item):
    rand = random.randint(1,100)
    item['xplo'] = interp(item['xplo'],item['xphi'],rand,100) 
    item['gplo'] = interp(item['gplo'],item['gphi'],rand,100) 
    if rand <= 30:
        item['name'] = item['name'] + ", hill"
    elif rand <= 50:
        item['name'] = item['name'] + ", stone"
    elif rand <= 70:
        item['name'] = item['name'] + ", frost"
    elif rand <= 85:
        item['name'] = item['name'] + ", fire"
    elif rand <= 95:
        item['name'] = item['name'] + ", cloud"
    elif rand <= 100:
        item['name'] = item['name'] + ", storm"
 

def get_misc_figurine_type(item):
    rand = random.randint(1,100)
    if rand <= 15:
        item['name'] = item['name'] + ", ebony fly"
        item['xplo'] = item['xplo'] * 4
        item['gplo'] = int(item['gplo'])  * 4
    elif rand <= 30:
        item['name'] = item['name'] + ", golden lions (pair)"
        item['xplo'] = item['xplo'] * 10
        item['gplo'] = int(item['gplo'])  * 10
    elif rand <= 40:
        item['name'] = item['name'] + ", ivory goats (trio)"
        item['xplo'] = item['xplo'] * 22 
        item['gplo'] = int(item['gplo'])  * 22
    elif rand <= 55:
        item['name'] = item['name'] + ", marble elephant"
        rand1 = random.randint(1,100)
        if rand1 <= 50:
            item['xplo'] = item['xplo'] * 10 
            item['gplo'] = int(item['gplo'])  * 10 
        elif rand1 <= 90:
            item['name'] = item['name'] + " (loxodont)"
            item['xplo'] = item['xplo'] * 11  
            item['gplo'] = int(item['gplo'])  * 11 
        elif rand1 <= 93:
            item['name'] = item['name'] + " (mammoth)"
            item['xplo'] = item['xplo'] * 13 
            item['gplo'] = int(item['gplo'])  * 13
        elif rand1 <= 100:
            item['name'] = item['name'] + " (mastodon)"
            item['xplo'] = item['xplo'] * 12 
            item['gplo'] = int(item['gplo'])  * 12
    elif rand <= 65:
        item['name'] = item['name'] + ", obsidian steed" 
        item['xplo'] = item['xplo'] * 6
        item['gplo'] = item['gplo'] * 6
    elif rand <= 85:
        item['name'] = item['name'] + ", onyx dog"
        item['xplo'] = item['xplo'] * 2
        item['gplo'] = int(item['gplo'])  * 2
    elif rand <= 100:
        item['name'] = item['name'] + ", serpentine owl"
        item['xplo'] = item['xplo'] * 4
        item['gplo'] = int(item['gplo'])  * 4
        
          
def get_misc_ball_type(item):
    rand = random.randint(1,100)
    if rand <= 50:
        pass
    elif rand <= 75:
        item['name'] = item['name'] + " with clairaudience"
        item['xplo'] = item['xplo'] * 2
        item['gplo'] = int(item['gplo']) * 2
    elif rand <= 90:
        item['name'] = item['name'] + " with ESP"
        item['xplo'] = item['xplo'] * 2
        item['gplo'] = int(item['gplo']) * 2
    elif rand <= 100:
        item['name'] = item['name'] + " with Telepathy"
        item['xplo'] = item['xplo'] * 2
        item['gplo'] = int(item['gplo']) * 2

def get_misc_cloak_type(item,rand=None):
    if not rand:
        rand = random.randint(1,100)
    logging.debug("Got random cloak {}".format(rand))
    if rand <= 45:
        item['name'] = item['name'] + " +1"
        item['xplo'] = item['xplo'] * 1
        item['gplo'] = int(item['gplo']) * 1
    elif rand <= 65:
        item['name'] = item['name'] + " +2"
        item['xplo'] = item['xplo'] * 2
        item['gplo'] = int(item['gplo']) * 2
    elif rand <= 85:
        item['name'] = item['name'] + " +3"
        item['xplo'] = item['xplo'] * 3
        item['gplo'] = int(item['gplo']) * 3
    elif rand <= 95:
        item['name'] = item['name'] + " +4"
        item['xplo'] = item['xplo'] * 4
        item['gplo'] = int(item['gplo']) * 4
    else:
        item['name'] = item['name'] + " +5"
        item['xplo'] = item['xplo'] * 5
        item['gplo'] = int(item['gplo']) * 5

def get_misc_purse_type(item):
    rand = random.randint(1,100)
    if rand <= 50:
        item['name'] = item['name'] + " (sp,ep,gp)"
        item['xplo'] = 1500
        item['gplo'] = 15000
    elif rand <= 90:
        item['name'] = item['name'] + " (cp,ep,pp)"
        item['xplo'] = 2500
        item['gplo'] = 25000
    elif rand <= 100:
        item['name'] = item['name'] + " (cp,ep,gems)"
        item['xplo'] = 4000
        item['gplo'] = 40000

def get_misc_bracer_type(item):
    rand = random.randint(1,100)
    if rand <= 5:
        item['name'] = item['name'] + " AC 8"
        offset = 2
    elif rand <= 15:
        item['name'] = item['name'] + " AC 7"
        offset = 3
    elif rand <= 35:
        item['name'] = item['name'] + " AC 6"
        offset = 4
    elif rand <= 50:
        item['name'] = item['name'] + " AC 5"
        offset = 5
    elif rand <= 70:
        item['name'] = item['name'] + " AC 4"
        offset = 6
    elif rand <= 85:
        item['name'] = item['name'] + " AC 3"
        offset = 7
    elif rand <= 100:
        item['name'] = item['name'] + " AC 2"
        offset = 8
    item['xplo'] = offset * item['xplo']
    item['gplo'] = offset * int(item['gplo']) 
