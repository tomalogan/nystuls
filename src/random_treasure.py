#!/usr/b}in/python
from utils import * 
import string
import argparse
import logging
import random
import textwrap

types = list(string.ascii_uppercase)
copper = [[1, 6, 25],  # A
          [1, 8, 50],  # B
          [1, 12, 20],  # C
          [1, 8, 10],  # D
          [1, 10, 5],  # E
          [0, 0, 0],  # F
          [0, 0, 0],  # G
          [5, 30, 25],  # H
          [0, 0, 0],  # I
          [3, 24, 100],  # J
          [0, 0, 0],  # K
          [0, 0, 0],  # L
          [0, 0, 0],  # M
          [0, 0, 0],  # N
          [1, 4, 25],  # O
          [0, 0, 0],  # P
          [0, 0, 0],  # Q
          [0, 0, 0],  # R
          [0, 0, 0],  # S
          [0, 0, 0],  # T
          [0, 0, 0],  # U
          [0, 0, 0],  # V
          [0, 0, 0],  # W
          [0, 0, 0],  # X
          [0, 0, 0],  # Y
          [1, 3, 20]]  # Z
silver = [[1, 6, 30],  # A
          [1, 6, 25],  # B
          [1, 6, 30],  # C
          [1, 12, 15],  # D
          [1, 12, 25],  # E
          [1, 20, 10],  # F
          [0, 0, 0],  # G
          [1, 100, 40],  # H
          [0, 0, 0],  # I
          [0, 0, 0],  # J
          [3, 18, 100],  # K
          [0, 0, 0],  # L
          [0, 0, 0],  # M
          [0, 0, 0],  # N
          [1, 2, 20],  # O
          [1, 6, 30],  # P
          [0, 0, 0],  # Q
          [0, 0, 0],  # R
          [0, 0, 0],  # S
          [0, 0, 0],  # T
          [0, 0, 0],  # U
          [0, 0, 0],  # V
          [0, 0, 0],  # W
          [0, 0, 0],  # X
          [0, 0, 0],  # Y
          [1, 4, 25]]  # Z
electrum = [[1, 6, 35],  # A
            [1, 4, 25],  # B
            [1, 4, 10],  # C
            [1, 8, 15],  # D
            [1, 6, 25],  # E
            [1, 12, 15],  # F
            [0, 0, 0],  # G
            [10, 40, 40],  # H
            [0, 0, 0],  # I
            [0, 0, 0],  # J
            [0, 0, 0],  # K
            [2, 12, 100],  # L
            [0, 0, 0],  # M
            [0, 0, 0],  # N
            [0, 0, 0],  # O
            [1, 2, 25],  # P
            [0, 0, 0],  # Q
            [0, 0, 0],  # R
            [0, 0, 0],  # S
            [0, 0, 0],  # T
            [0, 0, 0],  # U
            [0, 0, 0],  # V
            [0, 0, 0],  # W
            [0, 0, 0],  # X
            [0, 0, 0],  # Y
            [1, 4, 25]]  # Z
gold = [[1, 10, 40],  # A
        [1, 3, 25],  # B
        [0, 0, 0],  # C
        [1, 6, 50],  # D
        [1, 8, 25],  # E
        [1, 10, 40],  # F
        [10, 40, 50],  # G
        [10, 60, 55],  # H
        [0, 0, 0],  # I
        [0, 0, 0],  # J
        [0, 0, 0],  # K
        [0, 0, 0],  # L
        [2, 8, 100],  # M
        [0, 0, 0],  # N
        [0, 0, 0],  # O
        [0, 0, 0],  # P
        [0, 0, 0],  # Q
        [2, 8, 40],  # R
        [0, 0, 0],  # S
        [0, 0, 0],  # T
        [0, 0, 0],  # U
        [0, 0, 0],  # V
        [5, 30, 60],  # W
        [0, 0, 0], # X
        [2, 12, 70], # Y
        [1, 4, 30]]  # Z
platinum = [[1, 4, 25],  # A
            [0, 0, 0],  # B
            [0, 0, 0],  # C
            [0, 0, 0],  # D
            [0, 0, 0],  # E
            [1, 8, 35],  # F
            [1, 20, 50],  # G
            [5, 50, 25],  # H
            [3, 18, 30],  # I
            [0, 0, 0],  # J
            [0, 0, 0],  # K
            [0, 0, 0],  # L
            [0, 0, 0],  # M
            [1, 6, 100],  # N
            [0, 0, 0],  # O
            [0, 0, 0],  # P
            [0, 0, 0],  # Q
            [10, 60, 50],  # R
            [0, 0, 0],  # S
            [0, 0, 0],  # T
            [0, 0, 0],  # U
            [0, 0, 0],  # V
            [1, 8, 15],  # W
            [0, 0, 0],  # X
            [0, 0, 0],  # Y
            [1, 6, 30]]  # Z
gems = [[4, 40, 60],  # A
        [1, 8, 30],  # B
        [1, 6, 25],  # C
        [1, 10, 30],  # D
        [1, 12, 15],  # E
        [3, 30, 20],  # F
        [5, 20, 30],  # G
        [1, 100, 50],  # H
        [2, 20, 55],  # I
        [0, 0, 0],  # J
        [0, 0, 0],  # K
        [0, 0, 0],  # L
        [0, 0, 0],  # M
        [0, 0, 0],  # N
        [0, 0, 0],  # O
        [0, 0, 0],  # P
        [1, 4, 50],  # Q
        [4, 32, 55],  # R
        [0, 0, 0],  # S
        [0, 0, 0],  # T
        [10, 80, 90],  # U
        [0, 0, 0],  # V
        [10, 80, 60],  # W
        [0, 0, 0],  # X
        [0, 0, 0],  # Y
        [10, 60, 55]]  # Z
jewelry = [[3, 30, 50],  # A
           [1, 4, 20],  # B
           [1, 3, 20],  # C
           [1, 6, 25],  # D
           [1, 8, 10],  # E
           [1, 10, 10],  # F
           [1, 10, 25],  # G
           [10, 40, 50],  # H
           [1, 12, 50],  # I
           [0, 0, 0],  # J
           [0, 0, 0],  # K
           [0, 0, 0],  # L
           [0, 0, 0],  # M
           [0, 0, 0],  # N
           [0, 0, 0],  # O
           [0, 0, 0],  # P
           [0, 0, 0],  # Q
           [1, 12, 45],  # R
           [0, 0, 0],  # S
           [0, 0, 0],  # T
           [5, 30, 80],  # U
           [0, 0, 0],  # V
           [5, 40, 50],  # W
           [0, 0, 0],  # X
           [0, 0, 0],  # Y
           [5, 30, 50]]  # Z

def get_quantity(lo, hi, pct):
    if random.randrange(1, 100)<=pct:
        return(random.randrange(lo, hi))
    else:
        return(None)

def consolidate(items):
    types = []
    cnts = []
    for value in items:
        if not value in types:
            types.append(value)
            cnts.append(1)
        else:
            cnts[types.index(value)] = cnts[types.index(value)] + 1
    type_count_list = sorted(zip(types, cnts))
    gems = []
    for item in type_count_list:
        gem = {}
        gem['count'] = item[1] 
        gem['value'] = item[0] 
        gems.append(gem)
    return (gems)


base_value = [0.05, 0.25, 0.5, 1, 5, 10, 50, 100, 500, 1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]

def get_gems(cnt):
    total = 0
    gem_list = []
     
    for x in range(cnt):
        pct = random.randrange(1, 100)
        if pct <= 25:
            first_base = 5
        elif pct <= 50:
            first_base = 6
        elif pct <= 70:
            first_base = 7
        elif pct <= 90:
            first_base = 8
        elif pct <= 99:
            first_base = 9
        else:
            first_base = 10
        base = first_base 
        roll = random.randrange(1, 10)
        done = False
        while not done:
            if roll == 1:
                if base - first_base < 7:
                    base = base + 1
                    roll = random.randrange(1, 8)
                else:
                    value = base_value[base]
                    done = True
            elif roll == 2:
                value = base_value[base] * 2
                done = True
            elif roll == 3:
                value = base_value[base] * (1 + random.randrange(1, 6) / 10)
                done = True
            elif roll >= 4 and roll <= 8:
                value = base_value[base]
                done = True
            elif roll == 9:
                value = base_value[base] * (1 - random.randrange(1, 4) / 10)
                done = True
            else:
                if first_base - base < 5:
                    base = base - 1
                    roll = random.randrange(2, 10)
                else:
                    value = base_value[base]
                    done = True

        total = total + value
        gem_list.append(value)

    sorted_list = consolidate(gem_list)
    return (sorted_list, total)


def get_jewelry(cnt):
    jewelry_list = []
    total = 0
    for x in range(cnt):

        # Set base class for this piece of jewelry
        roll = random.randrange(1, 100)
        if roll <= 10:
            base = 0
        elif roll <= 20:
            base = 1
        elif roll <= 40:
            base = 2
        elif roll <= 50:
            base = 3
        elif roll <= 70:
            base = 4
        elif roll <= 90:
            base = 5
        else:
            base = 6

        # Check for workmanship increases 
        done = False
        value = 0
        while not done:
            roll = random.randrange(1, 10)
            if roll == 1:
                if base == 6:
                    done = True
                    value = 12000
                else:
                    base = base + 1
            else:
                done = True

        # Set the base value
        if value == 0:
            if base == 0:
                value = random.randrange(1, 10) * 100
            elif base == 1:
                value = random.randrange(2, 12) * 100
            elif base == 2:
                value = random.randrange(3, 18) * 100
            elif base == 3:
                value = random.randrange(5, 30) * 100
            elif base == 4:
                value = random.randrange(1, 6) * 1000
            elif base == 5:
                value = random.randrange(2, 8) * 1000
            else:
                value = random.randrange(2, 12) * 1000

        # Check for exceptional stones
        if base >= 4:
            roll = random.randrange(1, 8)
            adder = 0
            if roll == 1:
                adder = 5000
                while adder < 640000:
                    roll = random.randrange(1, 6)
                    if roll > 1:
                        break
                    else:
                        adder = adder * 2
            value = value + adder

        jewelry_list.append(value)
        total = total + value

    sorted_list = consolidate(jewelry_list)
    return (sorted_list, total)


def print_coins(cp, sp, ep, gp, pp, p):
    out = "Coins: "
    some = False
    if cp:
        some = True
        out = out + "CP: {},".format(cp)
    if sp:
        some = True
        out = out + "SP: {},".format(sp)
    if ep:
        some = True
        out = out + "EP: {},".format(ep)
    if gp:
        some = True
        out = out + "GP: {},".format(gp)
    if pp:
        some = True
        out = out + "PP: {},".format(pp)
    out = out[:len(out) - 1]
    if some:
        if p:
            logging.info("{}".format(out))
        return out
    else:
        return None


def print_gems(gems,total_value):
    text = "Gems: "
    for gem in gems:
        text = text + "{} (x{}),".format(gem['value'], gem['count'])
    text = text[:len(text) - 1]
    wrapper = textwrap.TextWrapper(initial_indent="", width=72, subsequent_indent="\t")
    text = wrapper.fill(text)
    logging.info("{}".format(text))
    logging.info("Total Gem Value: {}".format(total_value))
    return (text)


def print_jewelry(jewels,total_value):
    out = "Jewelry: "
    for jewel in jewels:
        out = out + "{} (x{}),".format(jewels['value'], jewels['count'])
    out = out[:len(out) - 1]
    wrapper = textwrap.TextWrapper(initial_indent="", width=72, subsequent_indent="\t")
    out = wrapper.fill(out)
    logging.info("Total Jewelry Value: {}".format(total_value))
    return (out)


def print_magic(magic):
    out = "Magic: "
    for item in magic:
        out = out + "{},".format(item['name'])
    out = out[:len(out) - 1]
    wrapper = textwrap.TextWrapper(initial_indent="", width=72, subsequent_indent="\t")
    out = wrapper.fill(out)
    return (out)


def get_any_magic(tables):
    pct = random.randrange(1, 100)
    if pct <= 20:
        item = get_potion(tables)
    elif pct <= 35:
        item = get_scroll(tables)
    elif pct <= 40:
        item = get_ring(tables)
    elif pct <= 45:
        item = get_rod_staff(tables)
    elif pct <= 60:
        item = get_misc_magic(tables)
    elif pct <= 75:
        item = get_armor_shield(tables)
    elif pct <= 86:
        item = get_sword(tables)
    else:
        item = get_misc_weapon(tables)
    return (item)


def get_magic(tables, x):
    list = []
    pct = random.randrange(1, 100)
    logging.info("Treasure type: {}".format(x))
    if x == 'A':
        if pct <= 30:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
    elif x == 'B':
        if pct <= 10:
            num = random.randrange(1, 3)
            if num == 1:
                list.append(get_armor_shield(tables))
            elif num == 2:
                list.append(get_sword(tables))
            else:
                list.append(get_misc_weapon(tables))
    elif x == 'C':
        if pct <= 10:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
    elif x == 'D':
        if pct <= 15:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_potion(tables))
    elif x == 'E':
        if pct <= 25:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_scroll(tables))
    elif x == 'F':
        if pct <= 30:
            for x in range(3):
                num = random.randrange(1, 6)
                if num == 1:
                    list.append(get_potion(tables))
                elif num == 2:
                    list.append(get_scroll(tables))
                elif num == 3:
                    list.append(get_ring(tables))
                elif num == 4:
                    list.append(get_rod_staff(tables))
                elif num == 5:
                    list.append(get_misc_magic(tables))
                elif num == 6:
                    list.append(get_armor_shield(tables))
            list.append(get_potion(tables))
            list.append(get_scroll(tables))
    elif x == 'G':
        if pct <= 35:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_scroll(tables))
    elif x == 'H':
        if pct <= 15:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_potion(tables))
            list.append(get_scroll(tables))
    elif x == 'I':
        if pct <= 15:
            list.append(get_any_magic(tables))
    elif x == 'S':
        if pct <= 40:
            num = random.randrange(2, 8)
            for x in range(num):
                list.append(get_potion(tables))
    elif x == 'T':
        if pct <= 50:
            num = random.randrange(1, 4)
            for x in range(num):
                list.append(get_scroll(tables))
    elif x == 'U':
        if pct <= 70:
            list.append(get_ring(tables))
            list.append(get_rod_staff(tables))
            list.append(get_misc_magic(tables))
            list.append(get_armor_shield(tables))
            list.append(get_sword(tables))
            list.append(get_misc_weapon(tables))
    elif x == 'V':
        if pct <= 85:
            logging.info("Got treasure type v")
            logging.info("\n")
            logging.info("Getting ring")
            logging.info("\n")
            list.append(get_ring(tables))
            logging.info("\n")
            logging.info("Getting ring")
            logging.info("\n")
            list.append(get_ring(tables))
            logging.info("\n")
            logging.info("Getting rod-staff-wand")
            logging.info("\n")
            list.append(get_rod_staff(tables))
            logging.info("\n")
            logging.info("Getting rod-staff-wand")
            logging.info("\n")
            list.append(get_rod_staff(tables))
            logging.info("\n")
            logging.info("Getting misc-magic")
            logging.info("\n")
            list.append(get_misc_magic(tables))
            logging.info("\n")
            logging.info("Getting misc-magic")
            logging.info("\n")
            list.append(get_misc_magic(tables))
            logging.info("\n")
            logging.info("Getting armor-shield")
            logging.info("\n")
            list.append(get_armor_shield(tables))
            logging.info("\n")
            logging.info("Getting armor-shield")
            logging.info("\n")
            list.append(get_armor_shield(tables))
            logging.info("\n")
            logging.info("Getting sword")
            logging.info("\n")
            list.append(get_sword(tables))
            logging.info("\n")
            logging.info("Getting sword")
            logging.info("\n")
            list.append(get_sword(tables))
            logging.info("\n")
            logging.info("Getting misc-weapon")
            logging.info("\n")
            list.append(get_misc_weapon(tables))
            logging.info("\n")
            logging.info("Getting misc-weapon")
            logging.info("\n")
            list.append(get_misc_weapon(tables))
            logging.info("\n")
    elif x == 'W':
        if pct <= 55:
            list.append(new_item("Map", 1000, 100))
    elif x == 'X':
        if pct <= 60:
            list.append(get_any_magic(tables))
            list.append(get_potion(tables))
    elif x == 'Z':
        if pct <= 50:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))

    return (list)


def find_quantity(x, lo, hi, pct, multiplier,platinum=False):
    if lo == 0 and hi == 0 and pct == 0:
        return(None)
    else:
        num = get_quantity(lo, hi, pct)
    if num:
        num = num * multiplier
    return(num)


def find_coin_quantity(x, lo, hi, pct, multiplier,platinum=False):
    if lo == 0 and hi == 0 and pct == 0:
        return(None)
    else:
        if x >= 'J' and x <= 'N':
            num = get_quantity(lo, hi, pct)
        elif platinum:
            num = get_quantity(lo*100, hi*100, pct)
        else:
            num = get_quantity(lo*1000, hi*1000, pct)
    if num:
        num = num * multiplier
    return(num)



def get_random_treasure(x, p=False, multiplier=1):
    tables = read_tables()
    loot = {}

    logging.info("Looking for treasure type {}".format(x))
    logging.info("passed in Multiplier of ".format(multiplier))

    logging.info("Copper lo, hi, pct = {} {} {}".format(copper[types.index(x)][0], \
        copper[types.index(x)][1], copper[types.index(x)][2]))

    logging.info("Silver lo, hi, pct = {} {} {}".format(silver[types.index(x)][0], \
        silver[types.index(x)][1], silver[types.index(x)][2]))

    logging.info("Electrum lo, hi, pct = {} {} {}".format(electrum[types.index(x)][0], \
        electrum[types.index(x)][1], electrum[types.index(x)][2]))

    logging.info("Gold lo, hi, pct = {} {} {}".format(gold[types.index(x)][0], \
        gold[types.index(x)][1], gold[types.index(x)][2]))
 
    logging.info("Platinum lo, hi, pct = {} {} {}".format(platinum[types.index(x)][0], \
        platinum[types.index(x)][1], platinum[types.index(x)][2]))

    logging.info("Gems lo, hi, pct = {} {} {}".format(gems[types.index(x)][0], \
        gems[types.index(x)][1], gems[types.index(x)][2]))

    cp = find_coin_quantity(x, copper[types.index(x)][0], copper[types.index(x)][1], \
        copper[types.index(x)][2],multiplier)

    sp = find_coin_quantity(x, silver[types.index(x)][0], silver[types.index(x)][1], \
        silver[types.index(x)][2],multiplier)

    ep = find_coin_quantity(x, electrum[types.index(x)][0], electrum[types.index(x)][1], \
        electrum[types.index(x)][2],multiplier)

    gp = find_coin_quantity(x, gold[types.index(x)][0], gold[types.index(x)][1], \
        gold[types.index(x)][2],multiplier)

    pp = find_coin_quantity(x, platinum[types.index(x)][0], platinum[types.index(x)][1], \
        platinum[types.index(x)][2],multiplier,platinum=True)

    gem = find_quantity(x, gems[types.index(x)][0], gems[types.index(x)][1], \
        gems[types.index(x)][2],multiplier)
    logging.info("Found {} gems".format(gem))

    jwl = find_quantity(x, jewelry[types.index(x)][0], jewelry[types.index(x)][1], \
        jewelry[types.index(x)][2],multiplier)
    logging.info("Found {} pieces of jewelry".format(jwl))

    if gem:
        loot['gems'], loot['gem_total'] = get_gems(gem)
    else:
        loot['gems'] = None
        loot['gem_total'] = None

    if jwl:
        loot['jewelry'], loot['jewelry_total'] = get_jewelry(jwl)
    else:
        loot['jewelry'] = None
        loot['jewelry_total'] = None

    loot['magic'] = get_magic(tables, x)

    out = print_coins(cp, sp, ep, gp, pp, p)
    if not out:
        out = ''
    else:
        out = out + " "

    if loot['gem_total']:
        out = out + print_gems(loot['gems'],loot['gem_total']) + " "

    if loot['jewelry_total']:
        out = out + print_jewelry(loot['jewelry'],loot['jewelry_total']) + " "

    if len(loot['magic']) > 0:
        out = out + print_magic(loot['magic'])

    return (out)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Random treasure generator")
    parser.add_argument("type", help="Treasure type (a-z)")
    parser.add_argument("-l", "--logging", help="Logging level", default="INFO")
    args = parser.parse_args()

    loglevel = args.logging
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logFile = "random_treasure.log"
    logging.basicConfig(filename=logFile, format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=numeric_level)
    logging.getLogger().addHandler(logging.StreamHandler())

    get_random_treasure(args.type, p=True)
