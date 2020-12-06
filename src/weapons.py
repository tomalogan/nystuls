#!/usr/bin/python

import random
from interp import interp
from get_quantity import get_quantity


def set_weapon_subtype(item):
    if item['name'] == "Arrow +1":
        get_quantity(item, 2, 24)
    elif item['name'] == "Arrow +2":
        get_quantity(item, 2, 16)
    elif item['name'] == "Arrow +3":
        get_quantity(item, 2, 12)
    elif item['name'] == "Bolt +2":
        get_quantity(item, 2, 20)
    elif item['name'] == "Arrow +4":
        get_quantity(item, 2, 8)
    elif item['name'] == "Axe of Hurling":
        set_hurling_subtype(item)
    elif item['name'] == "Bolt +1":
        get_quantity(item, 6, 36)
    elif item['name'] == "Bolt +3":
        get_quantity(item, 3, 12)
    elif item['name'] == "+1 Sling Bullet":
        get_quantity(item, 5, 20)
    elif item['name'] == "+2 Sling Bullet":
        get_quantity(item, 3, 12)
    elif item['name'] == "+3 Sling Bullet":
        get_quantity(item, 2, 8)
    elif item['name'] == "Sling Bullet of Impact":
        get_quantity(item, 1, 4)
    elif item['name'] == "Dagger of Throwing":
        set_throwing_subtype(item)
    elif item['name'] == "Dart +1":
        get_quantity(item, 3, 12)
    elif item['name'] == "Dart +2":
        get_quantity(item, 2, 8)
    elif item['name'] == "Dart +3":
        get_quantity(item, 1, 4)
    elif item['name'] == "Hornblade":
        set_hornblade_subtype(item)
    elif item['name'] == "Knife Buckle":
        set_knife_subtype(item)
    elif item['name'] == "Quarterstaff Magic":
        set_staff_subtype(item)
    elif item['name'] == "Scimitar of Speed":
        set_scimitar_subtype(item)


def set_hurling_subtype(item):
    rand = random.randint(1, 20)
    if rand <= 5:
        item['name'] += " +1"
        item['xplo'] = 1500
        item['gplo'] = 15000
    elif rand <= 10:
        item['name'] += " +2"
        item['xplo'] = 3000
        item['gplo'] = 30000
    elif rand <= 15:
        item['name'] += " +3"
        item['xplo'] = 4500
        item['gplo'] = 45000
    elif rand <= 19:
        item['name'] += " +4"
        item['xplo'] = 6000
        item['gplo'] = 60000
    elif rand <= 20:
        item['name'] += " +5"
        item['xplo'] = 7500
        item['gplo'] = 75000


def set_throwing_subtype(item):
    rand = random.randint(1, 100)
    if rand <= 35:
        item['name'] += " +1"
        item['xplo'] = 250
        item['gplo'] = 2500
    elif rand <= 65:
        item['name'] += " +2"
        item['xplo'] = 350
        item['gplo'] = 3500
    elif rand <= 90:
        item['name'] += " +3"
        item['xplo'] = 450
        item['gplo'] = 4500
    elif rand <= 100:
        item['name'] += " +4"
        item['xplo'] = 550
        item['gplo'] = 5500


def set_hornblade_subtype(item):
    rand = random.randint(1, 100)
    if rand <= 20:
        item['name'] += " +1 knife"
        item['xplo'] = 500
        item['gplo'] = 1500
    elif rand <= 35:
        item['name'] += " +2 knife"
        item['xplo'] = 1000
        item['gplo'] = 3000
    elif rand <= 50:
        item['name'] += " +1 dagger"
        item['xplo'] = 750
        item['gplo'] = 2000
    elif rand <= 70:
        item['name'] += " +2 dagger"
        item['xplo'] = 1500
        item['gplo'] = 4000
    elif rand <= 90:
        item['name'] += " +2 scimitar"
        item['xplo'] = 2000
        item['gplo'] = 6000
    elif rand <= 100:
        item['name'] += " +3 scimitar"
        item['xplo'] = 3000
        item['gplo'] = 9000


def set_knife_subtype(item):
    rand = random.randint(1, 10)
    if rand <= 4:
        item['name'] += " +1"
        item['xplo'] = 100
        item['gplo'] = 1000
    elif rand <= 7:
        item['name'] += " +2"
        item['xplo'] = 200
        item['gplo'] = 2000
    elif rand <= 9:
        item['name'] += " +3"
        item['xplo'] = 300
        item['gplo'] = 3000
    elif rand <= 10:
        item['name'] += " +4"
        item['xplo'] = 400
        item['gplo'] = 4000


def set_staff_subtype(item):
    rand = random.randint(1, 20)
    if rand <= 5:
        item['name'] += " +1"
        item['xplo'] = 250
        item['gplo'] = 1500
    elif rand <= 9:
        item['name'] += " +2"
        item['xplo'] = 500
        item['gplo'] = 3000
    elif rand <= 13:
        item['name'] += " +3"
        item['xplo'] = 750
        item['gplo'] = 4500
    elif rand <= 17:
        item['name'] += " +4"
        item['xplo'] = 1500
        item['gplo'] = 10000
    elif rand <= 20:
        item['name'] += " +5"
        item['xplo'] = 3000
        item['gplo'] = 35000


def set_scimitar_subtype(item):
    rand = random.randint(1, 100)
    if rand <= 25:
        rand1 = random.randint(1, 100)
        if rand1 <= 50:
            item['name'] += " +1"
            item['xplo'] = 2500
            item['gplo'] = 9000
        elif rand1 <= 75:
            item['name'] += " +3"
            item['xplo'] = 3500
            item['gplo'] = 15000
        elif rand1 <= 90:
            item['name'] += " +4"
            item['xplo'] = 4000
            item['gplo'] = 18000
        elif rand1 <= 75:
            item['name'] += " +5"
            item['xplo'] = 4500
            item['gplo'] = 21000
    else:
        item['name'] += " +2"
        item['xplo'] = 3000
        item['gplo'] = 12000
