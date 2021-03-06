#!/usr/local/bin/python3

import copy
import argparse
import sys
import logging
import random
import re
import random
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
  

def roll_die(sides):
    return random.randint(1,sides)

def get_column(attacker):
    col = 0
    for x in to_hit_level[attacker['type']]:
        logging.debug(f"Checking level {x}")
        if attacker['level'] >= x:
            col = col + 1
        else:
            break
    return col

def is_hit(attacker,defender):
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
            logging.info("    FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE ---")
            if roll < 3:
                logging.info(f"    FUMBLE -- attacker {attacker['name']} fumbled - make a dexterity check")
            elif roll <5:
                logging.info(f"    FUMBLE -- attacker {attacker['name']} fumbled - make a 1/2 dexteriry check")
            else:
                logging.info(f"    FUMBLE -- attacker {attacker['name']} fumbled - make a weapon saving throw")
            logging.info("    FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE --- FUMBLE ---")

#        attacker['off_hand'] = ~attacker['off_hand']


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
        t = attacker['damage'].split("-")
        list = attacker['damage'].split("/")
        print(f"Damage values {list}")
        if len(list) <= attacker['attack_number']:
            attacker['attack_number'] = 0
        t = list[attacker['attack_number']].split("-")

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

def print_action(name, opponent_int, num_characters):
    if opponent_int >= 0 and opponent_int < num_characters:
        logging.info(f"    {name} opponent set to {opponent_int}")
    elif opponent_int == -1:
        logging.info(f"    {name} holding action until next segment")
    elif opponent_int == -2:
        logging.info(f"    {name} not attacking this round")
    elif opponent_int == -99:
        logging.info( "    Combat is over!!!!")
        exit(1)
 

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


def decrement_spell_times(characters):
    for c in characters:
        if casting(c):
            for spell in c['spells_active']:
                print(f"    {c['name']} is casting")
                if spell['casting_time'] >= 0:
                    spell['casting_time'] -= 1
                if spell['casting_time'] == 0:
                    logging.info(f"    {c['name']} spell {spell['name']} goes off")
                    spell['casting'] = False
                elif spell['casting_time'] > 0:
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

def display_intro():
    logging.info("================================================================================")
    logging.info("RUN COMBAT")
    logging.info("================================================================================")
    logging.info("Getting monster tables")

def combat_over(monsters):
    if len(monsters) == 0:
        return True
    else:
        return False


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
                if not combat_over(monsters) and not healing:
                    attacker['attack_segments'].remove(segment) 
                    attack(attacker,characters[attacker['opponent']])
                    attacker['attack_number'] += 1
                    if characters[attacker['opponent']]['opponent'] == -1:
                        which =  [i for i, e in enumerate(monsters) if e == attacker]
                        characters[attacker['opponent']]['opponent'] = int(which[0])


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
                    player_actions(monsters,characters)
                    decrement_spell_times(characters)
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


def get_int_input(str):
    target = 'A'
    while not is_number(target):
        target = input(str) 
    return(int(target))

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
                                              
def cast_spell(character):
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
    if not combat_over(monsters):
        while not response == '':
            who = -99
            while who >= len(characters) or who < 0:
                who = get_input("    Who's action is it (return to exit): ")
                if not is_number(who):
                    return()
            attacker = characters[who]
            response = get_input(f"    Who is {attacker['name']} attacking? (s for spell, enter for {attacker['opponent']})  ",specials=['s'])
            if response == 's':
                cast_spell(attacker)
                return
            elif response == '':
                target = int(attacker['opponent'])
            else:
                target = int(response)

            hi = max(m['number'] for m in monsters)
            if target < 0 or target > hi:
                logging.warning(f"    Not a valid target; enter a number between 0 and {hi}")
            else:
                defender_list = [d for i,d in enumerate(monsters) if d['number'] == target]
                if not defender_list:
                    logging.warning(f"    No target {target} exists!; enter a valid target")
                    response = 1
                else:
                    defender = defender_list[0]
                    col = get_column(attacker)
                    row = int(defender['ac']) + 10
                    logging.debug(f"Row {row} Column {col}")
                    logging.debug(f"    {attacker['name']} type is {attacker['type']}")
                    logging.info(f"    {attacker['name']} (level {attacker['level']}) needs a {to_hit_table[attacker['type']][col][row]} to hit AC {defender['ac']}")

                    # check for hit
                    response = get_input(f"    Did {attacker['name']} hit? (0/1) ")
                    if response:
                        if defender['opponent'] == -1:
                            defender['opponent'] = who                      
                        if attacker['opponent'] == -1:
                            attacker['opponent'] = target
                        damage = get_int_input("    How much damage did they do? ")
                        damage = int(damage)
                        if apply_damage(target,damage,monsters,attacker):
                            response=''
                     


def apply_damage(target,damage,monsters,attacker):
    m = [m for i,m in enumerate(monsters) if m['number'] == target][0]
    if (damage >= m['hp']):
        logging.info("    ++++++++++++++++++++++++++++++++")
        logging.info(f"    {attacker['name']} dropped {m['name']}")
        logging.info("    ++++++++++++++++++++++++++++++++")
        monsters.remove(m)
        if len(monsters)==0:
            logging.info("******************************************************")
            logging.info("           ALL MONSTERS HAVE BEEN DEFEATED ")
            logging.info("******************************************************")
            return(1)
        return(0)
    else:
        m['hp'] =  m['hp'] - damage
        return(0)


def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def set_up_round(round,monsters,characters):
    logging.info(f'START OF ROUND {round}')
    for attacker in monsters:
        if not attacker['fumble']:
            attacker['initiative'] = roll_die(10)
            logging.debug(f"    {attacker['name']} rolled a {attacker['initiative']} initiative")
            if int(attacker['attack_cycle']) > 1:
                swap_attacks(attacker)
            attacker['off_hand'] = False
            attacker['attack_number'] = 0
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
        total_attacks = natt.split("/")[0]
        attacker['attack_cycle'] = natt.split("/")[1]
        logging.debug(f"natt = {total_attacks} / {attacker['attack_cycle']} ")
        attacker['attacks_per_round'] = [(int(total_attacks)/int(attacker['attack_cycle']))-0.5, 
                                         (int(total_attacks)/int(attacker['attack_cycle']))+0.5]
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
            c['opponent'] = -1
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
    tokens = line.split()
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
    elif len(tokens) == 6:  	# cnt name HD AC #ATT DAM
        cnt = int(tokens[0])
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
        cnt = int(tokens[0])
        name = tokens[1]
        level = tokens[2]
        ac = tokens[3]
        natt = tokens[4]    
        dam = tokens[5]
        to_hit = tokens[6]
        to_dam = tokens[7]
    return(cnt,name,level,ac,natt,dam,to_hit,to_dam,pop_flag)


def build_monster_roster(names_table):
    monster_names = read_monster_names(names_table)
    monster_table = read_monsters()
    roster = [] 
    total_cnt = 0
    for line in monster_names:
        (cnt,name,level,ac,natt,dam,to_hit,to_dam,pop_flag) =  parse(line)
        logging.debug(f"Parsed string is: {cnt} {name} {level} {ac} {natt} {dam} {to_hit} {to_dam} {pop_flag}")
        attacker = {} 
        if pop_flag:
            found = False
            for m in monster_table:
                new_name = ''
                for word in m['Name'].split():
                    new_name = new_name + word
                if new_name == name:
                    set_attacks(attacker,m['NATT'])
                    attacker['ac'] = m['AC']
                    attacker['hp'] = get_monster_hp(m, 1, maxhp=True)[0]
                    attacker['max_hp'] = attacker['hp']
                    attacker['level'] = int(m['level'])
                    attacker['damage'] = m['DA']
                    found = True
                    break
            if not found:
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
        for num in range(0,cnt):
            new_attacker = copy.deepcopy(attacker)
            if cnt > 0:
                new_attacker['name'] = name + f"_{num}"
            else:
                new_attacker['name'] = name
            new_attacker['number'] = total_cnt
            total_cnt += 1
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

def print_tables(segment, characters,monsters):
    print('')
    print("================================================================================")
    logging.info(f"==================================  SEGMENT {segment : >2}   ===============================")
    print("================================================================================")
    print("  # : NAME            : DAM :  #  : OPPONENT NAME: HP :")
    print("================================================================================")
    cnt = 0
    monsters_done = []
    char_strings = []
    for c in characters:
        printed = False
        str = ''
        str1 = str + f"{cnt : 3} : {c['name'] : <16}: {c['total_damage'] : 3} "
        str2 = ':'
        str3 = ''

        hit_monster = False
        hit_spell = False
        opponents = [] 
        for m in monsters:
            if m['opponent'] == cnt:
                opponents.append(m)
        monst_cnt = len(opponents)
        spell_cnt = len(c['spells_active'])

        while monst_cnt or spell_cnt:
            if monst_cnt:
                m = opponents.pop()
                monst_cnt -= 1
                str2 = f": {m['number'] : <3} : {m['name'] : <12} : {m['hp'] : <3}:"
                monsters_done.append(m)
            else:
                str2 = ":     :              :    :"

            if spell_cnt > 0:
                spell = c['spells_active'][spell_cnt-1]
                if spell['casting']:
                    str3 = f" casting {spell['name']} {spell['casting_time']} "
                else:
                    str3 = f" {spell['name']} has {spell['duration']} rds "
                spell_cnt -= 1
            else:
                str3 = ''
            str = str1 + str2 + str3 
            char_strings.append(str)
            printed = True
            str1 = "    :                 :     "

        if not printed:   
            str2 = ":     :              :    :"
            str = str1 + str2 + str3 
            char_strings.append(str)
        char_strings.append('--------------------------------------------------------------------------------')
         
        cnt += 1

    monster_strings = []
    cnt = 100
    for m in monsters:
        if m not in monsters_done:
            tmp = "                            "
            tmp = tmp + f": {m['number'] : <3} : {m['name'] : <12} : {m['hp'] : <3}:"
            monster_strings.append(tmp)
            monster_strings.append('--------------------------------------------------------------------------------')
   
    for s in char_strings:
        print(s)
    for m in monster_strings:
        print(m)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dungeon Master's Assitant")
    parser.add_argument("char_table",help="Character roster file")
    parser.add_argument("monster_table",help="Monster roster file")
    parser.add_argument("-v", "--verbose", help="Logging level", default="INFO")

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

