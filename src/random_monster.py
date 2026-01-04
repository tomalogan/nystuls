#!/Users/thomaslogan/miniconda3/bin/python

import logging
import argparse
import textwrap
import random
from argparse import ArgumentDefaultsHelpFormatter
import os, re, sys
from random_treasure import get_random_treasure
from monster_utils import get_monster_hp
from monster_utils import read_monsters

def process_list_into_string(mylist):
    out = "{}".format(mylist[0])
    for x in range(1, len(mylist)):
        out = out + ",{}".format(mylist[x])
    return out


def get_cnt(monster):
    napp = monster['NAPP']
    if "-" in napp:
        lo = int(napp.split("-")[0])
        hi = int(napp.split("-")[1])
        cnt = random.randint(lo, hi)
    else:
        cnt = int(napp)
    return (cnt)


def Print_Monster(m, cnt, hp_list, in_lair):
    if in_lair:
        out = "{} {} (in lair) ".format(cnt, m['Name'])
    else:
        out = "{} {} (not in lair) ".format(cnt, m['Name'])

    hp_string = process_list_into_string(hp_list)
    out = out + "(HD: {}, HP: {}, AC: {}, MV: {}, #A: {}, DA: {}, SA: {}, SD: {}, ".format(
        m['HD'], hp_string, m['AC'], m['MV'], m['NATT'], m['DA'], m['SA'], m['SD'])

    if m['MR'] != 0:
        out = out + "MR: {}, ".format(m['MR'])
    out = out + "I: {}, Ali: {}, Size: {})".format(m['Int'], m['Ali'], m['Size'])

    wrapper = textwrap.TextWrapper(initial_indent="\t", width=72, subsequent_indent="\t")
    out = wrapper.fill(out)
    logging.info("{}".format(out))
    logging.debug("{}".format(m['TT']))

def get_water_monster(freq_list):
    water_monsters = [d for d in freq_list if '//' in d.get('MV')]
    if len(water_monsters) > 0:
        monster_index = random.randint(0, len(water_monsters) - 1)
        return water_monsters[monster_index]
    else:
        return None


def get_flying_monster(freq_list):
    tmp = [d for d in freq_list if '/' in d.get('MV')]
    flying_monsters = [d for d in tmp if '//' not in d.get('MV')]
    if len(flying_monsters) > 0:
        monster_index = random.randint(0, len(flying_monsters) - 1)
        return flying_monsters[monster_index]
    else:
        return None


encounter_table = [[16, 19, 20, -1, -1, -1, -1, -1, -1, -1],  # 1st
                   [12, 16, 18, 19, 20, -1, -1, -1, -1, -1],  # 2nd
                   [12, 16, 18, 19, 20, -1, -1, -1, -1, -1],  # 3rd
                   [5, 10, 16, 18, 19, 20, -1, -1, -1, -1],  # 4th
                   [3, 6, 12, 16, 18, 19, 20, -1, -1, -1],  # 5th
                   [2, 4, 6, 12, 16, 18, 19, 20, -1, -1],  # 6th
                   [1, 3, 5, 10, 14, 16, 18, 19, 20, -1],  # 7th
                   [1, 2, 4, 7, 10, 14, 16, 18, 19, 20],  # 8th
                   [1, 2, 3, 5, 8, 12, 15, 17, 19, 20],  # 9th
                   [1, 2, 3, 4, 6, 9, 12, 16, 19, 20],  # 10th
                   [1, 2, 3, 4, 6, 9, 12, 16, 19, 20],  # 11th
                   [1, 2, 3, 4, 5, 7, 9, 12, 18, 20],  # 12th
                   [1, 2, 3, 4, 5, 7, 9, 12, 18, 20],  # 13th
                   [1, 2, 3, 4, 5, 6, 8, 11, 17, 20],  # 14th
                   [1, 2, 3, 4, 5, 6, 8, 11, 17, 20],  # 15th
                   [1, 2, 3, 4, 5, 6, 7, 10, 16, 20]]  # 16th


def get_random_monster(monster_table, party_level=None, name=None, water=False, flying=False): 

    if name:
        monster = [d for d in monster_table if d.get('Name') == name][0]

    elif party_level: 
        logging.info("Found party_level: {}".format(party_level))
        encounter_table_level = random.randint(1, 20)
        logging.info("Rolled a {} for level determination matrix".format(encounter_table_level))
        if party_level > 16:
            party_level = 16
        for index,encounter_table_level in enumerate(encounter_table[party_level - 1]):
            logging.info("encounter_table_level {} : party_level {}".format(encounter_table_level, party_level))
            if encounter_table_level >= party_level:
                monster_level = index + 1
                break
        logging.info("For a party of level {}, looking for monsters of level {}".format(party_level, monster_level))

        # Make a list of monsters for this level
        lvl_list = [d for d in monster_table if int(d.get('Lvl')) == monster_level]
        logging.info("Got level {} list:".format(monster_level))
        for monster in lvl_list:
            logging.info("    {}".format(monster['Name']))

        # Determine frequency type to choose
        freqs = ['C', 'U', 'R', 'V']
        pct = random.randint(1, 100)
        if pct <= 65:
            cnt = 0
        elif pct <= 85:
            cnt = 1
        elif pct <= 96:
            cnt = 2
        elif pct <= 100:
            cnt = 3
        monster = None
        while not monster and cnt < len(freqs):
            f = freqs[cnt]
            logging.debug("Looking for frequency of {}".format(f))
            freq_list = [d for d in lvl_list if d.get('Freq') == f]
            logging.debug("Frequency list is {}".format(freq_list))
            length = len(freq_list)
            logging.debug("Found level {} frequency type {} list of {} monsters".format(args.level, f, length))
            if length > 0:
                if water:
                    monster = get_water_monster(freq_list)
                elif flying:
                    monster = get_flying_monster(freq_list)
                else:
                    move = "//"  # exclude water monsters
                    while "//" in move:
                        num = random.randint(0, length - 1)
                        monster = freq_list[num]
                        move = monster['MV']
                if not monster:
                    cnt = cnt + 1
            else:
                cnt = cnt + 1
    if monster:
        cnt = get_cnt(monster)
        hp_list = get_monster_hp(monster, cnt, maxhp = False)
        in_lair = determine_in_lair(monster)
        Print_Monster(monster, cnt, hp_list, in_lair)
        get_treasure(monster,in_lair)
    else:
        logging.info("Sorry, unable to find requested encounter.  Try again...")


def determine_in_lair(monster):
    in_lair = False
    if monster['Lair'] != 0:
        pct = random.randrange(1, 100)
        if pct < int(monster['Lair']):
            in_lair = True
    return(in_lair)

    
def get_treasure(monster,in_lair):
    logging.debug("Looking for treasure type: {}".format(monster['TT']))
    if monster['TT'] == "special":
        out = "Treasure: special"
    elif monster['TT'] == None:
        out = "Treasure: None"
    else:
        out = 'Treasure: '
        tokens = re.findall('([A-Z](x[\d]+)?)',monster['TT'])
        logging.info('tokens: {}'.format(tokens))
        for token in tokens:
            logging.info('token is {}'.format(token))
            if '-' in token:
                if not in_lair:
                    break
            else:
                multiplier = 1
                parts = token[0].split('x')
                if len(parts) == 2:
                    multiplier = list(filter(lambda x: x.isdigit(), parts[1]))
                    print('found {} multiplier for treasure type: {}', multiplier, parts[0])
                if re.match('[A-Z]',parts[0]):
                    out = out + get_random_treasure(parts[0], multiplier)
                else:
                    logging.info("Unable to find treasure")

    wrapper = textwrap.TextWrapper(initial_indent="\t", width=72, subsequent_indent="\t")
    out = wrapper.fill(out)
    logging.info("{}".format(out))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Monster Generator",
                                     formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--verbose", help="Logging level", default="INFO")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--name", help="Name of monster to to generate")
    group.add_argument("-l", "--level", help="Level of encounter to generate", type=int)
    parser.add_argument("-w", "--water", help="Generate a water encounter", action="store_true")
    parser.add_argument("-f", "--flying", help="Generate a flying encounter", action="store_true")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    loglevel = args.verbose
    numeric_level = getattr(logging, loglevel.upper(), None)
    #    if not isinstance(numeric_level, int):
    #         raise ValueError('Invalid log level: %s' % loglevel)
    logFile = "monsters.log"
    logging.basicConfig(filename=logFile, format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=numeric_level)
    logging.getLogger().addHandler(logging.StreamHandler())
   
    logging.info("Reading monster table")
    monster_table = read_monsters()
    logging.info("Starting random monster generation") 

    get_random_monster(monster_table, party_level=args.level, name=args.name, water=args.water, flying=args.flying)
