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

to_hit_table['Cleric'] =[[25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11],
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
    logging.debug(f" attacker {attacker['attack_type']}")
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

    # Multiple attack rounds per sequence
    if "/" in natt:
        attacker['attack_round'] = 1
        logging.debug(f'first_part {natt.split("/")[0]}')
        logging.debug(f'second part {natt.split("/")[1]}')
        attacker['total_attacks'] = int(natt.split("/")[0])
        attacker['attack_cycle_length'] = int(natt.split("/")[1])

       
        # this logic only works for attack sequences of length 1 or 2


        first_round_attacks = math.floor((attacker['total_attacks'] / attacker['attack_cycle_length']))
        second_round_attacks = attacker['total_attacks'] - first_round_attacks
        attacker['attack_sequence'] = []
        attacker['attack_sequence'].append(first_round_attacks)
        attacker['attack_sequence'].append(second_round_attacks)
        logging.debug(f"for NATT = {natt} attack sequence = {attacker['attack_sequence']}")
    # Multiple weapons to choose from
    elif "(" in natt:
        first_weapon = natt.split("(")[0]
        natt = first_weapon
        logging.debug(f"First weapon #att is {first_weapon}")
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
        logging.debug(f"for NATT = {natt} total_attacks = {attacker['total_attacks']}  attack sequence = {attacker['attack_sequence']}")

 
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
    id = 100
    for line in monster_names:

        (cnt,name,hd,ac,natt,dam,to_hit,to_dam,pop_flag) =  parse(line)
        logging.debug(f"Parsed string is: {cnt} {name} {hd} {ac} {natt} {dam} {to_hit} {to_dam} {pop_flag}")
        attacker = {}
        attacker['hp'] = 0
        attacker['who'] = id

        if pop_flag:
            idx = next((index for (index, d) in enumerate(monster_table) if d["Name"] == name), None)
            if idx:   # 1 or 2 parameters from file
                m = monster_table[idx]
                attacker['cnt'] = cnt
                attacker['name'] = name
                attacker['hd'] = int(m['HD'])
                attacker['ac'] = m['AC']
                set_attacks(attacker,m['NATT'])
                logging.debug(f'Original1 natt = {natt}')
                
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
            attacker['ac'] = ac
            set_attacks(attacker,natt)
            logging.debug(f'Original natt = {natt}')
            logging.debug(f"damage is {dam}")
            attacker['damage'] = dam
            logging.debug(f"attacker damage is {attacker['damage']}")

        attacker['hp'] = get_monster_hp(attacker,1,maxhp=False)[0]
        logging.debug(f"{attacker['name']} got {attacker['hp']} hit points")

        attacker['attack_type'] = "Monster"
        attacker['opponent'] = -1
        attacker['to_hit_mod'] = int(to_hit)
        attacker['to_dam_mod'] = int(to_dam)
        attacker['crit'] = False
        attacker['fumble'] = False
        attacker['spell_effects'] = []
        attacker['incapacitated'] = False
        if cnt == 1:
            roster.append(attacker) 
            id += 1
        else:
            for num in range(id,id+cnt):
                new_attacker = copy.deepcopy(attacker)
                new_attacker['name'] = name + f"_{num-100}"
                new_attacker['who'] = num
                new_attacker['hp'] = get_monster_hp(attacker, 1, maxhp=False)[0]
                new_attacker['max_hp'] = new_attacker['hp']
                roster.append(new_attacker)
                logging.debug(new_attacker)
            id += cnt
    logging.info(f"{roster}")
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

area_of_effect_spells = {}
area_of_effect_spells = {"armor","charm person","enlarge","friends", "jump",
"mount","protection from evil","run","sheild","sleep","bind","web","strength",
"entangle","faerie fire","shillelagh","speak with animals","hold person"}

#
# Cast a spell - set metadata to reflect spell casting
# 
def start_casting_spell(character):
    logging.info(f"    {character['name']} starting a spell")
    spell = {}
    spell['name'] = input("    What spell is being cast? ")
    spell['casting_time'] = get_int_input("    Casting time (segments)? ")
    spell['duration'] = get_int_input("    Spell duration (rounds)? ")
    spell['casting'] = True
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
            logging.debug(f"{d['name']} is casting: {casting}")
    return(casting)

#
#
#
def valid_id(target,multi_ret=False,monsters=None,characters=None):
    valid = False
    target_rec = None
    target_type = None
    logging.debug(f"Target id is {target}")
    int_target = int(target)
    if int_target >= 100:
        if monsters:
            m = get_target(int_target, monsters) 
            logging.debug(f"FOUND {m['who']} == {int_target}")
            valid = True
            target_rec = m
            target_type = 'monster'
    else:
        if characters:
            c = get_target(int_target, characters)
            logging.debug(f"FOUND {c['who']} == {target}")
            valid = True
            target_rec = c
            target_type = 'character'
    if multi_ret:
        return(valid, target_rec, target_type)
    else:
        return(valid)

#
# spell_results SPELL HANDLING 
#
# Upon spell completion, determine which category the spell falls under

#     - direct_fire_spells : Spells that do HP damage when completed
#				can have multiple targets
#     - area_of_effect_spells: Spells that impacted melee immediately

def spell_results(monsters, caster, spell):
    logging.info(f"{caster['name']}'s spell {spell['name']} is completed.")
    spell["casting"] = False
    spell['casting_time'] = -1

    if spell['name'] in direct_fire_spells:
        logging.info(f"**  Recognize direct fire spell {spell['name']}  **")
        spell['damage'] = get_int_input("    Damage caused (hp)?")
        done = False 
        while not done:
            tmp = input("    IDs of those affected, delimited by spaces, -99 to exit ")
            tmp_list = tmp.split()
            logging.debug(f"tmp_list {tmp_list}")
            for target in tmp_list:
                try:
                    if int(target) == -99:
                        logging.debug(f"    Recieved quit signal")
                        done = True
                except ValueError:
                    logging.info(f"    *** ERROR - INCORRECT INPUT: {target}, try again.")
                else:
                    logging.debug(f"target is {target}")
                    monster = get_target(target, monsters)
                    if monster == None:
                        logging.info(f"Invalid Target: {monster}")
                    else:
                        logging.debug(f"monster is {monster}")
                        apply_damage(monster, caster, spell['damage'])
                        done == True

    elif spell['name'] in area_of_effect_spells:
        c['spell_effects'].append(spell['name'])
        logging.info(f"Added effect {spell['name']} to {c['name']}")
	
#					
# Decrement Spell Times
#
def decrement_spell_times(monsters,characters):
    casting_characters =[c for c in characters if casting(c)]
    for c in casting_characters:
        for spell in c['spells_active']:
            print(f"    {c['name']}s casting {spell['name']}")
            if spell['casting_time'] > 0:
                print(f"    decrementing {c['name']} spell {spell['name']} casting_time: {spell['casting_time']}")
                spell['casting_time'] -= 1
            if spell['casting_time'] == 0:
                spell_results(monsters, c, spell)
                spell['casting'] = False
   

#
#
#
def finish_spells(characters):
    for c in characters:
        if casting(c):
            for spell in c['spells_active']:
                logging.debug(f"    c['name'] spell {spell['name']} goes off 2")
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
    str2 = f"[enter (use {target}), -1 (delay), -2 (forfeit), {specials}]: "
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
        logging.debug(f"attacker['damage'] = {attacker['damage']}")
        t = attacker['damage'].split("-")
        logging.debug(f"t parsed as {t}")
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
    return int(damage)

#
# Apply damage 
#
def apply_damage(target, caster, damage, is_PC=False):

    logging.debug(f" target = {target}  damage = {damage}")
    logging.debug(f" Character: {caster}")
    logging.debug(f"    is_pc value {is_PC}")

    if is_PC == True:
        target['total_damage'] += damage
    else:
        logging.debug(f"got hp = {target['hp']}")
        if target['hp'] >0:
            target['hp'] = target['hp'] -  damage
            if target['hp'] <= 0:
                logging.info("    ++++++++++++++++++++++++++++++++")
                logging.info(f"    {caster['name']} dropped {target['name']}")
                logging.info("    ++++++++++++++++++++++++++++++++")
                target['incapacitated'] = True

#
#
#
def apply_crit_table(attacker, defender):
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
            logging.info(f"****    CRITICAL HIT - 20/20 needed {to_hit_table[attacker['attack_type']][col][row]}   **** ")
            apply_crit_table(attacker,defender)
        else:
            logging.info(f"****    HIT - rolled {natural_die_roll}/20 needed {to_hit_table[attacker['attack_type']][col][row]}  ****")
    else:
        hit = False
        if natural_die_roll == 1:
            attacker['fumble'] = True
            attacker['attack_segments'] = []
        logging.info(f"    ***** MISS - rolled {die_roll}/{to_hit_table[attacker['attack_type']][col][row]} ({natural_die_roll}) *****")
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

    # commented out ror future  use     attacker['off_hand'] = ~attacker['off_hand']
        
 

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
            logging.debug(f"ATTACKER before is {attacker}") 
            opponent, healing = get_opponent(attacker,len(characters))
            logging.debug(f"ATTACKER afrer is {attacker}") 
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
                        logging.debug(f"which is {which}")
                        which_int = int(which[0])
                        characters[attacker['opponent']]['opponent'] = int(monsters[which_int]['who'])
            logging.debug(f"ATTACKER afrer is {attacker}") 
        
#
#
#
def player_actions(segment, monsters, characters):
    response = -99
    if not combat_over(monsters):
        actions_this_segment = [c for c in characters if segment in c['attack_segments']]
        for actor in actions_this_segment:
            logging.debug(f"Actor is {actor}")
            done = False
            while not done:
                logging.info(f"    ==================== ")
                response = get_input(f"    Who is {actor['name']} attacking? (s for spell, enter for {actor['opponent']})  ",specials=['s'])
                if response == 's':
                    logging.debug(f"Calling cast_spell")
                    start_casting_spell(actor)
                    done = True
                    actor['attack_segments'].remove(segment)
                    continue

                if response == '':
                    target = int(actor['opponent'])
                    if target == -1:
                        continue
                else:
                    target = int(response)
                    while target < 100 or target >= len(monsters)+100:
                        logging.warning(f"    Not a valid target; enter a number between 100 and {len(monsters)-1+100}")
                        response = get_input(f"    Who is {actor['name']} attacking? (s for spell, enter for {actor['opponent']})  ",specials=['s'])
                        target = int(response)
             
                col = get_column(actor)
                defender = get_target(target, monsters)
                row = int(defender['ac']) + 10
                logging.debug(f"Row {row} Column {col}")
                logging.debug(f"    {actor['name']} type is {actor['attack_type']}")
                logging.info(f"    {actor['name']} (level {actor['hd']}) needs a {to_hit_table[actor['attack_type']][col][row]} to hit AC {defender['ac']}")
                # check for hit
                response = get_int_input(f"    Did {actor['name']} hit? (0/1) ")
                done = True
                actor['attack_segments'].remove(segment)

                # if hit, set monster and character's opponent fields
                if response == 1:
                    if monsters[target-100]['opponent'] == -1:
                        monsters[target-100]['opponent'] = actor['who'] 
                    if actor['opponent'] == -1:
                        actor['opponent'] = target
                    damage = get_int_input("    How much damage did they do? ")
                    damage = int(damage)
                    logging.debug(f"{target}  {actor}  {damage}")
                    apply_damage(monsters[target-100],actor,damage)
                    response = ''
            logging.info(f"    ==================== ")


#
#
#
def get_target(id, roster):
    logging.debug(f"ROSTER IS {roster}")
    logging.debug(f"type(id) = {type(id)}")
    logging.debug(f"id is {id}")

    target_list = [ t for t in roster if t['who'] == int(id)]
    if target_list:
        if len(target_list) == 1:
            return target_list[0] 
        else:
            logging.debug(f"    Too many matches! {target_list}") 
    else: 
        try:
            if int(target_list[0]) != -99:
                logging.info(f"    Didn't find a unique record matching {id}") 
        except IndexError:
            return None
        


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
        logging.debug(f"Calling set up round")

        set_up_round(round,monsters,characters)
        for segment in range(10,-1,-1):
            if not combat_over(monsters):
                logging.debug('')
                print_tables(segment, characters, monsters)
                logging.debug(f"Calling monster action")
                monster_actions(segment, monsters, characters)
                if not combat_over(monsters):
                    logging.debug(f"Calling player action")
                    player_actions(segment, monsters, characters)
                    logging.debug(f"Calling decrement spell timers")
                    decrement_spell_times(monsters,characters)
            logging.debug(f"Calling dm_actions")
            dm_actions(segment, monsters, characters)
            logging.debug(f"Calling apply_spell_effects")
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
    for m in affected_monsters:
        for spell in m['spell_effects']:
            logging.info(f"Applying effects of {spell} to {m['name']}")
    logging.debug(f"made it past monsters")
    affected_characters = [c for c in characters if len(c['spell_effects'])>0]
    for c in affected_characters:
        for spell in c['spell_effects']:
            logging.info(f"Applying effects of {spell} to {c['name']}")
            c['spell_effects'].append(spell)

#
#
#
def get_input(str,specials=None):
    done = False
    while not done:
        response = input(str)
        logging.debug(f"    response is {response}")
        if specials and response in specials:
            return(response)
        elif response == '':
            return(response)
        elif is_number(response):
            return(response)
        else:
            logging.warning(f"    Invalid entry: must be {specials} or a number")

def get_input_id_list(str):
    return_list = None
    done = False
    while not done:
        tmp = input("    IDs of those affected, delimited by spaces, -99 to exit ")
        tmp_list = tmp.split()
        logging.debug(f"tmp_list {tmp_list}")
        if return_list!=None:
            new_list = return_list + tmp_list
            return_list = new_list
        else:
            return_list = tmp_list                
          
        if int(tmp_list[-1]) == -99:
            return(return_list)

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
        selection_list = get_input_id_list("    list of those affected (space delimited): ")
        logging.info(f"selection list is {selection_list}")

        for id in selection_list:
            if int(id) != -99:
                valid, record, record_type = valid_id(id,multi_ret=True,monsters=monsters,characters=characters)
                if valid:
                    record['spell_effects'].append(type)
                else:
                    logging.info(f"{id} is not a valid id")
                    selection_list.remove(id)
            else:
                selection_list.remove(id)
                logging.info(f"Added effect {type} to {selection_list}")             
                return(selection_list)

    
    # change to hit or to damage
    #
    elif action == "c":
        id = -20
        while not valid_id(d, monsters=monsters, characters=characters) and id != -99:
            id = get_int_input("who is to be modified (-99 to exit)? ")
            if id > 99:
                valid, this_one, this_type = valid_id(id,multi_ret=True,monsters=monsters)
            else:
                valid, this_one, this_type = valid_id(id,multi_ret=True,characters=characters)
            logging.debug(f"Found {this_one['name']} with values: {this_one['to_hit_mod']} / {this_one['to_dam_mod']}")
            to_hit = get_int_input("Enter new to hit bonus: ")
            to_dam = get_int_input("Enter new to damage bonus: ")
            logging.debug(f"Changing {this_one['name']} to hit and damage bonus from {this_one['to_hit_mod']}/{this_one['to_dam_mod']} to {to_hit} to {to_dam}")
            this_one['to_hit_mod'] = to_hit
            this_one['to_dam_mod'] = to_dam
 
    #
    # Damage a character or monster
    #
    elif action == 'd' or action == 'h':
        # Get a valid ID for either character or monster
        valid = False
        while not valid:
            select = get_int_input("id of entity to modify: ")
            valid, entity, entity_type = valid_id(select,multi_ret=True,monsters=monsters,characters=characters)
            if not valid: 
                logging.info(f"Not a valid ID: {select}.  Try again.")   

        # Get hit point adjustment
        amount = get_int_input("hit point adjustment: ")

        if entity_type == 'Monster': 
            # Damage Monster
            if action == 'd':
                entity['hp'] -= amount
                logging.info("Reduced {entity['name']} hit points by {amount}")
                if entity['hp'] <= 0:
                    entity['incapacitated'] = True
                    logging.info(f"    *** Entity {entity['who']} is incapacitated")
            # Heal Monter
            elif acion == 'h':
                entity['hp'] += amount
                logging.info("increased {entity['name']} hit points by {amount}")
                if entity['hp'] > entity['max_hp']:
                    entity['hp'] = entity['max_hp']
          
        else:
            if action == 'd':
                entity['damage'] += amount
                logging.info(f"Increased {entity['name']} damage by {amount}")
            elif action == 'h':
                entity['damage'] -= amount
                logging.info(f"reduced {entity['name']} damage by {amount}")
                if entity['damage'] < 0:
                    entity['damage'] = 0 

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
    attacker['attack_segments'] = []
    if attacker['incapacitated'] == False:

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
    else:
        logging.info(f"    {attacker['name']} is incapacitated and will not attack")


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
            c['incapacitated'] = False
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

#
#
#
def print_action(name, opponent_int, num_characters):
    if opponent_int >= 0 and opponent_int < num_characters:
        logging.info(f"    {name} opponent set to {opponent_int}")
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
    print("=======================================================================================")
    print(f"======================================  SEGMENT {segment : >2}   ===================================")
    print("=======================================================================================")
    print("  # : NAME            : DAM :STATUS:INIT :: # : OPPONENT NAME  : HP : INIT : Magical Effects")
    print("=======================================================================================")
    monsters_done = []
    char_strings = []
    for c in characters:
        printed = False
        id = c['who']

        # Set the character's string
        str1 = f"{id: 3} : {c['name'] : <16}: {c['total_damage'] : 3} :{c['incapacitated'] : 6}:{c['initiative'] : 4} :"
         
        #get opponent list; get opponents and spell counts
        opponents = [m for m in monsters if m['opponent']==id and m['incapacitated']==False] 
        monster_cnt = len(opponents)
        spell_cnt = len(c['spells_active'])
        logging.debug(f"spell_cnt = {spell_cnt}   monster_cnt = {monster_cnt}")

        if monster_cnt == 0 and spell_cnt == 0:
            char_strings.append(str1)
            printed = True
            str1 = "    :                 :     :      :     :"
            str2 = "    :                 :     :      :     :"

        while monster_cnt > 0 or spell_cnt > 0:
      
            if monster_cnt > 0:
                m = opponents[0]
                str2 =  f":{m['who'] :3}: {m['name'] : <15}: {m['hp'] : <3} : {m['initiative'] : 4} :" 
                monsters_done.append(m)
                del opponents[0] 
                monster_cnt -= 1
            else:
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
                str1 = "    :                 :     :      :    :"

        if not printed:   
            str = str1 + str2 + str3 
            char_strings.append(str)
            char_strings.append('--------------------------------------------------------------------------------')

        str1 = "    :                 :     :      :     :"

    monster_strings = []
    monster_strings.append('--------------------------------------------------------------------------------')
    for index, m in enumerate(monsters):
        if m not in monsters_done:
            if m['hp'] > 0:
                str2 =  f"{m['who'] : 3} : {m['name'] : <16}: {m['hp'] : <3} : {m['initiative'] : 4}" 
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
	
