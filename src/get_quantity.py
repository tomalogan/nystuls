#!/usr/bin/python
import random
def get_quantity(item,lo,hi):
    rand = random.randint(lo,hi)
    item['cnt'] = rand
    item['gplo'] = int(item['gplo']) * (float(1+random.randint(1,50)/float(100)))


