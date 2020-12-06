#!/usr/bin/python

import random


def set_scroll_subtype(item):
    num = int(item['name'][0])
    low_level_range = item['xplo']
    high_level_range = item['gplo']
    pct = random.randint(1, 100)
    if pct <= 70:
        pct2 = random.randint(1, 100)
        if pct2 <= 10:
            classtype = "Illusionist"
        else:
            classtype = "Magic-User"
    else:
        pct2 = random.randint(1, 100)
        if pct2 <= 25:
            classtype = "Druid"
        else:
            classtype = "Cleric"

    if classtype == "Druid" or classtype == "Cleric":
        if high_level_range == 8:
            high_level_range == 6
        if high_level_range == 9:
            high_level_range == 7

    item['name'] = item['name'] + " ({}) (".format(classtype)
    out = ""
    level_list = []
    for x in xrange(num):
        level_list.append(random.randint(low_level_range, high_level_range))
    level_list = sorted(level_list)
    for x in xrange(num):
        out = out + "{},".format(level_list[x])
    item['name'] = item['name'] + "{})".format(out[:len(out) - 1])
