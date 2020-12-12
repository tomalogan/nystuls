#!/usr/local/bin/python3

import copy
import argparse
import sys
import logging
import random
import re
import random
from random_monster import read_monsters
from get_monster_hp import get_monster_hp

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
  

def roll_die(sides):
    return random.randint(1,sides)

def get_column(attacker):
    col = 0
    for x in to_hit_level[attacker['type']]:
        logging.debug(f"Checking level {x}")
        if attacker['level'] > x:
            col = col + 1
        else:
            break
    return col

def is_hit(attacker,defender):
    roll = roll_die(20)
    logging.debug(f"Attacker type is {attacker['type']}")
    col = get_column(attacker)
    row = int(defender['ac']) + 10
    logging.debug(f"Row {row} Column {col}")
    logging.debug(f"    {attacker['name']} type is {attacker['type']}")
    logging.debug(f"    {attacker['name']} (level {attacker['level']}) needs a {to_hit_table[attacker['type']][col][row]} to hit AC {defender['ac']}")
    natural_die_roll = roll_die(20) 
    die_roll = natural_die_roll + attacker['to_hit_mod'] 
    if die_roll > 20:
        die_roll -= 5
        if die_roll < 20:
            die_roll = 20
    if die_roll >= to_hit_table[attacker['type']][col][row]:
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
            logging.info(f"    CRITICAL HIT - {die_roll}/{to_hit_table[attacker['type']][col][row]} ({natural_die_roll})")
        else:
            logging.info(f"    HIT - rolled {die_roll}/{to_hit_table[attacker['type']][col][row]} ({natural_die_roll})")
    else:
        hit = False 
        if natural_die_roll == 1:
            attacker['fumble'] = True
            attacker['attack_segments'] = []
        logging.info(f"    MISS - rolled {die_roll}/{to_hit_table[attacker['type']][col][row]} ({natural_die_roll})")
    return(hit)
  
def casting(d):
    casting = False
    for spell in d['spells_active']:
        logging.debug(f"checking spell {spell}")
        if spell['casting']:
            casting = True
    logging.debug(d['spells_active'])
    logging.debug(f"{d['name']} is casting: {casting}")
    return(casting)

 
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
            logging.info("    FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- ")
            if roll <3:
                logging.info(f"    FUMBLE - attacker {attacker['name']} fumbled - make a dexteriry check")
            elif roll <5:
                logging.info(f"    FUMBLE - attacker {attacker['name']} fumbled - make a 1/2 dexteriry check")
            else:
                logging.info(f"    FUMBLE - attacker {attacker['name']} fumbled - make a weapon saving throw")
            logging.info("    FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- ")

def calc_damage(attacker):
    t = attacker['damage'].split("-")
    upper = int(t[1].split()[0])
    lower = int(t[0])
    while lower > 0:
        if upper%lower == 0:
            roll = roll_die(int(upper/lower))*lower
            if attacker['crit']:
                attacker['crit']=False
                roll = roll * 2
            damage = roll + (int(t[0]) - lower)
            logging.info(f"    Rolling {lower}d{int(upper/lower)} + {int(t[0])-lower+attacker['to_dam_mod']}")
            break
        else:
            lower-=1
            upper-=1
    damage += attacker['to_dam_mod']
    return damage 

def get_opponent(attacker,num_characters):
    target = attacker['opponent']    
    special = "h"
    str1 = f"    Who is {attacker['name']} attacking? "
    str2 = f"character number, enter (no change - use {target}), -1 (no one) {special} heal: "
    str = str1 + str2

    combat_over = False
    healed = False
    done = False
    opponent = ''
    while not done:
        opponent = get_input(str, special = 'h') 
        if opponent == '':
            logging.info(f"    {attacker['name']} re-using opponent {target}")
            opponent = "99"
            done = True
        elif opponent == 'h':
            healing = get_int_input(f"    How any points was {attacker['name']} healed? ")
            attacker['hp'] += healing
            if attacker['hp'] > attacker['max_hp']:
                attacker['hp'] = attacker['max_hp']
            attacker['attack_segments'] = []
            done = True
            healed = True
        if not done: 
            opponent_int = int(opponent)
            logging.debug(f"    opponent_int is {opponent_int}")
            done = True
            if opponent_int == -1:
                logging.info("    Setting opponent to None (-1)")
                attacker['opponent'] = -1
            elif opponent_int >= 0 and opponent_int <= num_characters:
                logging.info(f"    Setting opponent to {opponent_int}")
                attacker['opponent'] = opponent_int
            elif opponent_int == -99:
                logging.info( "    Combat is over!!!!")
                combat_over = True
            else:
                logging.info(f"Invalid opponent entered {opponent}; please enter a value of -1 to {num_characters}")
                opponent = ''
                done = False
    return combat_over, healed


def decrement_spell_times(characters):
    for c in characters:
        if casting(c):
            for spell in c['spells_active']:
                print(f"    {c['name']} is casting")
                if spell['casting_time'] > 0:
                    spell['casting_time'] -= 1
                if spell['casting_time'] == 0:
                    logging.info(f"    {c['name']} spell {spell['name']} goes off")
                    spell['casting'] = False
                else:
                    print(f"    decrementing {c['name']} spell {spell['name']} casting_time: {spell['casting_time']}")

def finish_spells(characters):
    for c in characters:
        if casting(c):
            print(f"    {c['name']} is casting")
            for spell in c['spells_active']:
                if spell['casting_time'] > 0:
                    spell['casting_time'] = 0
                if spell['casting_time'] == 0:
                    logging.info(f"    c['name'] spell {spell['name']} goes off")
                    spell['casting'] = False


def run_combat():
    logging.info("==================================================")
    logging.info("RUN COMBAT")
    logging.info("==================================================")

    # roll up monsters
    logging.info("Getting monster tables")
    characters = read_char_table(args.char_table)
    monster_names = read_monster_names(args.monster_table)
    monster_table = read_monsters()
    monsters = build_monster_roster(monster_names,monster_table)

    combat_over = False
    round = 1
    while not combat_over:
        # Run this round
        logging.info(f'START OF ROUND {round}')
        set_up_round(monsters,characters)
        for init in range(10,-1,-1):
            if not combat_over:
                logging.info('')
                logging.info(f"SEGMENT {init} ----------------------------------------")
                for attacker in monsters:
                    while init in attacker['attack_segments'] and not combat_over:
                        print_character_roster(characters,monsters)
                        combat_over, healed = get_opponent(attacker,len(characters))
                        if not combat_over and not healed:
                            attack(attacker,characters[attacker['opponent']])
                            if not attacker['fumble']:
                                attacker['attack_segments'].remove(init) 
                if not combat_over:
                    player_actions(monsters,characters)
                    decrement_spell_times(characters)
        finish_spells(characters)
        logging.info('')
        logging.info(f'END OF ROUND {round}')
        logging.info('')
        logging.info('================================================================')
        logging.info('')
        round += 1

def get_int_input(str):
    target = 'A'
    while not is_number(target):
        target = input(str) 
    return(int(target))

def get_input(str,special=''):
    done = False
    while not done:
        response = input(str)
        if response == special:
            return(response)
        elif response == '':
            return(response)
        elif is_number(response):
            return(int(response))
        else:
            logging.warning(f"    Invalid entry: must be {special} or a number")
                                              
def cast_spell(who,character,):
    spell = {}
    
    spell['name'] = input("    What spell is being cast? ")
    while not spell['name'].isalpha():
        spell['name'] = input("    What spell is being cast? ")
    spell['casting_time'] = get_int_input("    Casting time (segments)? ")
    spell['casting'] = True
    spell['duration'] = get_int_input("    Spell duration (rounds)? ") 
    logging.debug(spell)
    character['spells_active'].append(spell) 
    logging.debug(f"    active spells {character['spells_active']}") 

def player_actions(monsters,characters):
    response = '1'
    while not response == '':
        print_character_roster(characters,monsters)
        who = -99
        while who >= len(characters) or who < 0:
            who = get_input("    Who's action is it (return to exit): ")
            if not is_number(who):
                return()
        print_monster_roster(monsters)
        response = get_input(f"    Who is {characters[who]['name']} attacking? (s for spell) ",special='s')
        if response == 's':
            cast_spell(who,characters[who])
        elif response == '':
            pass 
        else:
            target = int(response)
            if target < 0 or target >= len(monsters):
                logging.warning(f"    Not a valid target; enter a number between 0 and {len(monsters)-1}")
            else:
                # TODO:  look up the character's to hit needed
                attacker = characters[who]
                col = get_column(attacker)
                defender = monsters[target]
                row = int(defender['ac']) + 10
                logging.debug(f"Row {row} Column {col}")
                logging.debug(f"    {attacker['name']} type is {attacker['type']}")
                logging.info(f"    {attacker['name']} (level {attacker['level']}) needs a {to_hit_table[attacker['type']][col][row]} to hit AC {defender['ac']}")
 
                # check for hit
                response = get_input(f"    Did {attacker['name']} hit? (0/1) ")
                if response:
                    damage = get_int_input("    How much damage did they do? ")
                    damage = int(damage)
                    apply_damage(target,damage,monsters,attacker['name'])

def apply_damage(target,damage,monsters,char_name):
    m = monsters[target]
    if (damage >= m['hp']):
        logging.info("    ++++++++++++++++++++++++++++++++")
        logging.info(f"    {char_name} dropped {m['name']}")
        logging.info("    ++++++++++++++++++++++++++++++++")
        monsters.remove(m)
        if len(monsters)==0:
            logging.info("******************************************************")
            logging.info("           ALL MONSTERS HAVE BEEN DEFEATED ")
            logging.info("******************************************************")
            exit(0)
    else:
        m['hp'] =  m['hp'] - damage


def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def set_up_round(monsters,characters):
    for attacker in monsters:
        if not attacker['fumble']:
            attacker['initiative'] = roll_die(10)
            logging.debug(f"    {attacker['name']} rolled a {attacker['initiative']} initiative")
            if int(attacker['attack_cycle']) > 1:
                swap_attacks(attacker)
            attacker['attack_segments'] = []
            attacker['attack_segments'].append(attacker['initiative'])
            if attacker['attacks'] > 1:
                offset = int(attacker['initiative'] / attacker['attacks'])
                logging.debug(f"    Offset is {offset}")
                for x in range(2,attacker['attacks']):
                    attacker['attack_segments'].append(attacker['initiative'] - (x-1)*offset)
                attacker['attack_segments'].append(0)
            logging.info(f"    {attacker['name']} will attack on segments {attacker['attack_segments']}")
        else:
            logging.info(f"    {attacker['name']} fumbled last round and loses their attack this round")
            attacker['fumble'] = False
    for character in characters:
        for spell in character['spells_active']:
            spell['duration'] -= 1
            if spell['duration'] < 0:
                logging.info(f"{character['name']} spell {spell['name']} has expired")
                character['spells_active'].remove(spell)
             
            
def set_attacks(attacker,natt):
    if "/" in natt:
        attacker['attack_round'] = 0
        attacker['attack_cycle'] = natt.split("/")[1]
        logging.debug(f'natt = {natt.split("/")[0]} / {natt.split("/")[1]}')
        attacker['attacks_per_round'] = [(int(natt.split("/")[0])/int(natt.split("/")[1]))-0.5, 
                                         (int(natt.split("/")[0])/int(natt.split("/")[1]))+0.5]
        logging.debug(f"attacks per round is {attacker['attacks_per_round']}")
    else:
        attacker['attacks'] = int(natt)
        attacker['attack_cycle'] = 1

    
def swap_attacks(attacker):
    logging.debug(f"    attack round is {attacker['attack_round']+1}")
    attacker['attacks'] = int(attacker['attacks_per_round'][attacker['attack_round']])
    logging.debug(f"    set attacks to {attacker['attacks']}")
    attacker['attack_round'] = ~attacker['attack_round']
    
def read_char_table(fi):
    characters = []
    f = open(fi,'r')
    for line in f.readlines():
        line = line.strip()
        if not "Character_Name" in line:
            columns = line.split()
            c = {}
            c['name'] = columns[0]
            c['ac'] = int(columns[1])
            c['class'] = columns[2]
            c['type'] = columns[2]
            if c['type'] == "Monk":
                c['type'] = "Cleric"
            c['level'] = int(columns[3])
            c['spells_active'] = []
            c['casting'] = False
            c['total_damage'] = 0
            logging.debug(c)
            characters.append(c)
    return(characters)


def parse(line):
    cnt = 1
    name = ''
    level = 0
    ac = 11 
    natt = 0
    dam = ''
    to_hit = 0
    to_dam = 0 
    # [cnt] name [level ac natt dam [to_hit to_dam]] 
    string = re.match("\d*\s*\D+\s*(([+-]?\d+\s+){2}((\d/\d)|\d)\s+\d+-\d+((\s+[+-]?\d+){2,2})*)*",line).group()
    tokens = string.split()
    logging.debug(f"tokens = {tokens}")
    pop_flag = False 
    if len(tokens) == 1:	# name
        name = tokens[0] 
        pop_flag = True
    elif len(tokens) == 2:	# cnt name
        cnt = int(tokens[0])
        name = tokens[1]
        pop_flag = True
    elif len(tokens) == 5:	# name HD AC #ATT DAM
        name = tokens[0]
        level = tokens[1]
        ac = tokens[2]
        natt = tokens[3]    
        dam = tokens[4]
        pop_flag = False 
    elif len(tokens) == 6:  	# cnt name HD AC #ATT DAM
        cnt = tokens[0]
        name = tokens[1]
        level = tokens[2]
        ac = tokens[3]
        natt = tokens[4]    
        dam = tokens[5]
        pop_flag = False
    elif len(tokens) == 7:      # name HD AC #ATT DAM to_hit to_dam
        name = tokens[0]
        level = tokens[1]
        ac = tokens[2]
        natt = tokens[3]    
        dam = tokens[4]
        to_hit = tokens[5]
        to_dam = tokens[6]
        pop_flag = False 
    elif len(tokens) == 8:      # cnt name HD AC #ATT DAM to_hit to_dam
        cnt = tokens[0]
        name = tokens[1]
        level = tokens[2]
        ac = tokens[3]
        natt = tokens[4]    
        dam = tokens[5]
        to_hit = tokens[6]
        to_dam = tokens[7]
        pop_flag = False

    return(cnt,name,level,ac,natt,dam,to_hit,to_dam,pop_flag)


def build_monster_roster(monster_names,monster_table):
  
    roster = [] 
    for line in monster_names:
        (cnt,name,level,ac,natt,dam,to_hit,to_dam,pop_flag) =  parse(line)
        logging.debug(f"Parsed string is: {cnt} {name} {level} {ac} {natt} {dam} {to_hit} {to_dam} {pop_flag}")
        attacker = {} 
        if pop_flag:
            idx = next((index for (index, d) in enumerate(monster_table) if d["Name"] == name), None) 
            if idx:
                m = monster_table[idx]
                set_attacks(attacker,m['NATT'])
                attacker['ac'] = m['AC']
                attacker['hp'] = get_monster_hp(m, 1, maxhp=True)[0]
                attacker['max_hp'] = attacker['hp'] 
                attacker['level'] = int(m['level'])
                attacker['damage'] = m['DA']
            else:
                logging.error(f"Can't find {name} in monster_table!!!")
                exit(1)
        else:
            set_attacks(attacker,natt)
            attacker['ac'] = ac
            attacker['level'] = int(level)
            attacker['hp'] = int(attacker['level']) * 8
            attacker['max_hp'] = attacker['hp'] 
            attacker['damage'] = dam
        
        attacker['type'] = "Monster"
        attacker['opponent'] = -1 
        attacker['to_hit_mod'] = int(to_hit)
        attacker['to_dam_mod'] = int(to_dam)
        attacker['crit'] = False
        attacker['fumble'] = False
        for num in range(1,cnt+1):
            new_attacker = copy.deepcopy(attacker)
            if cnt > 1:
                new_attacker['name'] = name + f"_{num}"
            else:
                new_attacker['name'] = name
            roster.append(new_attacker)
            logging.debug(new_attacker) 

    return(roster)
 

def read_monster_names(fi):
    monsters = []
    f = open(fi,'r')
    for line in f.readlines():
        line = line.strip()
        if not "Monster_Type" in line:
            monsters.append(line.strip())
    return(monsters)


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
    logging.info(f'    {"Character Roster" : <20}|DAM| Opponent(s) | Active spells')
    logging.info('    ====================================')
    for c in characters:
        str = ''
        str1 = str + f"    {cnt} : {c['name'] : <16}|{c['total_damage'] : 3}"
        str2 = '| '
        for m in monsters:
            if m['opponent'] ==  cnt:
                str2 = str2 + f" {m['name']} |"
        str3 = ' | '
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
    parser.add_argument("monster_table",help="Monster roset file")
    parser.add_argument("-v", "--verbose", help="Logging level", default="INFO")


#    group.add_argument("-c", "--class_name", help="Character class to generate",
#                       choices=["Cleric", "Druid", "Fighter", "Paladin", "Ranger", "Magic-User", "Illusionist", "Thief",
#                                "Assassin", "Monk", "CA", "CF", "CM", "CR", "CT", "CFM", "FA", "FI", "FM", "FT", "FMT",
#                                "IT", "MT"])
#    group.add_argument("-p", "--party", help="Generate an NPC Party of specified type",
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

