#!/usr/bin/python

import random
import os
import logging
import copy
from potions import set_potion_subtype
from rings import set_ring_subtype
from swords import set_sword_subtype
from sticks import set_wand_subtype
from sticks import set_rod_subtype
from misc_magic import set_misc_subtype
from weapons import set_weapon_subtype
from scrolls import set_scroll_subtype


def get_character_level(c, name):
    classes = c['classes']
    logging.debug("Classes are {}; Looking for {}".format(classes, name))
    cnt = 0
    for item in classes:
        if item == name:
            level = c['class_lvl'][cnt]
        cnt = cnt + 1
    return level


def new_item(name, xp, gp, cnt=1):
    item = {}
    item['name'] = name
    item['gplo'] = gp
    item['xplo'] = xp
    item['cnt'] = cnt
    return (item)


def get_potion(tables):
    sources = ["IIIA", "IIIA2"]
    pcts = [65]
    item = get_item_from_list(tables, sources, pcts)
    if not ("Oil" in item['name']) and not ("Philter" in item['name']):
        item['name'] = "Potion of " + item['name']
    item['gplo'] = int(item['gplo']) * (float(1 + random.randint(1, 50) / float(100)))
    return (item)


def get_scroll(tables):
    sources = ["IIIB", "IIIB2"]
    pcts = [85]
    item = get_item_from_list(tables, sources, pcts)
    item['name'] = "Scroll of " + item['name']
    item['gplo'] = int(item['gplo']) * (float(1 + random.randint(1, 50) / float(100)))
    return (item)


def get_ring(tables):
    sources = ["IIIC", "IIIC2"]
    pcts = [67]
    item = get_item_from_list(tables, sources, pcts)
    item['name'] = "Ring of " + item['name']
    item['gplo'] = int(item['gplo']) * (float(1 + random.randint(1, 50) / float(100)))
    return (item)


def get_rod_staff(tables, classtype=None):
    sources = ["IIID", "IIID2"]
    pcts = [40]
    while 1:
        item = get_item_from_list(tables, sources, pcts)
        i = item['name']
        if not ("Staff" in i) and not ("Rod" in i) and not ("Wand" in i):
            item['name'] = "Wand of {}".format(item['name'])
        item['gplo'] = int(item['gplo']) * (float(1 + random.randint(1, 50) / float(100)))
        if classtype == "Cleric":
            if (not "(M)" in item['name'] and not "(F)" in item['name'] and
                    not "(D)" in item['name'] and not "(T)" in item['name'] and
                    not "(FM)" in item['name'] and not "(FMT)" in item['name']):
                return item
        else:
            return item


def get_misc_magic(tables, gplimit=1000001, classtype=None):
    gplimit = gplimit * 1.3
    sources = ["IIIE1", "IIIE2", "IIIE3", "IIIE4", "IIIE5", "IIIE6", "IIIE7"]
    pcts = [14, 28, 42, 56, 70, 85, 100]
    while 1:
        item = get_item_from_list(tables, sources, pcts)
        item['gplo'] = int(item['gplo']) * (float(1 + random.randint(1, 50) / float(100)))
        logging.debug("Got item named {} for classtype {}".format(item['name'], classtype))
        if classtype == "Fighter":
            if ((not "(M)" in item['name'] and not "(C)" in item['name'] and
                 not "(D)" in item['name'] and not "(T)" in item['name'] and
                 not "(CM)" in item['name'] and not "(CMT)" in item['name']) and
                    item['gplo'] < gplimit):
                logging.debug("Item accepted: {}".format(item['name']))
                return (item)
        elif classtype == "FM":
            if ((not "(C)" in item['name'] and not "(D)" in item['name'] and not "(T)" in item['name']) and
                    item['gplo'] < gplimit):
                return (item)
        elif classtype == "Cleric":
            if ((not "(M)" in item['name'] and not "(F)" in item['name'] and
                 not "(D)" in item['name'] and not "(T)" in item['name'] and
                 not "(FM)" in item['name'] and not "(FMT)" in item['name']) and
                    item['gplo'] < gplimit):
                return (item)
        elif classtype == "Magic-User":
            if ((not "(C)" in item['name'] and not "(F)" in item['name'] and
                 not "(D)" in item['name'] and not "(T)" in item['name'] and
                 not "(CF)" in item['name'] and not "(CFT)" in item['name']) and
                    item['gplo'] < gplimit):
                return (item)
        else:
            if (item['gplo'] < gplimit):
                return (item)


def get_armor_shield(tables):
    sources = ["IIIF", "IIIF2"]
    pcts = [50]
    item = get_item_from_list(tables, sources, pcts)
    item['gplo'] = int(item['gplo']) * (float(1 + random.randint(1, 50) / float(100)))
    return (item)


def get_sword(tables):
    sources = ["IIIG", "IIIG2"]
    pcts = [95]
    item = get_item_from_list(tables, sources, pcts)
    item['gplo'] = int(item['gplo']) * (float(1 + random.randint(1, 50) / float(100)))
    return (item)


def get_misc_weapon(tables):
    sources = ["IIIH", "IIIH2"]
    pcts = [50]
    item = get_item_from_list(tables, sources, pcts)
    item['gplo'] = int(item['gplo']) * (float(1 + random.randint(1, 50) / float(100)))
    return (item)


def get_item_from_list(tables, names, pcts):
    cnt = len(tables)
    rand = random.randint(1, 100)
    rand1 = random.randint(1, 100)
    logging.debug("Rolled {} for table name".format(rand))
    logging.debug("Rolled {} for item".format(rand1))
    found = None

    cnt = 0
    for val in pcts:
        if rand <= val:
            break
        cnt = cnt + 1
    name = names[cnt]
    logging.debug("Looking for table name {}".format(name))

    cnt = len(tables)
    for x in range(cnt):
        logging.debug("Table name {}".format(tables[x]['name']))
        if tables[x]['name'] == name:
            mytype = tables[x]['type']
            logging.debug("Found table {}".format(tables[x]['name']))
            for item in tables[x]['data']:
                if int(item['pctlo']) <= rand1 and int(item['pcthi']) >= rand1:
                    found = copy.deepcopy(item)

    if not found:
        logging.info("Couldn't find any {}!".format(mytype.lower()))
    else:
        if found['subtype'] == 'set':
            if mytype == "Potions":
                set_potion_subtype(found)
            elif mytype == "Scrolls":
                set_scroll_subtype(found)
            elif mytype == "Rings":
                set_ring_subtype(found)
            elif mytype == "Rods & Staves":
                set_rod_subtype(found)
            elif mytype == "Wands":
                set_wand_subtype(found)
            elif mytype == "Swords":
                set_sword_subtype(found)
            elif mytype == "Miscellaneous Magic":
                set_misc_subtype(found)
            elif mytype == "Miscellaneous Weapons":
                set_weapon_subtype(found)

    return (found)


def read_tables():
    etcFile = "data.txt"
    etcPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'etc'))
    etcFile = os.path.join(etcPath, etcFile)

    f = open(etcFile, "r")
    tables = []
    cnt = -1
    for line in f:
        t = line.strip().split(",")
        if len(t) == 2:
            # We have a new table
            logging.debug("Found new table")
            table = {}
            table['name'] = t[0]
            table['type'] = t[1]
            table_type = table['type']
            table['data'] = []
            tables.append(table)
            cnt = cnt + 1
            logging.debug("Found new table of type {} named {}".format(table['type'], table['name']))
        elif len(t) == 5:
            # We have a regular item to parse
            item = {}
            item['pctlo'] = int(t[0])
            item['pcthi'] = int(t[1])
            item['name'] = t[2]
            item['xplo'] = int(t[3])
            item['gplo'] = int(t[4])
            item['subtype'] = None
            item['type'] = table_type
            item['cnt'] = 1
            tables[cnt]['data'].append(item)
            logging.debug("Found item {}".format(item))
        elif len(t) >= 6:
            # special handling required
            item = {}
            item['pctlo'] = int(t[0])
            item['pcthi'] = int(t[1])
            item['name'] = t[2]
            item['xplo'] = int(t[3])
            item['gplo'] = int(t[4])
            item['type'] = table_type
            item['cnt'] = 1
            if t[5] == "*":
                item['subtype'] = 'set'
                if len(t) > 6:
                    item['xphi'] = int(t[6])
                    item['gphi'] = int(t[7])
            logging.debug("Found item {}".format(item))
            tables[cnt]['data'].append(item)

    logging.debug("Found {} tables".format(cnt + 1))
    return (tables)


def add_to_inventory(tables, inventory, target, cnt):
    # First, check if it is in our inventory already
    found = False
    for item  in inventory:
        if target == item['name']:
            iten['cnt'] += cnt
            found = True

    # If its not there, add it
    new_item = None
    if not found:
        for table in tables:
            for item in table['data']:
                if target == item['name']:
                    new_item = copy.deepcopy(item)
        if new_item:
            new_item['cnt'] = cnt
            new_item['gplo'] = int(new_item['gplo']) * (float(1 + random.randint(1, 50) / float(100)))
            #            if new_item['type'] == 'Potions':
            #                new_item['name']=new_item['name'] + ", Potion"
            inventory.append(new_item)
        else:
            logging.error("Unable to find target item {}".format(target))
