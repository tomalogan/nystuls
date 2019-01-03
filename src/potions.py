#!/usr/bin/python
import random
import logging
from interp import interp


def set_potion_subtype(item): 
    # need to set a specific type
    if item['name'] == 'Animal Control':
        get_animal_type_for_potion(item)
    elif item['name'] == 'Dragon Control':
        get_dragon_type_for_potion(item)
    elif item['name'] == 'Giant Control':
        get_giant_type_for_potion(item)
    elif item['name'] == 'Giant Strength (F)':
        get_giant_strength_for_potion(item)
    elif item['name'] == 'Human Control':
        get_human_type_for_potion(item)
    elif item['name'] == 'Undead Control':
        get_undead_type_for_potion(item)
    elif item['name'] == 'Oil of Sharpness (per app)':
        get_oil_sharpness_type(item)

def get_animal_type_for_potion(item):
    rand = random.randint(1,20)
    if rand <= 4 : 
        item['name'] = item['name']+" (mammal/marsupial)"
    elif rand <= 8:
        item['name'] = item['name']+" (avian)"
    elif rand <= 12:
        item['name'] = item['name']+" (reptile/amphibian)"
    elif rand <= 15:
        item['name'] = item['name']+" (fish)"
    elif rand <= 17:
        item['name'] = item['name']+" (mammal/marsupial/avian)"
    elif rand <= 19:
        item['name'] = item['name']+" (reptile/amphibian/fish)"
    elif rand == 20:
        item['name'] = item['name']+" (all)"

def get_dragon_type_for_potion(item):
    rand = random.randint(1,20)
    item['xplo'] = interp(item['xplo'],item['xphi'],rand,20) 
    item['gplo'] = interp(item['gplo'],item['gphi'],rand,20) 
    if rand <= 2: 
        item['name'] = item['name']+" (white)"
    elif rand <= 4:
        item['name'] = item['name']+" (black)"
    elif rand <= 7:
        item['name'] = item['name']+" (green)"
    elif rand <= 9:
        item['name'] = item['name']+" (blue)"
    elif rand <= 10:
        item['name'] = item['name']+" (red)"
    elif rand <= 12:
        item['name'] = item['name']+" (brass)"
    elif rand <= 14:
        item['name'] = item['name']+" (copper)"
    elif rand <= 15:
        item['name'] = item['name']+" (bronze)"
    elif rand <= 16:
        item['name'] = item['name']+" (silver)"
    elif rand <= 17:
        item['xplo'] = item['xphi']
        item['gplo'] = item['gphi']
        item['name'] = item['name']+" (gold)"
    elif rand <= 19:
        item['xplo'] = item['xphi']
        item['gplo'] = item['gphi']
        item['name'] = item['name']+" (evil)"
    elif rand <= 20:
        item['xplo'] = item['xphi']
        item['gplo'] = item['gphi']
        item['name'] = item['name']+" (good)"

def get_giant_type_for_potion(item):
    rand = random.randint(1,20)
    item['xplo'] = interp(item['xplo'],item['xphi'],rand,20) 
    item['gplo'] = interp(item['gplo'],item['gphi'],rand,20) 
    if rand <= 5: 
        item['name'] = item['name']+" (hill)"
    elif rand <= 9:
        item['name'] = item['name']+" (stone)"
    elif rand <= 13:
        item['name'] = item['name']+" (frost)"
    elif rand <= 17:
        item['name'] = item['name']+" (fire)"
    elif rand <= 19:
        item['name'] = item['name']+" (cloud)"
    elif rand == 20:
        item['name'] = item['name']+" (storm)"

def get_giant_strength_for_potion(item):
    rand = random.randint(1,20)
    item['xplo'] = interp(item['xplo'],item['xphi'],rand,20) 
    item['gplo'] = interp(item['gplo'],item['gphi'],rand,20) 
    if rand <= 6: 
        item['name'] = item['name']+" (hill)"
    elif rand <= 10:
        item['name'] = item['name']+" (stone)"
    elif rand <= 14:
        item['name'] = item['name']+" (frost)"
    elif rand <= 17:
        item['name'] = item['name']+" (fire)"
    elif rand <= 19:
        item['name'] = item['name']+" (cloud)"
    elif rand == 20:
        item['name'] = item['name']+" (storm)"

def get_human_type_for_potion(item):
    rand = random.randint(1,20)
    if rand <= 2: 
        item['name'] = item['name']+" (dwarves)"
    elif rand <= 4:
        item['name'] = item['name']+" (elves/half-elves)"
    elif rand <= 6:
        item['name'] = item['name']+" (gnomes)"
    elif rand <= 8:
        item['name'] = item['name']+" (halflings)"
    elif rand <= 10:
        item['name'] = item['name']+" (half-orcs)"
    elif rand <= 16:
        item['name'] = item['name']+" (humans)"
    elif rand <= 19:
        item['name'] = item['name']+" (Humanoids)"
    elif rand <= 20:
        item['name'] = item['name']+" (Elves, Half-Elves, Humans)"


def get_undead_type_for_potion(item):
    rand = random.randint(1,10)
    if rand <= 1: 
        item['name'] = item['name']+" (ghasts)"
    elif rand <= 2:
        item['name'] = item['name']+" (ghosts)"
    elif rand <= 3:
        item['name'] = item['name']+" (ghouls)"
    elif rand <= 4:
        item['name'] = item['name']+" (shadows)"
    elif rand <= 5:
        item['name'] = item['name']+" (skeletons)"
    elif rand <= 6:
        item['name'] = item['name']+" (spectres)"
    elif rand <= 7:
        item['name'] = item['name']+" (wights)"
    elif rand <= 8:
        item['name'] = item['name']+" (wraiths)"
    elif rand <= 9:
        item['name'] = item['name']+" (vampires)"
    elif rand <= 10:
        item['name'] = item['name']+" (zombies)"

def get_oil_sharpness_type(item):
    rand = random.randint(1,20)
    if rand <= 2: 
        item['name'] = item['name']+" (+1)"
    elif rand <= 5:
        item['name'] = item['name']+" (+2)"
        item['gplo'] = int(item['gplo']) * 2
    elif rand <= 11:
        item['name'] = item['name']+" (+3)"
        item['gplo'] = int(item['gplo']) * 3
    elif rand <= 16:
        item['name'] = item['name']+" (+4)"
        item['gplo'] = int(item['gplo']) * 4
    elif rand <= 19:
        item['name'] = item['name']+" (+5)"
        item['gplo'] = int(item['gplo']) * 5
    elif rand <= 20:
        item['name'] = item['name']+" (+6)"
        item['gplo'] = int(item['gplo']) * 6
    rand = random.randint(3,5)
    item['name'] = item['name'] + ' {} apps'.format(rand)
