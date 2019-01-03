#!/usr/bin/python
import random
import logging
from interp import interp

def set_wand_subtype(item):
    if item['name'] == 'Earth & Stone':
        get_wand_earth_stone_type(item)

def get_wand_earth_stone_type(item):
    rand = random.randint(1,2)
    if rand == 1:
        item['name'] = item['name'] + " (basic)"
    else:
        item['xplo'] = item['xphi']
        item['gplo'] = item['gphi']
        item['name'] = item['name'] + " (with transmute)"

def set_rod_subtype(item):
    if item['name'] == 'Staff-Spear':
        get_staff_spear_type(item)
    if item['name'] == 'Staff of Swarming (CM)':
        get_staff_swarming_type(item)

def get_staff_swarming_type(item):
    rand = random.randint(1,50)
    item['cnt']=rand
    item['name']=item['name']+" ({})".format(rand)

def get_staff_spear_type(item):
    rand = random.randint(1,20)
    if rand <= 6:
        item['name'] = item['name'] + " +1"
        item['xplo'] = 1000
        item['gplo'] = 5000
    elif rand <= 10:
        item['name'] = item['name'] + " +2"
        item['xplo'] = 1500
        item['gplo'] = 7500
    elif rand <= 13:
        item['name'] = item['name'] + " +3"
        item['xplo'] = 2000
        item['gplo'] = 10000
    elif rand <= 16:
        item['name'] = item['name'] + " +4"
        item['xplo'] = 2500
        item['gplo'] = 15000
    elif rand <= 19:
        item['name'] = item['name'] + " +5"
        item['xplo'] = 3000
        item['gplo'] = 20000
    elif rand == 20:
        item['name'] = item['name'] + " +3 (d2-8)"
        item['xplo'] = 3500
        item['gplo'] = 25000
