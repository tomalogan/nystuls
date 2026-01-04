#!/usr/local/bin/python3

import copy
import argparse
import sys
import logging
import re
import random
import math
from monster_utils import read_monsters
from monster_utils import get_monster_hp

to_hit_table = {}
to_hit_level = {}
to_hit_table['Cleric'] =[[25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10],
 [23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8],
 [21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6],
 [20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4],
 [20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
 [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
 [19, 18, 17, 16, 15, 14, 13, 12, 11, 10,  9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, -1]]
to_hit_level['Cleric'] = [4, 7, 10, 13, 16, 19]

to_hit_table['Magic-User'] = [[26, 25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11],
 [24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9],
 [21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6],
 [20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3],
 [20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 ]]
to_hit_level['Magic-User'] = [6, 11, 16, 21]

to_hit_table['Fighter'] = [[26, 25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11],
 [25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10],
 [23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8],
 [21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6],
 [20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4],
 [20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
 [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
 [18, 17, 16, 15, 14, 13, 12, 11, 10,  9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, -1, -2],
 [16, 15, 14, 13, 12, 11, 10,  9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, -1, -2, -3, -4],
 [14, 13, 12, 11, 10,  9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, -1, -2, -3, -4, -5, -6]]
to_hit_level['Fighter'] = [1, 3, 5, 7, 9, 11, 13, 15, 17]

to_hit_table['Thief'] = [[26, 25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11],
 [24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9],
 [21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6],
 [20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4],
 [20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
 [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
to_hit_level['Thief'] = [5, 9, 13, 17, 21]

to_hit_table['Monster'] = [[26, 25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11],
 [25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10],
 [24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9],
 [23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8],
 [21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6],
 [20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5],
 [20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3],
 [20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
 [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
 [19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, -1],
 [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, -1, -2],
 [17, 16, 15, 14, 13, 12, 11, 10,  9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, -1, -2, -3]]
to_hit_level['Monster'] = [0.5,1,1.01,2,4,6,8,10,12,14,16]
  

#############################################################
#
# General routines
#
#############################################################

#
#
#
def roll_die(sides):
    tmp =  random.randint(1,sides)
    logging.debug(f"Rolled a D{sides} got {tmp}/{sides}")
    return tmp


#
#
#
def get_column(attacker):
    col = 0
    print(f" attacker {attacker['attack_type']}")
    for x in to_hit_level[attacker['attack_type']]:
        logging.debug(f"Checking level {x}")
        if int(attacker['hd']) >= x:
            col = col + 1
        else:
            break
    return col

#
#
#
def get_int_input(str):
    target = 'A'
    while not is_number(target):
        target = input(str)
    return(int(target))


#
#
#
def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


#############################################################
#
#  Set up routines
#
#############################################################
def read_monster_names(fi):
    monsters = []
    f = open(fi,'r')
    for line in f.readlines():
        line = line.strip()
        if not "Monster_Type" in line:
            monsters.append(line.strip())
    return(monsters)

#
# Parse multiple attacks per round - only call this routine
# once to set up initial attacks per round variables
#
def set_attacks(attacker,natt):

    if "/" in natt:
        attacker['attack_round'] = 1
        attacker['total_attacks'] = int(natt.split("/")[0])
        attacker['attack_cycle_length'] = int(natt.split("/")[1])

        first_round_attacks = math.floor((attacker['total_attacks'] / attacker['attack_cycle_length']))
        second_round_attacks = attacker['total_attacks'] - first_round_attacks
        attacker['attack_sequence'] = []
        attacker['attack_sequence'].append(first_round_attacks)
        attacker['attack_sequence'].append(second_round_attacks)
        logging.info(f"for NATT = {natt} attack sequence = {attacker['attack_sequence']}")
    elif "(" in natt:
        first_weapon = natt.split("(")[0]
        natt = first_weapon
        logging.info(f"First weapon #att is {first_weapon}")
        logging.info("Under construction... this will allow changing weapons")
        attacker['attack_round'] = 0
        attacker['attack_sequence'] = []
        attacker['attack_sequence'].append(1)
        attacker['total_attacks'] = int(natt)
        attacker['attack_cycle_length'] = 1
    else:
        attacker['attack_round'] = 0
        attacker['attack_sequence'] = []
        attacker['attack_sequence'].append(1)
        attacker['total_attacks'] = int(natt)
        attacker['attack_cycle_length'] = 1


    attacker['off_hand'] = False
    logging.debug(f"attacker['attack_cycle_length'] = {attacker['attack_cycle_length']}") 
#
#
#
def best_melee_class(class_list):
    for cl in class_list:
        if cl == "Fighter":
            return("Fighter")
    for cl in class_list:
        if cl == "Cleric":
            return("Cleric")
    for cl in class_list:
        if cl == "Thief":
            return("Thief")
    for cl in class_list:
        if cl == "Magic-User":
            return("Magic-User")


#
# There are only 4 attack tables; so we have to condense classes
#
def condense_classes(class_list):
    new_list = [item.replace("Monk","Cleric") for item in class_list]
    class_list = new_list
    new_list = [item.replace("Druid","Cleric") for item in class_list]
    class_list = new_list
    new_list = [item.replace("Illusionist","Magic-User") for item in class_list]
    class_list = new_list
    new_list = [item.replace("Ranger","Fighter") for item in class_list]
    class_list = new_list
    new_list = [item.replace("Paladin","Fighter") for item in class_list]
    class_list = new_list
    new_list = [item.replace("Assassin","Theif") for item in class_list]
    logging.debug(f"The final class_list is {new_list}")
    return(new_list)


#
#
#
def build_monster_roster(names_table):
    monster_names = read_monster_names(names_table)
    monster_table = read_monsters()
    roster = [] 
    for line in monster_names:
        (cnt,name,hd,ac,natt,dam,to_hit,to_dam,pop_flag) =  parse(line)
        logging.debug(f"Parsed string is: {cnt} {name} {hd} {ac} {natt} {dam} {to_hit} {to_dam} {pop_flag}")
        attacker = {} 
        if pop_flag:
            idx = next((index for (index, d) in enumerate(monster_table) if d["Name"] == name), None) 
            if idx:   # 1 or 2 parameters from file
                m = monster_table[idx]
                attacker['cnt'] = cnt
                attacker['name'] = name
                attacker['hd'] = int(m['HD'])
                attacker['ac'] = m['AC']
                set_attacks(attacker,m['NATT'])
                attacker['damage'] = m['DA']
                logging.debug(f"m[DA] is {m['DA']}")
                logging.debug(f"attacker['damage'] = {attacker['damage']}")
            else:
                logging.error(f"Can't find {name} in monster_table!!!")
                exit(1)
        else:
            attacker['cnt'] = cnt
            attacker['name'] = name
            attacker['hd'] = hd
            attacker['hp'] = get_monster_hp(attacker,1,maxhp=False)[0]
            logging.debug(f"got {attacker['hp']} hit points")
            attacker['ac'] = ac
            set_attacks(attacker,natt)
            logging.debug(f"damage is {dam}")
            attacker['damage'] = dam 
            logging.debug(f"attacker damage is {attacker['damage']}")

        attacker['attack_type'] = "Monster"
        attacker['opponent'] = -1 
        attacker['to_hit_mod'] = int(to_hit)
        attacker['to_dam_mod'] = int(to_dam)
        attacker['crit'] = False
        attacker['fumble'] = False
        attacker['spell_effects'] = [] 
        for num in range(1,cnt+1):
            new_attacker = copy.deepcopy(attacker)
            if cnt > 1:
                new_attacker['name'] = name + f"_{num}"
            else:
                new_attacker['name'] = name
            new_attacker['hp'] = get_monster_hp(attacker, 1, maxhp=False)[0]
            new_attacker['max_hp'] = new_attacker['hp'] 
            roster.append(new_attacker)
            logging.debug(new_attacker) 
    return roster


#############################################################
#
#  Spell casting routines
#
#############################################################
#
#
#

direct_fire_spells = {}
direct_fire_spells = {"cause light wounds", "spiritual hammer", "cause serious wounds",
"cause critical wounds", "flame strike", "slay living", "harm", "destruction",
"burning hands", "magic missile", "shocking grasp", "stinking cloud","fireball",
"lightning bolt", "ice storm", "wall of fire", "wall of ice", "cloud kill", 
"cone of cold", "death spell", "disintegrate", "incendiary cloud", "bigby's crushing hand"
"meteor storm", "power word, kill"}



def cast_spell(character):
    spell = {}
    spell['name'] = input("    What spell is being cast? ")
    # while not spell['name'].isalpha():
    #    spell['name'] = input("    What spell is being cast? ")


    spell['casting_time'] = get_int_input("    Casting time (segments)? ")
    spell['casting'] = True
    spell['duration'] = get_int_input("    Spell duration (rounds)? ")
    logging.debug(spell)
    character['spells_active'].append(spell)
    logging.debug(f"    active spells {character['spells_active']}")


#
#
#
def casting(d):
    casting = False
    for spell in d['spells_active']:
        logging.debug(f"checking spell {spell}")
        if spell['casting']:
            casting = True
        logging.debug(d['spells_active'])
        logging.debug(f"{d['name']} is casting: {casting}")
        return(casting)


#
#
#
def valid_id(target,monsters=None,characters=None):
    valid = False
    logging.info(f"Target id is {target}")
    if monsters:
        for m in monsters:
             if int(m['id']) == int(target):
                 logging.info(f"FOUND {m['id']} == {target}")
                 valid = True
    if characters:
        for c in characters:
            if int(m['id']) == int(target):
                 logging.info(f"FOUND {m['id']} == {target}")
                 valid = True
    return valid 

#
# spell_results
#
def spell_results(monsters, characters):
    for c in characters:
        if casting(c):
            for spell in c['spells_active']:
                logging.info(f"    c['name'] spell {spell['name']} goes off")
 
                if spell['name'] in direct_fire_spells:
                    logging.info(f"Recognize direct fire spell {spell['name']}")
                    spell['damage'] = get_int_input("    Damage caused (hp)?")
                    spell_hits = [] 
                    done = False 
                    while not done:
                        tmp = input("IDs of those affected, delimited by spaces, -99 to exit ")
                        tmp_list = tmp.split() 
                        logging.info(f"tmp_list {tmp_list}")                        
                        for target in tmp_list:
                            if int(target) == -99:
                                logging.info(f"recieved quit signal")
                                done = True
                            else:
                                monster_match = find_monster(monsters, target)
                                logging.info(f"monster_match is {monster_match}")
                                print(type(monster_match))
                                if len(monster_match)>0:
                                    logging.info(f"Found monster match {monster_match[0]['name']}") 
                                    apply_damage(target, spell['damage'], monsters, c['name'])
                                else:
                                    character_match = find_character(characters, target)
                                    logging.info(f"character_match is {character_match}")
                                    print(type(character_match))
                                    if len(character_match) > 0:
                                        logging.info(f"Found character match {character_match[0]['name']}") 
                                        apply_damage(target, spell['damage'], character, c['name']) 

def find_monster(monsters, target):
    affected_monster = [m for m in monsters if int(m['id']) == int(target)]

    print(type(affected_monster))
    print(affected_monster)
    for m in monsters:
        logging.info(f"Found ID {m['id']}") 
    if len(affected_monster) == 0:
        logging.info(f"Unable to find id {target} in monsters")
        affected_monster = []
    return affected_monster

def find_character(characters, target): 
    affected_character = [c for c in characters if int(c['id']) == int(target)]
    print(type(affected_character))
    if len(affected_character) == 0:
        logging.info(f"Unable to find id {target} in characters")
        affected_monster = []
    return affected_character


      

#
# Decrement Spell Times
#
def decrement_spell_times(monsters,characters):
    casting_characters =[c for c in characters if casting(c)]
    for c in casting_characters:
        for spell in c['spells_active']:
            print(f"    {c['name']} is casting {spell['name']}")
            if spell['casting_time'] > 0:
                print(f"    decrementing {c['name']} spell {spell['name']} casting_time: {spell['casting_time']}")
                spell['casting_time'] -= 1
            if spell['casting_time'] == 0:
                spell_results(monsters, characters)
        spell['casting'] = False




#
#  Double  check eveything from here on down
#
def finish_spells(characters):
    for c in characters:
        if casting(c):
            for spell in c['spells_active']:
                logging.info(f"    c['name'] spell {spell['name']} goes off")
                spell['casting_time'] = 0
                spell['casting'] = False

#############################################################
#
#  Attack Routines 
#
#############################################################

#
# Rolls initiative for monsters and sets attack segments,
# while dealing with fumbles and multiple attacks per round
#
# Gets character initiatives, sets attack_segment(s)
#
def set_up_round(round,monsters,characters):
    logging.info("============================================================")
    logging.info(f'---       START OF ROUND {round}                        ---')
    logging.info("============================================================")
    for attacker in monsters:
        if not attacker['fumble']:
            attacker['initiative'] = roll_die(10)
            logging.debug(f"    {attacker['name']} rolled a {attacker['initiative']} initiative")
            set_attack_segments(attacker)
        else:
            logging.info(f"    {attacker['name']} fumbled last round and loses their attack this round")
            attacker['fumble'] = False

    for character in characters:
        character['initiative'] = -1
        while character['initiative'] > 10 or character['initiative'] < 1:
            character['initiative'] = get_int_input(f"    Initiative for { character['name']} ")
            set_attack_segments(character)
             
    for spell in character['spells_active']:
        spell['duration'] -= 1
        if spell['duration'] < 0:
            logging.info(f"{character['name']} spell {spell['name']} has expired")
            character['spells_active'].remove(spell)

#
#
# Get opponent for this attacker
#
def get_opponent(attacker,num_characters):
    target = attacker['opponent']
    specials = ['p']
    str2 = f"[enter (use {target}), -1 (delay), -2 (forfiet), {specials}]: "
    str1 = f"    Who is {attacker['name']} attacking? "
    str = str1 + str2

    healed = False
    done = False
    opponent = ''
    while not done:
        opponent = get_input(str, specials = specials)
        if opponent == '':
            print_action(attacker['name'],target,num_characters)
            done = True
        elif opponent == 'p':
            logging.info(f"    {attacker['name']} drinks a healing potion")
            done = True
            healed = True
        if not done:
            opponent_int = int(opponent)
            if (opponent_int >= -2 and opponent_int < num_characters) or opponent_int == -99:
                attacker['opponent'] = opponent_int
                logging.debug(f"    opponent_int is {opponent_int}")
                print_action(attacker['name'], opponent_int, num_characters)
                done = True
        else:
            logging.info(f"Invalid opponent entered {opponent}; please enter -99 or -2 to {num_characters}")
            done = False

        return opponent, healed


#       
#       
#           
def calc_damage(attacker):           
    if attacker['off_hand']:
        print("    Attacking with off hand dagger")
        roll = roll_die(4)
        if attacker['crit']:
            attacker['crit']=False
            roll = roll * 2
        # Remove specialization +3
        dam_mod = attacker['to_dam_mod'] - 3
        if dam_mod > 0:
            damage = roll + dam_mod
        else:
            damage = roll
    else:
        logging.info(f"attacker['damage'] = {attacker['damage']}")
        t = attacker['damage'].split("-")
        logging.info(f"t parsed as {t}")
        upper = int(t[1].split()[0])
        lower = int(t[0])
        while lower > 0:
            if upper%lower == 0:
                roll = 0
                for x in range(0,lower):
                     roll += roll_die(int(upper/lower))
                if attacker['crit']:
                    attacker['crit']=False
                    roll = roll * 2
                damage = roll + (int(t[0]) - lower)
                logging.debug(f"    Rolling {lower}d{int(upper/lower)} + {int(t[0])-lower+attacker['to_dam_mod']}")
                break
            else:
                lower-=1
                upper-=1
        damage += attacker['to_dam_mod']
    return damage

#
#
#
def apply_damage(target,damage,monsters,char_name):
    tmp_list = [m for m in monsters if int(m['id']) == int(target)]

    logging.info(f" tmp_list is {tmp_list}")
    for m in tmp_list:
        logging.info(f"damaging {m['name']}")
        m['hp'] =  m['hp'] - damage
        if m['hp'] <= 0:
            logging.info("    ++++++++++++++++++++++++++++++++")
            logging.info(f"    {char_name} dropped {m['name']}")
            logging.info("    ++++++++++++++++++++++++++++++++")
            monsters.remove(m)
            if len(monsters)==0:
                logging.info("******************************************************")
                logging.info("           ALL MONSTERS HAVE BEEN DEFEATED ")
                logging.info("******************************************************")
                return(1)
            return(0)
        else:
            return(0)


#
#
#
def is_hit(attacker,defender):
    logging.debug(f"Attacker attack_type is {attacker['attack_type']}")
    col = get_column(attacker)
    row = int(defender['ac']) + 10
    logging.debug(f"Row {row} Column {col}")
    logging.debug(f"    {attacker['name']} attack_type is {attacker['attack_type']}")
    logging.debug(f"    {attacker['name']} (level {attacker['hd']}) needs a {to_hit_table[attacker['attack_type']][col][row]} to hit AC {defender['ac']}")
    natural_die_roll = roll_die(20)
    die_roll = natural_die_roll + attacker['to_hit_mod']
    if die_roll > 20:
        die_roll -= 5
        if die_roll < 20:
            die_roll = 20
    if die_roll >= to_hit_table[attacker['attack_type']][col][row]:
        hit = True
        if natural_die_roll == 20:
            attacker['crit'] = True
            logging.info("    CCCCCCCCCC  RRRRRRRRRR  IIIIIIIIII  TTTTTTTTTT")
            logging.info("    CCCCCCCCCC  RRRRRRRRRR      II      TTTTTTTTTT")
            logging.info("    CC          RR      RR      II          TT    ")
            logging.info("    CC          RR      RR      II          TT    ")
            logging.info("    CC          RRRRRRRRRR      II          TT    ")
            logging.info("    CC          RR  RR          II          TT    ")
            logging.info("    CC          RR   RR         II          TT    ")
            logging.info("    CCCCCCCCCC  RR     RR   IIIIIIIIII      TT    ")
            logging.info("    CCCCCCCCCC  RR      RR  IIIIIIIIII      TT    ")
            logging.info(f"    CRITICAL HIT - {die_roll}/{to_hit_table[attacker['attack_type']][col][row]} ({natural_die_roll})")
        else:
            logging.info(f"    HIT - rolled {die_roll}/{to_hit_table[attacker['attack_type']][col][row]} ({natural_die_roll})")
    else:
        hit = False
        if natural_die_roll == 1:
            attacker['fumble'] = True
            attacker['attack_segments'] = []
        logging.info(f"    MISS - rolled {die_roll}/{to_hit_table[attacker['attack_type']][col][row]} ({natural_die_roll})")
    return(hit)

#
#
#
def attack(attacker,defender):
    logging.info(f"    {attacker['name']} is attacking {defender['name']}")
    if is_hit(attacker,defender):
        if casting(defender):
            print(f"    {defender['name']} has been hit by {attacker['name']}")
            defender['casting'] = False
            spell = defender['spells_active'][-1]
            print(f"    {defender['name']}'s spell {spell['name']} was foiled by attack")
            defender['spells_active'].remove(spell)
        damage = calc_damage(attacker)
        defender['total_damage'] += damage
        logging.info (f"    {defender['name']} is hit by {attacker['name']} for {damage} points.")
    else:
        if attacker['fumble']:
            roll = roll_die(6)
            logging.info("    FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE ---")
            if roll < 3:
                logging.info(f"    FUMBLE -- attacker {attacker['name']} fumbled - make a dexterity check")
            elif roll <5:
                logging.info(f"    FUMBLE -- attacker {attacker['name']} fumbled - make a 1/2 dexteriry check")
            else:
                logging.info(f"    FUMBLE -- attacker {attacker['name']} fumbled - make a weapon saving throw")
            logging.info("    FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE ---")

    # commented out for future  use     attacker['off_hand'] = ~attacker['off_hand']
        
 

#
#
#            
def combat_over(monsters):
    if len(monsters) == 0:
        return True
    else:
        return False


#
#  Monster Actions
#
def monster_actions(segment, monsters, characters):
    for attacker in monsters:
        while segment in attacker['attack_segments'] and not combat_over(monsters):
            opponent, healing = get_opponent(attacker,len(characters))
            if healing:
                healing = get_int_input(f"    How any points was {attacker['name']} healed? ")
                attacker['hp'] += healing
                if attacker['hp'] > attacker['max_hp']:
                    attacker['hp'] = attacker['max_hp']
                attacker['attack_segments'] = []
            elif attacker['opponent'] == -1:
                attacker['attack_segments'].append(segment-1)
                attacker['attack_segments'].remove(segment)
            elif attacker['opponent'] == -2:
                attacker['attack_segments'].remove(segment)
            elif attacker['opponent'] == -99:
                monsters = []
                print("Set monsters to zero")
            else:
                if not combat_over(monsters):
                    attacker['attack_segments'].remove(segment)
                    attack(attacker,characters[attacker['opponent']])
                    if characters[attacker['opponent']]['opponent'] == -1:
                        which =  [i for i, e in enumerate(monsters) if e == attacker]
                        characters[attacker['opponent']]['opponent'] = int(which[0])

#
#
#
def player_actions(segment, monsters, characters):
    response = -99
    if not combat_over(monsters):
        actions_this_segment = [c for c in characters if segment in c['attack_segments']]
        for actor in actions_this_segment:
                response = get_input(f"    Who is {actor['name']} attacking? (s for spell, enter for {actor['opponent']})  ",specials=['s'])
                if response == 's':
                    cast_spell(actor)
                    break
                    actor['attack_segments'].remove(segment)
                elif response == '':
                    target = int(actor['opponent'])
                else:
                    target = int(response) - 100
                if target < 0 or target >= len(monsters):
                    logging.warning(f"    Not a valid target; enter a number between 100 and {len(monsters)-1+100}")
                else:
                    col = get_column(actor)
                    defender = monsters[target]
                    row = int(defender['ac']) + 10
                    logging.debug(f"Row {row} Column {col}")
                    logging.debug(f"    {actor['name']} type is {actor['attack_type']}")
                    logging.info(f"    {actor['name']} (level {actor['hd']}) needs a {to_hit_table[actor['attack_type']][col][row]} to hit AC {defender['ac']}")
   
                    # check for hit
                    response = get_input(f"    Did {actor['name']} hit? (0/1) ")

                    # if hit, set monster and character's opponent fields
                    if response:
                        if monsters[target]['opponent'] == -1:
                            monsters[target]['opponent'] = actor['id'] 
                        if actor['opponent'] == -1:
                            actor['opponent'] = target
                        damage = get_int_input("    How much damage did they do? ")
                        damage = int(damage)
                        tmp =  apply_damage(target,damage,monsters,actor['name'])
                    actor['attack_segments'].remove(segment)
                    response = ''



#
#  Main Combat Loop
#
def run_combat():
    display_intro()

    # roll up monsters
    characters = read_char_table(args.char_table)

    monsters = build_monster_roster(args.monster_table)
    monster_backup = copy.deepcopy(monsters)

    # main combat loop
    round = 1
    while not combat_over(monsters):
        set_up_round(round,monsters,characters)
        for segment in range(10,-1,-1):
            if not combat_over(monsters):
                logging.info('')
                print_tables(segment, characters, monsters)
                monster_actions(segment, monsters, characters)
                if not combat_over(monsters):
                    player_actions(segment, monsters, characters)
                    decrement_spell_times(monsters,characters)
            dm_actions(segment, monsters, characters)
            apply_spell_effects(monsters, characters)
        finish_spells(characters)
        logging.info('')
        logging.info(f'END OF ROUND {round}')
        logging.info('')
        logging.info('================================================================')
        logging.info('')
        round += 1

    mon_list = []
    for m in monster_backup:
        if m['name'] not in mon_list:
            tmp = m['name'].replace('_',' ')
            tmp = tmp.split()[0]
            mon_list.append(tmp)
    mon_list = set(mon_list)
    print(mon_list)

    for types in mon_list:
        print(f"types = {types}")

def apply_spell_effects(monsters,characters):
    affected_monsters = [m for m in monsters if len(m['spell_effects'])>0]
    affected_characters = [c for c in characters if len(c['spell_effects'])>0]
    for m in affected_monsters:
        for spell in m['spell_effects']:
            logging(f"Applying effects of {spell} to {m['name']}")
            pass 

def get_input(str,specials=None):
    done = False
    while not done:
        response = input(str)
        if specials and response in specials:
            return(response)
        elif response == '':
            return(response)
        elif is_number(response):
            return(int(response))
        else:
            logging.warning(f"    Invalid entry: must be {specials} or a number")

#
#
#
options = "(a)pply magical effect, (c)hange to hit and damage bonus, (d)amage,\
(h)eal, (r)einforce, (s)witch weapon, -99 to exit"
#
#
def dm_actions(segment, monsters, characters):
    logging.info(f"Options: {options}")
    action = get_input("make your selection: ", specials=['h','d','r','a','c','s'])

    #
    # Add a spell effect
    #
    if action == 'a':
        type = input("Spell that was cast: ")
        selection_str = get_input("list of those affected (space delimited): ")
        selection_list = selection_str.split(" ")
        for persona in selection_list:
            if valid_id(persona,monsters=monsters,characters=characters):
                persona['spell_effects'].add(type)
            else:
                logging.info(f"{persona} is not a valid id")
                selection_list.remove(persona)
        logging.info(f"Added effect {type} to {selection_list}")             

    #
    # change to hit or to damage
    #
    elif action == "c":
        id = -20
        while not valid_id(id, monsters=monsters, characters=characters) and id != -99:
            id = get_int_input("who is to be modified (-99 to exit)? ")
            if id > 99:
                this_one = [m for m in  monsters if m['id']==id]
            else:
                this_one = [c for c in characters if c['id']==id]
       
            logging.info(f"Found {this_one['name']} with values: {this_one['to_hit_mod']} / {this_one['to_dam_mod']}")
            to_hit = get_int_input("Enter new to hit bonus: ")
            to_dam = get_int_input("Enter new to damage bonus: ")
            logging.info(f"Changing {this_one['name']} to hit and damage bonus from {this_one['to_hit_mod']}/{this_one['to_dam_mod']} to {to_hit} to {to_dam}")
            this_one['to_hit_mod'] = to_hit
            this_one['to_dam_mod'] = to_dam
 
    #
    # Damage a character or monster
    #
    elif action == 'd':
        select = get_int_input("id of entity to damage: ")
        amount = get_int_input("hit points to damage: ")
        if valid_id(select):
            select['hp'] -= amount
            logging.info("Reduced {select['name']} hit points by {amount}")
            if select['hp'] <= 0:
                logging.info(f"{select['name']} is down")   
        else:
            logging.info(f"{select} is not a valid ID.  Try again")
    elif action == 'h':
        select = get_int_input("id of entity to heal: ")
        amount = get_int_input("hit points to heal: ")
        if valid_id(select):
            select['hp'] += amount
            logging.info("increased {select['name']} hit points by {amount}")
        else:
            logging.info(f"{select} is not a valid ID.  Try again")
    elif action == "r":
            # Send in the reinforcements
            pass
    elif action == "s":
            # Switch weapons
            pass




                
 
#
# Set up attack segments
#
def set_attack_segments(attacker):

    swap_attacks(attacker)
 
    logging.debug(f"attacker['attack_sequence'] is {attacker['attack_sequence']}")
    logging.debug(f"attacker['attack_round'] is {attacker['attack_round']}")
    attacks_this_round = attacker['attack_sequence'][attacker['attack_round']]

    attacker['attacks_this_round'] = attacks_this_round
    attacker['attack_segments'] = []

    # First attack on initiative
    attacker['attack_segments'].append(attacker['initiative'])

    # Second attack on zero
    if attacks_this_round > 1:
        attacker['attack_segments'].append(0)

    # Evenly distribute remaining attacks
    if attacks_this_round > 2:
        offset = int(attacker['initiative']) / int(attacker['attacks'])
        logging.debug(f"    Offset is {offset}")
        for x in range(3,attacker['attacks']):
            attacker['attack_segments'].append(attacker['initiative'] - (x-2)*offset)

    logging.info(f"    {attacker['name']} will attack on segments {attacker['attack_segments']}")

#
#
#
def swap_attacks(attacker):
    logging.debug(f"attacker['attack_cycle_length'] = {attacker['attack_cycle_length']}")
    logging.debug(f"attacker['attack_round'] = {attacker['attack_round']}")
    if int(attacker['attack_cycle_length']) > 1:
        attacker['attack_round'] += 1
        if attacker['attack_round'] == attacker['attack_cycle_length']:
            attacker['attack_round'] = 0
    logging.debug(f"attacker['attack_round'] = {attacker['attack_round']}")
                
# read in the character file...
#
# format is
#    name AC Class Level NATT
#
# multi-class, I cheateed
#   when entering multi-class character, alway put the classes in this order 
#    
#    Fighter/CLeric/Thief/Magic-User 
# 
#   because I'm going to use the first class and the first level as the #   fighting ability
#
#
def read_char_table(fi):
    characters = []
    f = open(fi,'r') 
    cnt = 0
    for line in f.readlines():
        line = line.strip()
        if not "Character_Name" in line:
            columns = line.split()
            c = {}
            c['name'] = columns[0]
            c['ac'] = int(columns[1])
                
            c['class'] = columns[2]
            c['class_list'] = c['class'].split("/")
            c['class_list'] = condense_classes(c['class'].split("/"))
                    
            #
            # Find the best attack type and corresponding level
            #
            if "/" in c['class']:
                c['multi-class'] = True
                c['attack_type'] = best_melee_class(c['class_list'])
            else:
                c['attack_type'] = c['class_list']

            if isinstance(c['attack_type'], list):
                logging.debug(f"Found list {c['attack_type']} : taking first element {c['attack_type'][0]}")
                c['attack_type'] = c['attack_type'][0]

            logging.debug(f"Best attack class is {c['attack_type']}")
            c['hd'] = columns[3]
            if "/" in c['hd']:
                c['level_list'] = c['hd'].split("/")
                c['hd'] = int(c['level_list'][0]) 



            #
            # sort out the attacks
            # 
            c['natt'] = columns[4]
            set_attacks(c,c['natt'])



            c['spells_active'] = []
            c['casting'] = False
            c['total_damage'] = 0
            c['opponent'] = -1
            c['who'] = cnt
            c['spell_effects'] = []
            cnt = cnt + 1
            logging.debug(c)
            characters.append(c)
    return(characters)

#
# [cnt] name [level ac natt dam [to_hit to_dam]] 
#
def parse(line):
    cnt = 1
    name = ''
    level = 0
    ac = 11 
    natt = 0
    dam = ''
    to_hit = 0
    to_dam = 0 
    tokens = line.split()
    logging.debug(f"tokens = {tokens}")
    pop_flag = False 
    if len(tokens) == 1:    # name
        name = tokens[0] 
        pop_flag = True
    elif len(tokens) == 2:    # cnt name
        cnt = int(tokens[0])
        name = tokens[1]
        pop_flag = True
    elif len(tokens) == 5:    # name HD AC #ATT DAM
        name = tokens[0]
        level = tokens[1]
        ac = tokens[2]
        natt = tokens[3]    
        dam = tokens[4]
    elif len(tokens) == 6:      # cnt name HD AC #ATT DAM
        cnt = tokens[0]
        name = tokens[1]
        level = tokens[2]
        ac = tokens[3]
        natt = tokens[4]    
        dam = tokens[5]
    elif len(tokens) == 7:      # name HD AC #ATT DAM to_hit to_dam
        name = tokens[0]
        level = tokens[1]
        ac = tokens[2]
        natt = tokens[3]    
        dam = tokens[4]
        to_hit = tokens[5]
        to_dam = tokens[6]
    elif len(tokens) == 8:      # cnt name HD AC #ATT DAM to_hit to_dam
        cnt = tokens[0]
        name = tokens[1]
        level = tokens[2]
        ac = tokens[3]
        natt = tokens[4]    
        dam = tokens[5]
        to_hit = tokens[6]
        to_dam = tokens[7]

    logging.debug(f"cnt = {cnt},name = {name}, level = {level} ,ac = {ac}, ")
    logging.debug(f"natt = {natt}, dam = {dam}, to_hit = {to_hit}, to_dam = {to_dam}, ")
    logging.debug(f"pop_flag = {pop_flag}")

    return(cnt,name,level,ac,natt,dam,to_hit,to_dam,pop_flag)


    return(roster)

#
#
#
def print_action(name, opponent_int, num_characters):
    if opponent_int >= 0 and opponent_int < num_characters:
        logging.debug(f"    {name} opponent set to {opponent_int}")
    elif opponent_int == -1:
        logging.info(f"    {name} holding action until next segment")
    elif opponent_int == -2:
        logging.info(f"    {name} not attacking this round")
    elif opponent_int == -99:
        logging.info( "    Combat is over!!!!")

#
#
#
def display_intro():
    logging.info("================================================================================")
    logging.info("RUN COMBAT")
    logging.info("================================================================================")
    logging.info("Getting monster tables")


#
#
#    print("================================================================================")
#    print("  # : NAME            : DAM : INIT :: # : OPPONENT NAME  : HP : INIT ")
#    print("================================================================================")
#           0        1         2         3         4         5         6         7         8
#           12345678901234567890123456789012345678901234567890123456789012345678901234567890.
#   str1 = "    :                 :     :      :"
#   str2 =                                     ":   :                :    :      :0"




def print_tables(segment, characters, monsters):
    print('')
    print("================================================================================")
    logging.info(f"==================================  SEGMENT {segment : >2}   ===============================")
    print("================================================================================")
    print("  # : NAME            : DAM : INIT :: # : OPPONENT NAME  : HP : INIT ")
    print("================================================================================")
    id = 0
    monsters_done = []
    char_strings = []
    for c in characters:
        printed = False

        # Set the character's string
        str1 = f"{id : 3} : {c['name'] : <16}: {c['total_damage'] : 3} : {c['initiative'] : 4} :"
        c['id'] = id
         
        #get opponent list; get opponents and spell counts
        opponents = [m for m in monsters if m['opponent']==id]
        monster_cnt = len(opponents)
        spell_cnt = len(c['spells_active'])
        logging.debug(f"spell_cnt = {spell_cnt}   monster_cnt = {monster_cnt}")

        if monster_cnt == 0 and spell_cnt == 0:
            char_strings.append(str1)
            printed = True
            str1 = "    :                 :     :      :"

        while monster_cnt > 0 or spell_cnt > 0:
      
            if monster_cnt > 0:
                m = opponents[0]
                str2 =  f":{id+100 :3} : {m['name'] : <14}: {m['hp'] : <3} : {m['initiative'] : 4}" 
                monsters_done.append(m)
                del opponents[0] 
                monster_cnt -= 1
            else:
#                 str2 = '' 
                 str2 = ":   :                :    :      :"
            if spell_cnt > 0:
                spell = c['spells_active'][0]
                if spell['casting']:
                    str3 = f" casting {spell['name']} {spell['casting_time']} "
                else:
                    str3 = f" {spell['name']} has {spell['duration']} rounds "
                del c['spells_active'][0]
                spell_cnt -= 1
            else:
                str = str1 + str2 
                char_strings.append(str)
                printed = True
                str1 = "    :                 :     :      :"

        if not printed:   
            str = str1 + str2 + str3 
            char_strings.append(str)
            char_strings.append('--------------------------------------------------------------------------------')

        str1 = "    :                 :     :      :"
        id += 1

    monster_strings = []
    monster_strings.append('--------------------------------------------------------------------------------')
    for index, m in enumerate(monsters):
        if m not in monsters_done:
            str2 =  f"{index+100 : 3} : {m['name'] : <16}: {m['hp'] : <3} : {m['initiative'] : 4}" 
            m['id'] = index+100
            str = str1 + str2 
            monster_strings.append(str)
            monster_strings.append('--------------------------------------------------------------------------------')

    for s in char_strings:
        print(s)
    for m in monster_strings:
        print(m)


# Not currently used
def print_monster_roster(monsters):
    cnt = 0
    logging.info('')
    logging.info(f'{"    Monster Roster" : <28} : HP : Opponent')
    logging.info('    ========================================')
    for m in monsters:
        logging.info(f"    {cnt} : {m['name'] : <20} : {m['hp'] : <3}  : {m['opponent']}")
        cnt = cnt + 1
    logging.info('    ========================================')


def print_character_roster(characters,monsters):
    cnt = 0
    logging.info('')
    logging.info(f'    {"Character Roster" : <20}:DAM: Opponent(s) : Active spells')
    logging.info('    ====================================')
    for c in characters:
        str = ''
        str1 = str + f"    {cnt} : {c['name'] : <16}:{c['total_damage'] : 3}"
        str2 = ': '
        for m in monsters:
            if m['opponent'] ==  cnt:
                str2 = str2 + f" {m['name']} :"
        str3 = ' '
        for spell in c['spells_active']:
            if spell['casting']:
                str3 = str3 + f" casting {spell['name']} {spell['casting_time']}; "
            else:
                str3 = str3 + f" {spell['name']} has {spell['duration']} rds; "
                str = str1 + str2 +str3
                logging.info(str)
    cnt += 1
    logging.info('    ====================================')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dungeon Master's Assitant")
    parser.add_argument("char_table",help="Character roster file")
    parser.add_argument("monster_table",help="Monster roster file")
    parser.add_argument("-v", "--verbose", help="Logging level", default="INFO")


#    group.add_argument("-c", "--class_name", help="Character class to generate",
#                       choices=["Cleric", "Druid", "Fighter", "Paladin", "Ranger", "Magic-User", "Illusionist", "Thief",
#                                "Assassin", "Monk", "CA", "CF", "CM", "CR", "CT", "CFM", "FA", "FI", "FM", "FT", "FMT",
#                                "IT", "MT"])
#    group.add_argument("-p", "--party", help="Generate an NPC Party of specified attack_type",
#                       choices=["DrowPatrol", "DrowParty", "Patrol", "NPCParty"])

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    loglevel = args.verbose
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logFile = "dm_assistant.log"
    logging.basicConfig(filename=logFile, format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p', level=numeric_level)
    logging.getLogger().addHandler(logging.StreamHandler())
    run_combat()

