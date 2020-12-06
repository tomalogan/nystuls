#!/usr/local/bin/python3

import argparse
import sys
import logging
import random

to_hit_table = {}
to_hit_level = {}
to_hit_table['Cleric'] =[[25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10],
 [23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8],
 [21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6],
 [20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4],
 [20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
 [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
 [19, 18, 17, 16, 15, 14, 13, 12, 11, 10,  9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, -1]]
to_hit_level['cleric'] = [4, 7, 10, 13, 16, 19]

to_hit_table['Magic-User'] = [[26, 25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11],
 [24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9],
 [21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6],
 [20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3],
 [20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 ]]
to_hit_level['cleric'] = [6, 11, 16, 21]

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

to_hit_table['Theif'] = [[26, 25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11],
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
    logging.info(f"    {attacker['name']} type is {attacker['type']}")
    logging.info(f"    {attacker['name']} (level {attacker['level']}) needs a {to_hit_table[attacker['type']][col][row]} to hit AC {defender['ac']}")
    die_roll = roll_die(20) + attacker['to_hit_mod'] 
    if die_roll > 20:
        die_roll -= 5
        if die_roll < 20:
            die_roll = 20
    if die_roll >= to_hit_table[attacker['type']][col][row]:
        hit = True
        logging.info(f"    Rolled {die_roll} - hit")
    else:
        hit = False
        logging.info(f"    Rolled {die_roll} - miss")
    return(hit)
   
def attack(attacker,defender):
    logging.info(f"    {attacker['name']} is attacking {defender['name']}")
    if is_hit(attacker,defender):
        damage = calc_damage(attacker)
        logging.info (f"    {defender['name']} is hit by {attacker['name']} for {damage} points.")

def calc_damage(attacker):
    return 5

def get_opponent(attacker,num_characters):

    target = attacker['opponent']    

    str1 = f"    Who is {attacker['name']} attacking? "
    str2 = f"character number, enter (no change - use {target}), -1 (no one): "
    str = str1 + str2
 
    combat_over = False
    done = False
    opponent = ''
    while not done:  
        while not is_number(opponent):
            opponent = input(str) 
            if opponent == '':
                logging.info(f"    {attacker['name']} re-using opponent {target}")
                opponent = f"{target}"
        opponent_int = int(opponent)
        logging.debug(f"opponent_int is {opponent_int}")
        done = True
        if opponent_int == -1:
            logging.info("    Setting opponent to None (-1)")
            attacker['opponent'] = -1
        elif opponent_int >= 0 and opponent_int <= num_characters:
            logging.info(f"    Setting opponent to {opponent_int}")
            attacker['opponent'] = opponent_int
        elif opponent_int == -99:
            logging.info("    Combat is over!!!!")
            combat_over = True
        else:
            logging.info(f"Invalid opponent entered {opponent}; please enter a value of -1 to {num_characters}")
            opponent = ''
            done = False
    return combat_over


def run_combat(characters,monsters):
    logging.info("==================================================")
    logging.info("RUN COMBAT")
    logging.info("==================================================")

    # roll up monster treasures

    combat_over = False
    round = 1
    while not combat_over:
        # Run this round
        logging.info(f'START OF ROUND {round}')
        set_up_round(monsters)
        for init in range(10,-1,-1):
            if not combat_over:
                logging.info('')
                logging.info(f"SEGMENT {init} ----------------------------------------")
                for attacker in monsters:
                    while init in attacker['attack_segments'] and not combat_over:
                        print_character_roster(characters,monsters)
                        combat_over = get_opponent(attacker,len(characters))
                        if (attacker['opponent'] >= 0) and not combat_over:
                            attack(attacker,characters[attacker['opponent']])
                            attacker['attack_segments'].remove(init) 
                if not combat_over:
                    player_damage(monsters)
        logging.info('')
        logging.info(f'END OF ROUND {round}')
        logging.info('')
        logging.info('================================================================')
        logging.info('')
        round += 1


def player_damage(monsters):
    target = 1
    while not target == '':
        print_monster_roster(monsters)
        str = "    Who is player attacking (return to exit): " 
        damage_str = "    How much damage did they do? "
        target = input(str)
        if not (target == ''):
            while not is_number(target):
                target = input(str) 
            target = int(target)
            if target < 0 or target > len(monsters):
                logging.warning(f"Not a valid target; enter a number between 0 and {len(monsters)}")                
            else:
                damage = input(damage_str)
                while not is_number(damage):
                    damage = input(str) 
                damage = int(damage)
                apply_damage(target,damage,monsters)

def apply_damage(target,damage,monsters):
    m = monsters[target]
    if (damage >= m['hp']):
        logging.info(f"Player dropped {m['name']}")
        monsters.remove(m)
    else:
        m['hp'] =  m['hp'] - damage

def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def set_up_round(monsters):

    for attacker in monsters:
        attacker['initiative'] = roll_die(10)
        logging.info(f"    {attacker['name']} rolled a {attacker['initiative']} initiative")

        if attacker['attack_cycle'] > 1:
            swap_attacks(attacker)

        attacker['attack_segments'] = []
        attacker['attack_segments'].append(attacker['initiative'])
        if attacker['attacks'] > 1:
            offset = int(attacker['initiative'] / attacker['attacks'])
            print(f"Offset is {offset}")
            for x in range(2,attacker['attacks']):
                attacker['attack_segments'].append(attacker['initiative'] - (x-1)*offset)
            attacker['attack_segments'].append(0)
        logging.info(f"    {attacker['name']} will attack on segments {attacker['attack_segments']}")
            
    
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
            c['ac'] = columns[1]
            logging.debug(c)
            characters.append(c)
    return(characters)

def read_monster_table(fi):
    monsters = []
    f = open(fi,'r')
    for line in f.readlines():
        line = line.strip()
        if not "Monster_Type" in line:
            columns = line.split()
            print(line)
            print(columns)
            attacker = {}
            attacker['type'] = "Monster"
            attacker['name'] = columns[0]
            attacker['level'] = int(columns[1])
            if "/" in columns[2]:
                attacker['attack_round'] = 0
                attacker['attack_cycle'] = int(columns[2][2])
                attacker['attacks_per_round'] = [int(columns[2][0])/int(columns[2][2])-0.5,int(columns[2][0])/int(columns[2][2])+0.5]
                logging.debug(f"attacks per round is {attacker['attacks_per_round']}")
            else:
                attacker['attacks'] = int(columns[2])
                attacker['attack_cycle'] = 1
            attacker['to_hit_mod'] = int(columns[3])
            attacker['to_dam_mod'] = int(columns[4])
            attacker['hp'] = attacker['level'] * 8
            attacker['opponent'] = -1 
            logging.debug(attacker) 
            monsters.append(attacker)
    return(monsters)


def print_monster_roster(monsters):
    cnt = 0
    logging.info('')
    logging.info('    Monster Roster')
    logging.info('    ================')
    for m in monsters:
        logging.info(f"    {cnt} : {m['name'] : <20} : {m['opponent'] : <3} : {m['hp']}")
        cnt = cnt + 1


def print_character_roster(characters,monsters):
    cnt = 0
    logging.info('')
    logging.info('    Character Roster')
    logging.info('    ================')
    for c in characters:
        str = ''
        str1 = str + f"    {cnt} : {c['name'] : <16} "
        str2 = '| Opponents: '
        for m in monsters:
            if m['opponent'] ==  cnt:
                str2 = str2 + f" {m['name']}"
        cnt += 1
        str = str1 + str2 
        logging.info(str)


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

    chars = read_char_table(args.char_table)
    monst = read_monster_table(args.monster_table)

    run_combat(chars,monst)

