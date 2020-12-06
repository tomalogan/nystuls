#!/usr/bin/python
import random
import logging
from interp import interp


def set_ring_subtype(item, rand=None):
    if not rand:
        rand = random.randint(1, 100)
    item['xplo'] = interp(item['xplo'], item['xphi'], rand, 100)
    item['gplo'] = interp(item['gplo'], item['gphi'], rand, 100)
    if rand <= 70:
        item['name'] = item['name'] + " +1"
    elif rand <= 82:
        item['name'] = item['name'] + " +2"
    elif rand <= 83:
        item['name'] = item['name'] + " +2 (5' radius)"
    elif rand <= 90:
        item['name'] = item['name'] + " +3"
    elif rand <= 91:
        item['name'] = item['name'] + " +3 (5' radius)"
    elif rand <= 97:
        item['name'] = item['name'] + " +4 AC, +2 saves"
    else:
        item['name'] = item['name'] + " +6 AC, +1 saves"
