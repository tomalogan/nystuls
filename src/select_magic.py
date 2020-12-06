#!/usr/bin/python

import os
import random
import copy
import logging
import argparse
import datetime
from utils import *


def get_response():
    action = "A"
    while not type(action) is int:
        try:
            action = input("Action: ")
        except:
            logging.info("Please enter a valid integer.")
    return (action)


def add_item(inventory, item, cart):
    if (inventory[item]['cnt'] > 0):
        new_item = copy.deepcopy(inventory[item])
        if new_item['cnt'] > 1:
            try:
                cnt = input("Number to purchase? ")
            except:
                logging.info("Please enter a valid integer.")
                cnt = input("Number to purchase? ")
        else:
            cnt = 1
        if (cnt <= inventory[item]['cnt']):
            new_item['cnt'] = cnt
            cart['items'].append(new_item)
            cart['total'] = cart['total'] + int(new_item['gplo']) * int(new_item['cnt'])
            inventory[item]['cnt'] -= cnt
            logging.info("Added {} to cart".format(new_item['name']))
        else:
            logging.info("Invalid entry")


def show_cart(cart):
    total = 0
    logging.info("----------------------------------------------------------------------------")
    logging.info("-----------------------  Cart Contents -------------------------------------")
    logging.info("----------------------------------------------------------------------------")
    if len(cart['items']) > 0:
        for x in xrange(len(cart['items'])):
            # Print out the item
            item = cart['items'][x]
            if item is not None:
                gp = int(item['gplo'])
                cnt = int(item['cnt'])
                tot = gp * cnt
                logging.info("{:3} {:50}{:5d} GP X {:3d} = {:5} GP".format(x, item['name'], gp, cnt, tot))
                total = total + tot
    logging.info("----------------------------------------------------------------------------")
    logging.info("    Total Cost: {} gp".format(total))
    logging.info("----------------------------------------------------------------------------")
    any = raw_input("Hit enter key to continue (r to remove an item) ")
    if any == 'r':
        num = input("Which item to remove? ")
        if num >= 0 and num <= len(cart['items']):
            cart['total'] = int(cart['total']) - int(cart['items'][num]['gplo'])
            cart['items'][num] = None
            show_cart(cart)


def checkout(cart, name):
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    total = 0
    f = open("{}.{}.cart.txt".format(name, date), "w")
    f.write("-------- Purchase for {} ----------------------------------------------------\n".format(name))
    logging.info("-------- Purchase for {} ----------------------------------------------------".format(name))
    for x in xrange(len(cart['items'])):
        item = cart['items'][x]
        if item is not None:
            gp = int(item['gplo'])
            cnt = int(item['cnt'])
            tot = gp * cnt
            f.write("{:50}{:5d} GP X {:3d} = {:5} GP\n".format(item['name'], gp, cnt, tot))
            logging.info("{:50}{:5d} GP X {:3d} = {:5} GP".format(item['name'], gp, cnt, tot))
            total = total + int(item['gplo']) * int(item['cnt'])
    logging.info("---------------------------------------------------------------------------")
    logging.info(" Total Spent: {}".format(total))
    logging.info("---------------------------------------------------------------------------")
    f.write("---------------------------------------------------------------------------\n")
    f.write(" Total Spent: {}\n".format(total))
    f.write("---------------------------------------------------------------------------\n")
    f.close()
    exit(0)


def Print_Choices():
    logging.info("--------------------------------------------------------------------")
    logging.info("   (0) Potion")
    logging.info("   (1) Scroll")
    logging.info("   (2) Ring")
    logging.info("   (3) Rod/Staff/Wand")
    logging.info("   (4) Misc Magic")
    logging.info("   (5) Armor")
    logging.info("   (6) Sword")
    logging.info("   (7) Misc Weapon")
    logging.info("   (8) Show Cart")
    logging.info("   (9) Exit")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Ye Olde Magick Shoppe of Nystul")
    parser.add_argument("-l", "--logging", help="Logging level", default="INFO")
    args = parser.parse_args()

    loglevel = args.logging
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logFile = "nystuls.log"
    logging.basicConfig(filename=logFile, format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=numeric_level)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info("Starting run")

    tables = read_tables()
    name = raw_input("Please enter NPC name: ")

    cart = {}
    cart['total'] = 0
    cart['items'] = []

    action = "99"
    while action != -1:
        Print_Choices()
        action = get_response()
        if action == -1:
            logging.info("Exiting without checkout...")
            resp = raw_input("Are you sure? (y/n) ")
            if resp == "y":
                exit(0)
        elif action == 0:  # Potion
            cart['items'].append(get_potion(tables))
        elif action == 1:  # Scroll
            cart['items'].append(get_scroll(tables))
        elif action == 2:  # Ring 
            cart['items'].append(get_ring(tables))
        elif action == 3:  # Rod/Staff/Wand
            cart['items'].append(get_rod_staff(tables))
        elif action == 4:  # Misc Magic
            cart['items'].append(get_misc_magic(tables))
        elif action == 5:  # Armor
            cart['items'].append(get_armor_shield(tables))
        elif action == 6:  # Sword 
            cart['items'].append(get_sword(tables))
        elif action == 7:  # Misc Weapon
            cart['items'].append(get_misc_weapon(tables))
        elif action == 8:
            show_cart(cart)
        elif action == 9:
            logging.info("Exiting with checkout...")
            resp = raw_input("Are you sure you are ready to leave? (y/n) ")
            if resp == "y":
                checkout(cart, name)
        else:
            logging.info("Please enter a valid response!!!")
