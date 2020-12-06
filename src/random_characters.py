#!/usr/bin/python

import argparse
from argparse import ArgumentDefaultsHelpFormatter
import os, sys
import random
import logging
import textwrap
from utils import *
from drow import *
from equip import *

# Data tables indexed by class_num
classes = ["Cleric", "Druid", "Fighter", "Paladin", "Ranger", "Magic-User", "Illusionist", "Thief",
           "Assassin", "Monk", "CA", "CF", "CM", "CR", "CT", "CFM", "FA", "FI", "FM", "FT", "FMT", "IT", "MT"]
multi_classes = ["CA", "CF", "CM", "CR", "CT", "CFM", "FA", "FI", "FM", "FT", "FMT", "IT", "MT"]

hitdice = [8, 8, 10, 10, 10, 4, 4, 6, 6, 4, 10, 8, 0]
maxhd = [9, 14, 9, 9, 11, 11, 10, 10, 15, 18, 9, 9, 0]
min_abilities = [[3, 3, 9, 3, 3, 3],
                 [3, 3, 12, 3, 3, 15],
                 [9, 3, 3, 3, 3, 3],
                 [12, 9, 13, 3, 9, 17],
                 [13, 13, 14, 3, 14, 3],
                 [3, 9, 3, 6, 3, 3],
                 [3, 15, 3, 16, 3, 3],
                 [3, 3, 3, 9, 3, 3],
                 [12, 11, 3, 12, 3, 3],
                 [15, 3, 15, 15, 11, 3]]
extrahp = [2, 0, 3, 3, 2, 1, 1, 2, 0, 0, 3, 2, 0]

# Other data tables
races = ["Dwarf", "Elf", "Gnome", "Half-Elf", "Halfling", "Half-Orc", "Human", "Drow"]
race_class_allowed = [[True, False, True, False, False, False, False, True, True, False, False, False,
                       False, False, False, False, False, False, False, True, False, False, False],
                      [True, True, True, False, True, True, False, True, True, False, False, False,
                       False, False, False, False, False, False, True, True, True, False, True],
                      [True, False, True, False, False, False, True, True, True, False, False, False,
                       False, False, False, False, False, True, False, True, False, True, False],
                      [True, True, True, True, True, True, False, True, True, False, False, True,
                       True, True, False, True, False, False, True, True, True, False, True],
                      [True, True, True, False, False, False, False, True, False, False, False, False,
                       False, False, False, False, False, False, False, True, False, False, False],
                      [True, False, True, False, False, False, False, True, True, False, True, True,
                       False, False, True, False, True, False, False, True, False, False, False],
                      [True, True, True, True, True, True, True, True, True, True, False, False, False,
                       False, False, False, False, False, False, False, False, False, False],
                      [True, False, True, False, True, True, False, True, True, False, False, True,
                       False, True, False, False, False, False, True, False, False, False, False]]

race_class_ability_limits = [[[8, 0, 7, 0, 0, 0, 0, 100, 9, 0],  # dwarf 9
                              [8, 0, 7, 0, 0, 0, 0, 100, 9, 0],
                              [8, 0, 7, 0, 0, 0, 0, 100, 9, 0],
                              [8, 0, 7, 0, 0, 0, 0, 100, 9, 0],
                              [8, 0, 7, 0, 0, 0, 0, 100, 9, 0],
                              [8, 0, 7, 0, 0, 0, 0, 100, 9, 0],
                              [8, 0, 7, 0, 0, 0, 0, 100, 9, 0],
                              [9, 0, 7, 0, 0, 0, 0, 100, 9, 0],
                              [10, 0, 8, 0, 0, 0, 0, 100, 9, 0],
                              [11, 0, 9, 0, 0, 0, 0, 100, 9, 0]],  # dwarf 18
                             [[7, 100, 5, 0, 0, 9, 0, 100, 10, 0],  # elf 9
                              [7, 100, 5, 0, 0, 9, 0, 100, 10, 0],
                              [7, 100, 5, 0, 0, 9, 0, 100, 10, 0],
                              [7, 100, 5, 0, 0, 9, 0, 100, 10, 0],
                              [7, 100, 5, 0, 0, 9, 0, 100, 10, 0],
                              [7, 100, 5, 0, 0, 9, 0, 100, 10, 0],
                              [7, 100, 5, 0, 0, 9, 0, 100, 10, 0],
                              [8, 100, 5, 0, 0, 9, 0, 100, 10, 0],
                              [9, 100, 5, 0, 0, 10, 0, 100, 10, 0],
                              [10, 100, 6, 0, 0, 11, 0, 100, 10, 0]],  # elf 18
                             [[7, 0, 5, 0, 0, 0, 6, 100, 8, 0],  # gnome 9
                              [7, 0, 5, 0, 0, 0, 6, 100, 8, 0],
                              [7, 0, 5, 0, 0, 0, 6, 100, 8, 0],
                              [7, 0, 5, 0, 0, 0, 6, 100, 8, 0],
                              [7, 0, 5, 0, 0, 0, 6, 100, 8, 0],
                              [7, 0, 5, 0, 0, 0, 6, 100, 8, 0],
                              [7, 0, 5, 0, 0, 0, 6, 100, 8, 0],
                              [8, 0, 5, 0, 0, 0, 6, 100, 8, 0],
                              [9, 0, 5, 0, 0, 0, 6, 100, 8, 0],
                              [10, 0, 6, 0, 0, 0, 7, 100, 8, 0]],  # gnome 18
                             [[5, 100, 6, 0, 6, 7, 0, 100, 11, 0],  # half-elf 9
                              [5, 100, 6, 0, 6, 7, 0, 100, 11, 0],
                              [5, 100, 6, 0, 6, 7, 0, 100, 11, 0],
                              [5, 100, 6, 0, 6, 7, 0, 100, 11, 0],
                              [5, 100, 6, 0, 6, 7, 0, 100, 11, 0],
                              [5, 100, 6, 0, 6, 7, 0, 100, 11, 0],
                              [5, 100, 6, 0, 6, 7, 0, 100, 11, 0],
                              [6, 100, 6, 0, 6, 7, 0, 100, 11, 0],
                              [7, 100, 7, 0, 7, 7, 0, 100, 11, 0],
                              [8, 100, 7, 0, 8, 8, 0, 100, 11, 0]],  # half-elf 18
                             [[4, 6, 4, 0, 0, 0, 0, 100, 0, 0],  # halfling 9
                              [4, 6, 4, 0, 0, 0, 0, 100, 0, 0],
                              [4, 6, 4, 0, 0, 0, 0, 100, 0, 0],
                              [4, 6, 4, 0, 0, 0, 0, 100, 0, 0],
                              [4, 6, 4, 0, 0, 0, 0, 100, 0, 0],
                              [4, 6, 4, 0, 0, 0, 0, 100, 0, 0],
                              [4, 6, 4, 0, 0, 0, 0, 100, 0, 0],
                              [4, 7, 4, 0, 0, 0, 0, 100, 0, 0],
                              [5, 9, 5, 0, 0, 0, 0, 100, 0, 0],
                              [6, 11, 6, 0, 0, 0, 0, 100, 0, 0]],  # halfling 18
                             [[4, 0, 10, 0, 0, 0, 0, 8, 100, 0],  # half-orc 9
                              [4, 0, 10, 0, 0, 0, 0, 8, 100, 0],
                              [4, 0, 10, 0, 0, 0, 0, 8, 100, 0],
                              [4, 0, 10, 0, 0, 0, 0, 8, 100, 0],
                              [4, 0, 10, 0, 0, 0, 0, 8, 100, 0],
                              [4, 0, 10, 0, 0, 0, 0, 8, 100, 0],
                              [5, 0, 10, 0, 0, 0, 0, 9, 100, 0],
                              [6, 0, 10, 0, 0, 0, 0, 10, 100, 0],
                              [7, 0, 10, 0, 0, 0, 0, 11, 100, 0],
                              [7, 0, 10, 0, 0, 0, 0, 11, 100, 0]],  # half-orc 18
                             [[100, 100, 100, 100, 100, 100, 100, 100, 100, 100],  # human 9
                              [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                              [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                              [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                              [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                              [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                              [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                              [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                              [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                              [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]],  # human 18
                             [[100, 0, 9, 0, 0, 0, 0, 100, 0, 0],  # drow 9
                              [100, 0, 9, 0, 0, 12, 0, 100, 0, 0],
                              [100, 0, 9, 0, 0, 12, 0, 100, 0, 0],
                              [100, 0, 9, 0, 0, 12, 0, 100, 0, 0],
                              [100, 0, 10, 0, 0, 12, 0, 100, 0, 0],
                              [100, 0, 11, 0, 0, 12, 0, 100, 0, 0],
                              [100, 0, 12, 0, 0, 12, 0, 100, 0, 0],
                              [100, 0, 12, 0, 0, 12, 0, 100, 0, 0],
                              [100, 0, 12, 0, 0, 12, 0, 100, 0, 0],
                              [100, 0, 12, 0, 0, 12, 0, 100, 0, 0]]]  # drow 18

ability_types = ['strength', 'intelligence', 'wisdom', 'dexterity', 'constitution', 'charisma']

# Number of dice to roll to generate abilities for each character type
dice = {}
dice['Cleric'] = [7, 4, 9, 5, 8, 6]
dice['Druid'] = [7, 4, 8, 5, 6, 9]
dice['Fighter'] = [9, 3, 5, 7, 8, 6]
dice['Paladin'] = [7, 5, 8, 3, 6, 9]
dice['Ranger'] = [7, 6, 8, 5, 9, 4]
dice['Magic-User'] = [4, 9, 7, 8, 6, 5]
dice['Illusionist'] = [3, 8, 7, 9, 5, 6]
dice['Thief'] = [6, 5, 3, 9, 7, 4]
dice['Assassin'] = [6, 7, 4, 9, 7, 4]
dice['Monk'] = [7, 5, 9, 8, 6, 4]
dice['CA'] = [7, 7, 9, 9, 8, 6]
dice['CF'] = [9, 4, 9, 7, 8, 6]
dice['CM'] = [7, 9, 9, 8, 8, 6]
dice['CR'] = [7, 6, 9, 5, 9, 6]
dice['CT'] = [7, 5, 9, 9, 8, 6]
dice['CFM'] = [9, 9, 9, 8, 8, 6]
dice['FA'] = [9, 7, 5, 9, 8, 6]
dice['FI'] = [9, 8, 7, 9, 8, 6]
dice['FM'] = [9, 9, 7, 8, 8, 6]
dice['FT'] = [9, 5, 5, 9, 8, 6]
dice['FMT'] = [9, 9, 7, 9, 8, 6]
dice['IT'] = [6, 8, 7, 9, 7, 4]
dice['MT'] = [6, 9, 7, 9, 7, 4]


def best_of(dice):
    nums = []
    for x in xrange(dice):
        nums.append(random.randint(1, 6))
    nums = sorted(nums, reverse=True)
    result = nums[0] + nums[1] + nums[2]
    return (result)


def get_hp_level(level, hd, class_num=None, class_name=None):
    if class_num is None:
        class_num = classes.index(class_name)
    hp = 0
    for x in xrange(int(level)):
        if hd < maxhd[class_num]:
            hp_add = random.randint(3, hitdice[class_num])
            hd = hd + 1
        else:
            hp_add = int(extrahp[class_num])
        hp = hp + hp_add
        logging.debug("Rolled {} for hitpoints for level {}".format(hp_add, x))
    logging.debug("Rolled hit points of {}".format(hp))
    return int(hp)


def get_con_bonus(con, name, level):
    hp = 0
    if con > 14:
        bonus = con - 14
        if bonus > 2 and not (name == 'Fighter' or name == 'Ranger' or name == 'Paladin'):
            bonus = 2
        hp = bonus * int(level)
    logging.debug("Con bonus is {}".format(hp))
    return int(hp)


def get_hp(c):
    hp = 0
    hd = 0
    bonus = 0
    if c['class'] == 'Monk' or c['class'] == 'Ranger':
        logging.debug("Rolling initial die for special class {}".format(c['class']))
        hp = hp + random.randint(3, hitdice[c['class_num']])
        hd = hd + 1

    for x in xrange(c['class_cnt']):
        class_name = c['classes'][x]
        logging.debug("Rolling hit points for class {}".format(class_name))
        level = c['class_lvl'][x]
        hp = hp + get_hp_level(level, hd, class_name=class_name)
        logging.debug("For {} of level {} total HP is {}".format(class_name, level, hp))
        bonus = bonus + get_con_bonus(c['constitution'], class_name, level)
    hp = (hp + bonus) / c['class_cnt']
    logging.debug("Got bonus of {} to get total {}".format(bonus, hp))
    return (hp)


def get_abilities(character):
    for x in xrange(len(ability_types)):
        ability = ability_types[x]
        character[ability] = best_of(dice[character['class']][x])
        if character[ability] < min_abilities[character['class_num']][x]:
            character[ability] = min_abilities[character['class_num']][x]
        logging.debug("Ability {} score is {}".format(ability, character[ability]))

    # Set tohit/todam
    if character['strength'] == 16:
        character['todam'] = character['todam'] + 1
    elif character['strength'] == 17:
        character['tohit'] = 1
        character['todam'] = 1
    elif character['strength'] == 18:
        character['tohit'] = 1
        character['todam'] = 2


def fix_level(c):
    for x in xrange(c['class_cnt']):
        logging.debug("Class cnt is {}; class levels are {}".format(c['class_cnt'], c['class_lvl']))
        level = c['class_lvl'][x]
        logging.debug("Found level of {}".format(level))
        maxlvl = get_level_limit(c, x)
        logging.debug("Maximum level is {}".format(maxlvl))
        if maxlvl:
            newlvl = min(level, maxlvl)
            if int(newlvl) < int(level):
                logging.debug("Racial level maximum exceeded; reset to {}".format(newlvl))
                c['class_lvl'][x] = newlvl
    str = ""
    for x in xrange(c['class_cnt']):
        str = str + "{}/".format(c['class_lvl'][x])
    c['level'] = str[0:len(str) - 1]


def get_ability_for_class(class_name):
    if class_name == "Cleric" or class_name == "Druid":
        return ('wisdom')
    elif class_name == 'Fighter' or class_name == 'Ranger' or class_name == 'Paladin':
        return ('strength')
    elif class_name == 'Magic-User' or class_name == 'Illusionist' or class_name == "Monk":
        return ('intelligence')
    elif class_name == 'Thief' or class_name == 'Assassin':
        return ('dexterity')


def get_level_limit(c, x):
    race = c['race']
    logging.debug("Looking for class {} out of {}".format(x, c['class_cnt']))
    class_name = c['classes'][x]
    race_num = races.index(race)
    class_num = classes.index(class_name)
    logging.debug("Getting primary ability for {}".format(class_name))
    ability = get_ability_for_class(class_name)
    logging.debug("Ability to check is {}".format(ability))
    ability_num = c[ability] - 9
    logging.debug("Ability look up is {}".format(ability_num))
    logging.debug("race_num is {}; ability_num is {}; class_num is {}".format(race_num, ability_num, class_num))
    logging.debug("Size of table is {}".format(len(race_class_ability_limits)))
    ret = race_class_ability_limits[race_num][ability_num][class_num]
    return (ret)


def set_fighter_abilities(character):
    if "F" in character['class']:
        level = int(get_character_level(character, name="Fighter"))
    else:
        level = int(get_character_level(character, name=character['class']))

    logging.debug("Got fighter level of {}".format(level))
    # Boost strength based upon level
    if (character['strength'] < 18):
        if level >= 7:
            logging.debug("Boosting strength!")
            character['strength'] = character['strength'] + 1
        if level >= 11:
            logging.debug("Boosting strength!")
            character['strength'] = character['strength'] + 1
        if level >= 14:
            logging.debug("Boosting strength!")
            character['strength'] = character['strength'] + 1
        if character['strength'] > 19:
            character['strength'] = 19

    # Set strength percent score
    if character['strength'] == 16:
        character['todam'] = character['todam'] + 1
    elif character['strength'] == 17:
        character['tohit'] = 1
        character['todam'] = 1
    elif character['strength'] == 18:
        pct = random.randint(1, 100)
        adder = int(level) * 3
        pct = pct + adder
        if pct >= 100:
            character['strength'] = "18/00"
        else:
            character['strength'] = "18/{}".format(pct)
        if pct <= 50:
            character['tohit'] = 1
            character['todam'] = 3
        elif pct <= 75:
            character['tohit'] = 2
            character['todam'] = 3
        elif pct <= 90:
            character['tohit'] = 2
            character['todam'] = 4
        elif pct <= 99:
            character['tohit'] = 2
            character['todam'] = 5
        elif pct >= 100:
            character['tohit'] = 3
            character['todam'] = 6
    elif character['strength'] == 19:
        character['tohit'] = 3
        character['todam'] = 7

    # Set number of attacks based upon melee specialization
    if character['class'] == "Fighter" or character['class'] == "Ranger" or character['class'] == "Paladin":
        if level < 7:
            character['numatt'] = 1.5
        elif level < 13:
            character['numatt'] = 2.0
        else:
            character['numatt'] = 2.5


def init_character():
    c = {}
    c['race'] = None
    c['classes'] = []
    c['class_lvl'] = []
    c['class_cnt'] = 0
    c['strength'] = 3
    c['intelligence'] = 3
    c['wisdom'] = 3
    c['dexterity'] = 3
    c['constitution'] = 3
    c['charisma'] = 3
    c['multi'] = False
    c['level'] = 1
    c['hp'] = 0
    c['stuff'] = []
    c['tohit'] = 0
    c['todam'] = 0
    c['numatt'] = 1
    c['armor'] = None
    c['shield'] = None
    c['weapons'] = []
    return c


def get_ac(c):
    ac = 10
    if c['armor'] is not None:
        a = c['armor']
        logging.debug("Armor type is {}".format(a))

        # Set armor type
        if "Leather" in a or "Padded" in a:
            ac = 8
        elif "Studded Leather" in a or "Ring Mail" in a:
            ac = 7
        elif "Scale Mail" in a:
            ac = 6
        elif "Chain Mail" in a or "Elfin Chain" in a:
            ac = 5
        elif "Splint Mail" in a or "Banded Mail" in a or "Bronze Plate Mail" in a:
            ac = 4
        elif "Plate Mail" in a:
            ac = 3
        elif "Field" in a:
            ac = 2
        elif "Full" in a:
            ac = 1

        # Determine plus if any
        if "+" in a:
            pos = a.index("+")
            plus = a[pos + 1]
            logging.debug("Armor plus is {}".format(plus))
            ac = ac - int(plus)

        if "Bracers of Defense" in a:
            # Determine strength 
            if "AC" in a:
                pos = a.index("C")
                plus = a[pos + 2]
                logging.debug("Bracer strength is {}".format(plus))
                ac = int(plus)
        logging.debug("Base AC is {}".format(ac))

    if c['shield'] is not None:
        logging.debug("Shield is {}".format(c['shield']))
        ac = ac - 1
        # Determine plus if any
        a = c['shield']
        if "+" in a:
            pos = a.index("+")
            plus = a[pos + 1]
            ac = ac - int(plus)
        logging.debug("AC with shield is {}".format(ac))
    if c['dexterity'] > 14:
        ac_bonus = c['dexterity'] - 14
        logging.debug("Dexterity bonus is {}".format(ac_bonus))
        ac = ac - ac_bonus

    for item in c['stuff']:
        if "Protection" in item['name']:
            a = c['armor']
            if a:
                if "Bracers" in a or "Leather" in a:
                    if "+" in item['name']:
                        pos = item['name'].index("+")
                        plus = item['name'][pos + 1]
                        ac = ac - int(plus)
            else:
                if "+" in item['name']:
                    pos = item['name'].index("+")
                    plus = item['name'][pos + 1]
                    ac = ac - int(plus)

    if ac < -10:
        ac = -10
    return (ac)


def add_weapon_to_hit(c):
    l = c['weapons']
    plus = 0
    for i in l:
        if "+" in i['name']:
            pos = i['name'].index("+")
            plus = max(int(i['name'][pos + 1]), int(plus))
    logging.debug("Found weapon plus of {}".format(plus))
    c['tohit'] = c['tohit'] + plus
    c['todam'] = c['todam'] + plus


def Print_Character(c, cnt):
    numatt = int(c['numatt'])
    if numatt != c['numatt']:
        numatt = c['numatt'] * 2
        numatt_str = "{}/2".format(int(numatt))
    else:
        numatt_str = "{}".format(numatt)

    if cnt:
        logging.info("({}) {},{},Lvl:{},AC:{},HP:{},S:{},I:{},W:{},D:{},C:{},Ch:{},#A:{}(+{}/+{})".
                     format(cnt, c['class'], c['race'], c['level'], c['ac'], c['hp'], c['strength'], c['intelligence'],
                            c['wisdom'], c['dexterity'], c['constitution'], c['charisma'], numatt_str, c['tohit'],
                            c['todam']))
    else:
        logging.info("{},{},Lvl:{},AC:{},HP:{},S:{},I:{},W:{},D:{},C:{},Ch:{},#A:{}(+{}/+{})".
                     format(c['class'], c['race'], c['level'], c['ac'], c['hp'], c['strength'], c['intelligence'],
                            c['wisdom'], c['dexterity'], c['constitution'], c['charisma'], numatt_str, c['tohit'],
                            c['todam']))

    weapons = ""
    if len(c['weapons']) > 0:
        for i in xrange(len(c['weapons']) - 1):
            weapons = weapons + c['weapons'][i]['name']
            if c['weapons'][i]['cnt'] > 1:
                weapons = weapons + "(x{})".format(c['weapons'][i]['cnt'])
            weapons = weapons + ","
        weapons = weapons + c['weapons'][-1]['name']
        if c['weapons'][-1]['cnt'] > 1:
            weapons = weapons + "(x{})".format(c['weapons'][-1]['cnt'])

    stuff = ""
    if len(c['stuff']) > 0:
        for i in xrange(len(c['stuff']) - 1):
            stuff = stuff + c['stuff'][i]['name']
            if c['stuff'][i]['cnt'] > 1:
                stuff = stuff + "(x{})".format(c['stuff'][i]['cnt'])
            stuff = stuff + ","
        stuff = stuff + c['stuff'][-1]['name']
        if c['stuff'][-1]['cnt'] > 1:
            stuff = stuff + "(x{})".format(c['stuff'][-1]['cnt'])

    out = ""
    if c['armor']:
        out = out + "{},".format(c['armor'])
    if c['shield']:
        out = out + "{},".format(c['shield'])
    if len(c['weapons']) > 0:
        out = out + weapons
    if len(c['stuff']) > 0:
        out = out + "," + stuff

    wrapper = textwrap.TextWrapper(initial_indent="\t", width=72, subsequent_indent="\t")
    out = wrapper.fill(out)
    logging.info("{}".format(out))


random_classes = ["Druid", "Paladin", "Ranger", "Illusionist", "Assassin", "Monk"]
random_multiclasses = ["CA", "CF", "CM", "CR", "CT", "CFM", "FA", "FI", "FM", "FT", "FMT", "IT", "MT"]


def get_non_Drow_NPC_race(class_name):
    race_num = random.randint(0, len(races) - 1)
    class_num = classes.index(class_name)
    while not race_class_allowed[race_num][class_num] or races[race_num] == "Drow":
        race_num = random.randint(0, len(races) - 1)
    race = races[race_num]
    return (race)


def create_NPC_party(level=5, race=None):
    fighters = random.randint(2, 3)
    for x in xrange(fighters):
        if not race:
            tmp_race = get_non_Drow_NPC_race("Fighter")
        else:
            tmp_race = race
        generate_character(tables, class_name="Fighter", level=level, race=tmp_race)

    clerics = random.randint(1, 2)
    for x in xrange(clerics):
        if not race:
            tmp_race = get_non_Drow_NPC_race("Cleric")
        else:
            tmp_race = race
        generate_character(tables, class_name="Cleric", level=level, race=tmp_race)

    if not race:
        tmp_race = get_non_Drow_NPC_race("Magic-User")
    else:
        tmp_race = race
    generate_character(tables, class_name="Magic-User", level=level, race=tmp_race)

    if not race:
        tmp_race = get_non_Drow_NPC_race("Thief")
    else:
        tmp_race = race
    generate_character(tables, class_name="Thief", level=level, race=tmp_race)

    pct = random.randint(1, 100)
    if pct > 25:
        generate_random_class(tables, random_multiclasses, level=level)
    if pct > 50:
        generate_random_class(tables, random_classes, level=level)
    if pct > 75:
        generate_random_class(tables, random_multiclasses, level=level)


def generate_random_class(tables, rand_table, level=5):
    this_class_num = random.randint(0, len(rand_table) - 1)
    logging.debug("rand_table is {}".format(rand_table))
    logging.debug("this_class_num is {}".format(this_class_num))
    class_num = classes.index(rand_table[this_class_num])
    race_num = random.randint(0, len(races) - 1)
    while not race_class_allowed[race_num][class_num] or races[race_num] == "Drow":
        race_num = random.randint(0, len(races) - 1)
    race = races[race_num]
    this_class = classes[class_num]
    generate_character(tables, class_name=this_class, race=race, level=level)


def create_DrowPatrol():
    lackeys = random.randint(4, 12)
    cnt = 1
    pct = random.randint(1, 100)
    if pct >= 90:
        generate_character(tables, class_name="FM", race="Drow", cnt=cnt)
        cnt = cnt + 1
    if lackeys <= 6:
        levels = 4
        generate_character(tables, class_name="Fighter", race="Drow", level=random.randint(7, 9), cnt=cnt)
        cnt = cnt + 1
    elif lackeys <= 9:
        levels = 3
        generate_character(tables, class_name="Fighter", level=random.randint(5, 7), race="Drow", cnt=cnt)
        cnt = cnt + 1
        generate_character(tables, class_name="Fighter", level=random.randint(5, 7), race="Drow", cnt=cnt)
        cnt = cnt + 1
    else:
        levels = 2
        generate_character(tables, class_name="Fighter", level=random.randint(4, 5), race="Drow", cnt=cnt)
        cnt = cnt + 1
        generate_character(tables, class_name="Fighter", level=random.randint(4, 5), race="Drow", cnt=cnt)
        cnt = cnt + 1
        generate_character(tables, class_name="Fighter", level=random.randint(7, 9), race="Drow", cnt=cnt)
        cnt = cnt + 1
    for x in xrange(lackeys):
        generate_character(tables, class_name="Fighter", level=levels, race="Drow", cnt=cnt)
        cnt = cnt + 1


def create_DrowParty():
    lackeys = random.randint(6, 18)
    cnt = 1
    generate_character(tables, class_name="FM", race="Drow", cnt=cnt)
    cnt = cnt + 1
    generate_character(tables, class_name="Cleric", race="Drow", cnt=cnt)
    cnt = cnt + 1
    if lackeys <= 6:
        levels = 4
        generate_character(tables, class_name="Fighter", race="Drow", level=random.randint(7, 9), cnt=cnt)
        cnt = cnt + 1
    elif lackeys <= 9:
        levels = 3
        generate_character(tables, class_name="Fighter", race="Drow", level=random.randint(5, 7), cnt=cnt)
        cnt = cnt + 1
        generate_character(tables, class_name="Fighter", race="Drow", level=random.randint(5, 7), cnt=cnt)
        cnt = cnt + 1
    else:
        levels = 2
        generate_character(tables, class_name="Fighter", race="Drow", level=random.randint(4, 5), cnt=cnt)
        cnt = cnt + 1
        generate_character(tables, class_name="Fighter", race="Drow", level=random.randint(4, 5), cnt=cnt)
        cnt = cnt + 1
        generate_character(tables, class_name="Fighter", race="Drow", level=random.randint(7, 9), cnt=cnt)
        cnt = cnt + 1
    for x in xrange(lackeys):
        generate_character(tables, class_name="Fighter", race="Drow", level=levels, cnt=cnt)
        cnt = cnt + 1


def init_multi_level():
    for myclass in multi_classes:
        mins = [3, 3, 3, 3, 3, 3]
        if "A" in myclass:
            mins = map(max, zip(mins, min_abilities[classes.index("Assassin")]))
        if "C" in myclass:
            mins = map(max, zip(mins, min_abilities[classes.index("Cleric")]))
        if "F" in myclass:
            mins = map(max, zip(mins, min_abilities[classes.index("Fighter")]))
        if "I" in myclass:
            mins = map(max, zip(mins, min_abilities[classes.index("Illusionist")]))
        if "M" in myclass:
            mins = map(max, zip(mins, min_abilities[classes.index("Magic-User")]))
        if "R" in myclass:
            mins = map(max, zip(mins, min_abilities[classes.index("Ranger")]))
        if "T" in myclass:
            mins = map(max, zip(mins, min_abilities[classes.index("Thief")]))
        min_abilities.append(mins)
        logging.debug("Calculated min abilities for {} to be {}".format(myclass, mins))


def generate_character(tables, class_name=None, level=None, race=None, cnt=None):
    character = init_character()
    init_multi_level()

    if race and class_name:
        race_num = races.index(race)
        class_num = classes.index(class_name)
        character['class'] = class_name
        character['race'] = races[race_num]
        if not race_class_allowed[race_num][class_num]:
            logging.info("You picked an illegal race/class combination ({}/{})".format(race, class_name))
            return (1)
    elif race:
        character['race'] = race
        race_num = races.index(character['race'])
        class_num = random.randint(0, len(classes) - 1)
        while not race_class_allowed[race_num][class_num]:
            class_num = random.randint(0, len(classes) - 1)
        character['class'] = classes[class_num]
        class_name = character['class']
    elif class_name:
        character['class'] = class_name
        class_num = classes.index(class_name)
        race_num = random.randint(0, len(races) - 1)
        while not race_class_allowed[race_num][class_num] and races[race_num] != "Drow":
            race_num = random.randint(0, len(races) - 1)
        character['race'] = races[race_num]
        race = character['race']
    else:
        race_num = random.randint(0, len(races) - 1)
        class_num = random.randint(0, len(classes) - 1)
        while not race_class_allowed[race_num][class_num]:
            class_num = random.randint(0, len(classes) - 1)
        character['race'] = races[race_num]
        character['class'] = classes[class_num]
        race = races[race_num]
        class_name = character['class']
    character['class_num'] = class_num

    logging.debug("Creating character of race {} class {} level {}".format(race, class_name, level))

    for name in multi_classes:
        if character['class'] == name:
            character['multi'] = True
            logging.debug("Found multi-class! {}".format(character['class']))
            for i in character['class']:
                if i == "C":
                    character['classes'].append("Cleric")
                    character['class_cnt'] = character['class_cnt'] + 1
                elif i == "F":
                    character['classes'].append("Fighter")
                    character['class_cnt'] = character['class_cnt'] + 1
                elif i == "R":
                    character['classes'].append("Ranger")
                    character['class_cnt'] = character['class_cnt'] + 1
                elif i == "M":
                    character['classes'].append("Magic-User")
                    character['class_cnt'] = character['class_cnt'] + 1
                elif i == "I":
                    character['classes'].append("Illusionist")
                    character['class_cnt'] = character['class_cnt'] + 1
                elif i == "T":
                    character['classes'].append("Thief")
                    character['class_cnt'] = character['class_cnt'] + 1
                elif i == "A":
                    character['classes'].append("Assassin")
                    character['class_cnt'] = character['class_cnt'] + 1
    if not character['multi']:
        character['classes'].append(character['class'])
        character['class_cnt'] = 1
    get_abilities(character)

    if level is None:
        logging.debug("Setting random level")

        if character['class_cnt'] == 1:
            level = random.randint(7, 12)
            character['class_lvl'].append(level)
            character['level'] = "{}".format(level)
        else:
            str = ""
            for x in xrange(character['class_cnt']):
                level = random.randint(5, 9)
                character['class_lvl'].append(level)
                str = str + "{}/".format(level)
            character['level'] = str[0:len(str) - 1]
        level = character['level']
        logging.debug("Set character level to {}".format(character['level']))
    else:
        level = "{}".format(level)
        if not "/" in level:
            logging.debug("Level is a string without a slash")
            str = ""
            for x in xrange(character['class_cnt']):
                character['class_lvl'].append(level)
                str = str + "{}/".format(level)
            character['level'] = str[0:len(str) - 1]
        else:
            logging.debug("Level is a string with a slash")
            character['level'] = level
            character['class_lvl'].append(level)

    fix_level(character)
    if ("F" in character['class'] or character['class'] == 'Ranger' or character['class'] == 'Paladin'):
        set_fighter_abilities(character)
    character['hp'] = get_hp(character)
    if character['race'] == 'Drow':
        character['dexterity'] = 18
    if character['dexterity'] == 18:
        character['numatt'] = character['numatt'] + 1.0

    # Add weapon specialization
    if (character['class'] == 'Fighter' or character['class'] == 'Ranger' or character['class'] == 'Paladin'):
        character['tohit'] = character['tohit'] + 3
        character['todam'] = character['todam'] + 3

    # Equip the character
    if character['class'] == 'Fighter' and character['race'] == 'Drow':
        equip_DrowFighter(tables, character)
    elif character['class'] == 'Cleric' and character['race'] == 'Drow':
        equip_DrowCleric(tables, character)
    elif character['class'] == 'FM' and character['race'] == 'Drow':
        equip_DrowFM(tables, character)
    elif "F" in character['class']:
        equip_Fighter(tables, character)
    elif character['class'] == "Cleric":
        equip_Cleric(tables, character)
    elif character['class'] == "Magic-User":
        equip_Mage(tables, character)
    elif character['class'] == "Thief":
        equip_Thief(tables, character)

    add_weapon_to_hit(character)
    character['ac'] = get_ac(character)

    Print_Character(character, cnt)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Character Generator",
                                     formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-l", "--level", help="Character level to generate")
    parser.add_argument("-n", "--number", help="Number of characters to generate", type=int, default=1)
    parser.add_argument("-v", "--verbose", help="Logging level", default="INFO")
    parser.add_argument("-r", "--race", help="Character race",
                        choices=["Dwarf", "Elf", "Gnome", "Half-Elf", "Halfling", "Half-Orc", "Human", "Drow"])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--class_name", help="Character class to generate",
                       choices=["Cleric", "Druid", "Fighter", "Paladin", "Ranger", "Magic-User", "Illusionist", "Thief",
                                "Assassin", "Monk", "CA", "CF", "CM", "CR", "CT", "CFM", "FA", "FI", "FM", "FT", "FMT",
                                "IT", "MT"])
    group.add_argument("-p", "--party", help="Generate an NPC Party of specified type",
                       choices=["DrowPatrol", "DrowParty", "Patrol", "NPCParty"])

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    loglevel = args.verbose
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logFile = "characters.log"
    logging.basicConfig(filename=logFile, format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=numeric_level)
    logging.getLogger().addHandler(logging.StreamHandler())

    tables = read_tables()

    if not args.party:
        for x in xrange(args.number):
            generate_character(tables, class_name=args.class_name, level=args.level, race=args.race)
    else:
        if args.party == "DrowPatrol":
            create_DrowPatrol()
        elif args.party == "DrowParty":
            create_DrowParty()
        elif args.party == "NPCParty":
            create_NPC_party(level=args.level, race=args.race)
        else:
            pass
