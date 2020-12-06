#!/usr/local/bin/python3

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

    if hd < 1:
        if hd == 0.25:
            hd = "1/4"
        else:
            hd = "1/2"
    else:
        hd = int(hd)
    if plus > 0:
        hd = "{}+{}".format(hd, plus)
    elif minus > 0:
        hd = "{}-{}".format(hd, minus)
    monster['HD'] = hd
    return hp_list

