#!/usr/bin/python

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
        [0, 0, 0],  # X
        [2, 12, 70],  # Y
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


def get_coins(lo, hi, pct):
    roll = random.randint(1, 100)
    if roll <= pct:
        coins = random.randint(lo, hi)
    else:
        coins = None
    return (coins)


def consolidate(items):
    types = []
    cnts = []
    for x in xrange(len(items)):
        value = items[x]
        if not value in types:
            types.append(value)
            cnts.append(1)
        else:
            cnts[types.index(value)] = cnts[types.index(value)] + 1

    Z = sorted(zip(types, cnts))
    types = [x[0] for x in Z]
    cnts = [x[1] for x in Z]

    return (types, cnts)


base_value = [0.05, 0.25, 0.5, 1, 5, 10, 50, 100, 500, 1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]


def get_gems(cnt):
    total = 0
    list = []

    for x in xrange(cnt):
        pct = random.randint(1, 100)
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

        roll = random.randint(1, 10)
        done = False
        base = first_base
        while not done:
            if roll == 1:
                if base - first_base < 7:
                    base = base + 1
                    roll = random.randint(1, 8)
                else:
                    value = base_value[base]
                    done = True
            elif roll == 2:
                value = base_value[base] * 2
                done = True
            elif roll == 3:
                value = base_value[base] * (1 + random.randint(1, 6) * 10 / 100)
                done = True
            elif roll >= 4 and roll <= 8:
                value = base_value[base]
                done = True
            elif roll == 9:
                value = base_value[base] * (1 - random.randint(1, 4) * 10 / 100)
                done = True
            else:
                if first_base - base < 5:
                    base = base - 1
                    roll = random.randint(2, 10)
                else:
                    value = base_value[base]
                    done = True

        total = total + value
        list.append(value)

    list, cnts = consolidate(list)
    return (list, cnts, total)


def get_jewelry(cnt):
    list = []
    total = 0
    for x in xrange(cnt):

        # Set base class for this piece of jewelry
        roll = random.randint(1, 100)
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
            roll = random.randint(1, 10)
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
                value = random.randint(1, 10) * 100
            elif base == 1:
                value = random.randint(2, 12) * 100
            elif base == 2:
                value = random.randint(3, 18) * 100
            elif base == 3:
                value = random.randint(5, 30) * 100
            elif base == 4:
                value = random.randint(1, 6) * 1000
            elif base == 5:
                value = random.randint(2, 8) * 1000
            else:
                value = random.randint(2, 12) * 1000

        # Check for exceptional stones
        if base >= 4:
            roll = random.randint(1, 8)
            adder = 0
            if roll == 1:
                adder = 5000
                while adder < 640000:
                    roll = random.randint(1, 6)
                    if roll > 1:
                        break
                    else:
                        adder = adder * 2
            value = value + adder

        list.append(value)
        total = total + value

    list, cnts = consolidate(list)
    return (list, cnts, total)


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


def print_gems(s, p):
    out = "Gems: "
    for x in xrange(len(s['gem_list'])):
        out = out + "{} (x{}),".format(s['gem_list'][x], s['gem_cnts'][x])
    out = out[:len(out) - 1]
    wrapper = textwrap.TextWrapper(initial_indent="", width=72, subsequent_indent="\t")
    out = wrapper.fill(out)
    if p:
        logging.info("{}".format(out))
        logging.info("Total Gem Value: {}".format(s['gem_total']))
    return (out)


def print_jewelry(s, p):
    out = "Jewelry: "
    for x in xrange(len(s['jewelry_list'])):
        out = out + "{} (x{}),".format(s['jewelry_list'][x], s['jewelry_cnts'][x])
    out = out[:len(out) - 1]
    wrapper = textwrap.TextWrapper(initial_indent="", width=72, subsequent_indent="\t")
    out = wrapper.fill(out)
    if p:
        logging.info("{}".format(out))
        logging.info("Total Jewelry Value: {}".format(s['jewelry_total']))
    return (out)


def print_magic(magic, p):
    out = "Magic: "
    for item in magic:
        out = out + "{},".format(item['name'])
    out = out[:len(out) - 1]
    wrapper = textwrap.TextWrapper(initial_indent="", width=72, subsequent_indent="\t")
    out = wrapper.fill(out)
    if p:
        logging.info("{}".format(out))
    return (out)


def get_any_magic(tables):
    pct = random.randint(1, 100)
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
    pct = random.randint(1, 100)
    logging.debug("Treasure type: {}".format(x))
    if x == 'a':
        if pct <= 30:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
    elif x == 'b':
        if pct <= 10:
            num = random.randint(1, 3)
            if num == 1:
                list.append(get_armor_shield(tables))
            elif num == 2:
                list.append(get_sword(tables))
            else:
                list.append(get_misc_weapon(tables))
    elif x == 'c':
        if pct <= 10:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
    elif x == 'd':
        if pct <= 15:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_potion(tables))
    elif x == 'e':
        if pct <= 25:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_scroll(tables))
    elif x == 'f':
        if pct <= 30:
            for x in xrange(3):
                num = random.randint(1, 6)
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
    elif x == 'g':
        if pct <= 35:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_scroll(tables))
    elif x == 'h':
        if pct <= 15:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_potion(tables))
            list.append(get_scroll(tables))
    elif x == 'i':
        if pct <= 15:
            list.append(get_any_magic(tables))
    elif x == 's':
        if pct <= 40:
            num = random.randint(2, 8)
            for x in xrange(num):
                list.append(get_potion(tables))
    elif x == 't':
        if pct <= 50:
            num = random.randint(1, 4)
            for x in xrange(num):
                list.append(get_scroll(tables))
    elif x == 'u':
        if pct <= 70:
            list.append(get_ring(tables))
            list.append(get_rod_staff(tables))
            list.append(get_misc_magic(tables))
            list.append(get_armor_shield(tables))
            list.append(get_sword(tables))
            list.append(get_misc_weapon(tables))
    elif x == 'v':
        if pct <= 85:
            logging.debug("Got treasure type v")
            logging.debug("\n")
            logging.debug("Getting ring")
            logging.debug("\n")
            list.append(get_ring(tables))
            logging.debug("\n")
            logging.debug("Getting ring")
            logging.debug("\n")
            list.append(get_ring(tables))
            logging.debug("\n")
            logging.debug("Getting rod-staff-wand")
            logging.debug("\n")
            list.append(get_rod_staff(tables))
            logging.debug("\n")
            logging.debug("Getting rod-staff-wand")
            logging.debug("\n")
            list.append(get_rod_staff(tables))
            logging.debug("\n")
            logging.debug("Getting misc-magic")
            logging.debug("\n")
            list.append(get_misc_magic(tables))
            logging.debug("\n")
            logging.debug("Getting misc-magic")
            logging.debug("\n")
            list.append(get_misc_magic(tables))
            logging.debug("\n")
            logging.debug("Getting armor-shield")
            logging.debug("\n")
            list.append(get_armor_shield(tables))
            logging.debug("\n")
            logging.debug("Getting armor-shield")
            logging.debug("\n")
            list.append(get_armor_shield(tables))
            logging.debug("\n")
            logging.debug("Getting sword")
            logging.debug("\n")
            list.append(get_sword(tables))
            logging.debug("\n")
            logging.debug("Getting sword")
            logging.debug("\n")
            list.append(get_sword(tables))
            logging.debug("\n")
            logging.debug("Getting misc-weapon")
            logging.debug("\n")
            list.append(get_misc_weapon(tables))
            logging.debug("\n")
            logging.debug("Getting misc-weapon")
            logging.debug("\n")
            list.append(get_misc_weapon(tables))
            logging.debug("\n")
    elif x == 'w':
        if pct <= 55:
            list.append(new_item("Map", 1000, 100))
    elif x == 'x':
        if pct <= 60:
            list.append(get_any_magic(tables))
            list.append(get_potion(tables))
    elif x == 'z':
        if pct <= 50:
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))
            list.append(get_any_magic(tables))

    return (list)


def get_random_treasure(x, p=False):
    tables = read_tables()
    stuff = {}

    logging.debug("Looking for treasure type {}".format(x))

    cplo = copper[types.index(x)][0]
    cphi = copper[types.index(x)][1]
    cppct = copper[types.index(x)][2]
    logging.debug("Copper lo, hi, pct = {} {} {}".format(cplo, cphi, cppct))
    if x >= "j" and x <= "n":
        cp = get_coins(cplo, cphi, cppct)
    else:
        cp = get_coins(cplo * 1000, cphi * 1000, cppct)

    splo = silver[types.index(x)][0]
    sphi = silver[types.index(x)][1]
    sppct = silver[types.index(x)][2]
    logging.debug("Silver lo, hi, pct = {} {} {}".format(splo, sphi, sppct))
    if x >= "j" and x <= "n":
        sp = get_coins(splo, sphi, sppct)
    else:
        sp = get_coins(splo * 1000, sphi * 1000, sppct)

    eplo = electrum[types.index(x)][0]
    ephi = electrum[types.index(x)][1]
    eppct = electrum[types.index(x)][2]
    logging.debug("Electrum lo, hi, pct = {} {} {}".format(eplo, ephi, eppct))
    if x >= "j" and x <= "n":
        ep = get_coins(eplo, ephi, eppct)
    else:
        ep = get_coins(eplo * 1000, ephi * 1000, eppct)

    gplo = gold[types.index(x)][0]
    gphi = gold[types.index(x)][1]
    gppct = gold[types.index(x)][2]
    logging.debug("Gold lo, hi, pct = {} {} {}".format(gplo, gphi, gppct))
    if x >= "j" and x <= "n":
        gp = get_coins(gplo, gphi, gppct)
    else:
        gp = get_coins(gplo * 1000, gphi * 1000, gppct)

    pplo = platinum[types.index(x)][0]
    pphi = platinum[types.index(x)][1]
    pppct = platinum[types.index(x)][2]
    logging.debug("Platinum lo, hi, pct = {} {} {}".format(pplo, pphi, pppct))
    if x >= "j" and x <= "n":
        pp = get_coins(pplo, pphi, pppct)
    else:
        pp = get_coins(pplo * 100, pphi * 100, pppct)

    gemlo = gems[types.index(x)][0]
    gemhi = gems[types.index(x)][1]
    gempct = gems[types.index(x)][2]
    logging.debug("Gems lo, hi, pct = {} {} {}".format(gemlo, gemhi, gempct))
    gem = get_coins(gemlo, gemhi, gempct)

    jwllo = jewelry[types.index(x)][0]
    jwlhi = jewelry[types.index(x)][1]
    jwlpct = jewelry[types.index(x)][2]
    logging.debug("Jewelry lo, hi, pct = {} {} {}".format(jwllo, jwlhi, jwlpct))
    jwl = get_coins(jwllo, jwlhi, jwlpct)

    if gem:
        stuff['gem_list'], stuff['gem_cnts'], stuff['gem_total'] = get_gems(gem)
    else:
        stuff['gem_cnts'] = None
        stuff['gem_list'] = None
        stuff['gem_total'] = None

    if jwl:
        stuff['jewelry_list'], stuff['jewelry_cnts'], stuff['jewelry_total'] = get_jewelry(jwl)
    else:
        stuff['jewelry_cnts'] = 0
        stuff['jewelry_list'] = None
        stuff['jewelry_total'] = None

    stuff['magic'] = get_magic(tables, x)

    out = print_coins(cp, sp, ep, gp, pp, p)
    if not out:
        out = ''
    else:
        out = out + " "

    if stuff['gem_cnts']:
        out = out + print_gems(stuff, p) + " "

    if stuff['jewelry_cnts']:
        out = out + print_jewelry(stuff, p) + " "

    if len(stuff['magic']) > 0:
        out = out + print_magic(stuff['magic'], p)

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
