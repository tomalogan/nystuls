#!/usr/bin/python

import logging
import argparse
import textwrap
import random
from argparse import ArgumentDefaultsHelpFormatter
import os, re, sys
from random_treasure import get_random_treasure


def read_monsters():
    etcFile = "monsters.txt"
    etcPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'etc'))
    etcFile = os.path.join(etcPath, etcFile)

    f = open(etcFile, "r")
    monsters = []
    cnt = -1
    for line in f:
        t = line.strip().split(",")
        if len(t) == 1:
            # New book
            logging.debug("Reading monsters from {}".format(t[0]))
        else:
            m = {}
            m['Name'] = t[0]
            m['Freq'] = t[1]
            m['NAPP'] = t[2]
            m['AC'] = t[3]
            m['MV'] = t[4]
            m['HD'] = t[5]
            if "-" in m['HD']:
                logging.debug("Found dash in HD: {} {}".format(t[0], t[5]))
            m['Lair'] = t[6]
            m['TT'] = t[7]
            m['NATT'] = t[8]
            m['DA'] = t[9]
            m['SA'] = t[10]
            m['SD'] = t[11]
            m['MR'] = t[12]
            m['Int'] = t[13]
            m['Ali'] = t[14]
            m['Size'] = t[15]
            m['Lvl'] = int(t[16])

            str = "{} Freq: {},NumApp: {},AC: {},MV: {},HD: {},InLair: {},TreasureType: {},NumAtt: {}, \
Dam/Att: {},SA: {},SD: {},MR: {},I: {},Ali: {},Size: {},Level: {}".format(
                m['Name'], m['Freq'], m['NAPP'], m['AC'], m['MV'], m['HD'], m['Lair'], m['TT'],
                m['NATT'], m['DA'], m['SA'], m['SD'], m['MR'], m['Int'], m['Ali'], m['Size'], m['Lvl'])
            wrapper = textwrap.TextWrapper(initial_indent="\t", width=72, subsequent_indent="\t")
            out = wrapper.fill(str)
            logging.debug("{}".format(out))
            monsters.append(m)
    return (monsters)


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


def Print_Monster(m, cnt, hp_list, inlair):
    if inlair:
        out = "{} {} (in lair) ".format(cnt, m['Name'])
    else:
        out = "{} {} (not in lair) ".format(cnt, m['Name'])

    hp_string = process_list_into_string(hp_list)
    out = out + "(HD: {}, HP: {}, AC: {}, MV: {}, #A: {}, DA: {}, SA: {}, SD: {}, ".format(
        m['HD'], hp_string, m['AC'], m['MV'], m['NATT'], m['DA'], m['SA'], m['SD'])

    if m['MR'] != 0:
        out = out + "MR: {}%, I: {}, Ali: {}, Size: {})".format(m['MR'], m['Int'], m['Ali'], m['Size'])
    else:
        out = out + "I: {}, Ali: {}, Size: {})".format(m['Int'], m['Ali'], m['Size'])

    wrapper = textwrap.TextWrapper(initial_indent="\t", width=72, subsequent_indent="\t")
    out = wrapper.fill(out)
    logging.info("{}".format(out))


def get_water_monster(freq_list):
    water_monsters = [d for d in freq_list if '//' in d.get('MV')]
    if len(water_monsters) > 0:
        num = random.randint(0, len(water_monsters) - 1)
        return water_monsters[num]
    else:
        return None


def get_flying_monster(freq_list):
    tmp = [d for d in freq_list if '/' in d.get('MV')]
    flying_monsters = [d for d in tmp if '//' not in d.get('MV')]
    if len(flying_monsters) > 0:
        num = random.randint(0, len(flying_monsters) - 1)
        return flying_monsters[num]
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


def get_random_monster(monser_table, level=None, name=None, water=False, flying=False):
    if level:
        num = random.randint(1, 20)
        logging.debug("Rolled a {} for level determination matrix".format(num))
        if level > 16:
            level = 16
        mylist = encounter_table[level - 1]
        for x in range(len(mylist)):
            if num <= mylist[x]:
                monster_level = x + 1
                break

        logging.debug("For a party of level {}, looking for monsters of level {}".format(level, monster_level))

        # Make a list of monsters for this level
        lvl_list = [d for d in monster_table if int(d.get('Lvl')) == monster_level]
        logging.debug("Got level {} list of {}".format(monster_level, lvl_list))

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
            hp_list = get_monster_hp(monster, cnt)
            if monster['Lair'] != 0:
                pct = random.randint(1, 100)
                if pct < int(monster['Lair']):
                    inlair = True
                else:
                    inlair = False
            else:
                inlair = False
            Print_Monster(monster, cnt, hp_list, inlair)
            get_treasure(monster)
        else:
            logging.info("Sorry, unable to find requested encounter.  Try again...")

    elif name:
        monster = [d for d in monster_table if d.get('Name') == name][0]
        cnt = get_cnt(monster)
        hp_list = get_monster_hp(monster, cnt)
        if monster['Lair'] != 0:
            pct = random.randint(1, 100)
            if pct < int(monster['Lair']):
                inlair = True
            else:
                inlair = False
        else:
            inlair = False
        Print_Monster(monster, cnt, hp_list, inlair)
        get_treasure(monster)


def get_treasure(monster):
    t = monster['TT']
    if t == "special":
        out = "Treasure: special"
    elif t == None:
        out = "Treasure: None"
    else:
        for x in range(len(t)):
            letter = t[x]
            if not letter.isdigit() and letter != "-":
                num = 1
                if letter == "x":
                    if len(t) >= x + 2:  # may have 2 digit number
                        if t[x + 2].isdigit():
                            num = int(t[x + 1:x + 2])
                        else:
                            num = int(t[x + 1])
                    else:
                        num = int(t[x + 1])
                    out = 'Treasure: '
                    for x in range(num - 1):
                        out = out + get_random_treasure(last)
                else:
                    out = 'Treasure: '
                    out = out + get_random_treasure(letter)
                last = letter

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

    monster_table = read_monsters()
    get_random_monster(monster_table, level=args.level, name=args.name, water=args.water, flying=args.flying)
