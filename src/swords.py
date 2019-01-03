#!/usr/bin/python

import random

def set_sword_subtype(item):
    rand = random.randint(1,100)
    if rand <= 65:
         item['name'] = item['name'] + " (long)"
    elif rand <= 80:
         item['name'] = item['name'] + " (bastard)"
    elif rand <= 90:
         item['name'] = item['name'] + " (short)"
    elif rand <= 95:
         item['name'] = item['name'] + " (broad)"
    elif rand <= 100:
         item['name'] = item['name'] + " (two-handed)"

