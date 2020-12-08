#!/usr/local/bin/python3

import random

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




def get_monster_hp(monster, cnt, maxhp=True):
    hd = "{}".format(monster['HD'])
    plus = None
    minus = None

    if "HP" in hd:
        hp_list = [int(hd.split()[0])]
        return hp_list
    elif "/" in hd:
        t = hd.split("/")
        choice = random.randint(1, len(t))
        hd = t[choice]
    else:
        if "+" in hd:
            t = hd.split("+")
            hd = t[0]
            plus = t[1]
        elif "=" in hd:
            t = hd.split("=")
            hd = t[0]
            minus = t[1]
            plus = "0"
        else:
            plus = "0"

        if "-" in hd:
            lo = int(hd.split("-")[0])
            hi = int(hd.split("-")[1])
            hd = random.randint(lo, hi)

        if "-" in plus:
            lo = int(plus.split("-")[0])
            hi = int(plus.split("-")[1])
            plus = random.randint(lo, hi)

    hd = float(hd)
    if plus:
        plus = int(plus)
    else:
        plus = 0
    if minus:
        minus = int(minus)
    else:
        minus = 0

    hp_list = []
    if maxhp:
        hp = hd * 8 + plus - minus
        hp_list.append(int(hp))
    else:
        hp_list = []
        for x in range(cnt):
            hp = plus - minus
            for x in range(hd):
                hp = hp + random.randint(1, 8)
            if hp < 0:
                hp = 1
            hp_list.append(int(hp))

    monster['level'] = hd
    return hp_list

