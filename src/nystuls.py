#!/usr/bin/python

import os
import random
import copy
import logging
import argparse
import datetime
from utils import *


def Print_Inventory(inventory):
    hdrs = []
    msg = "------------------- Xaryx Xeg's Potion Em-pour-eum -------------------------------"
    hdrs.append(msg)
    msg = "------------------- Reynaulds Renowned Rings  ------------------------------------"
    hdrs.append(msg)
    msg = "------------------- Soapy Slick's Magic Sticks -----------------------------------"
    hdrs.append(msg)
    msg = "------------------- Maximo's Miscelleous Magics ----------------------------------"
    hdrs.append(msg)
    msg = "------------------- Sheldon's Armor and Shields ----------------------------------"
    hdrs.append(msg)
    msg = "------------------- Salazar's Fine Swords-----------------------------------------"
    hdrs.append(msg)
    msg = "------------------- Wild Winfred's Wonderful Weapons -----------------------------"
    hdrs.append(msg)

    last_type = None
    cnt = 0
    item_cnt = 0
    for x in xrange(len(inventory)):
        item = inventory[x]
        # Check for new header
        if item['type'] != last_type:
            if (last_type == 'Wands' or last_type == "Rods & Staves") and (
                    item['type'] == 'Wands' or item['type'] == "Rods & Staves"):
                pass
            else:
                logging.info("{}".format(hdrs[cnt]))
                last_type = item['type']
                cnt += 1

        # Print out the item
        if item['gplo'] > 0:
            if item['cnt'] > 1:
                logging.info(
                    "{:3d}: {:50}{:5d} GP  {:3d} count".format(x, item['name'], int(item['gplo']), int(item['cnt'])))
            elif item['cnt'] == 1:
                logging.info("{:3d}: {:50}{:5d} GP".format(x, item['name'], int(item['gplo'])))


def Set_Inventory():
    tables = read_tables()
    inventory = []

    # Read in the Potions
    for x in xrange(10):
        item = get_potion(tables)
        inventory.append(item)

    # Pad inventory
    rand = random.randint(5, 10)
    add_to_inventory(tables, inventory, "Healing", rand)
    rand = random.randint(2, 8)
    add_to_inventory(tables, inventory, "Extra-Healing", rand)
    pct = random.randint(1, 100)
    if pct <= 25:
        rand = random.randint(1, 4)
        add_to_inventory(tables, inventory, "Healing XX", rand)
    pct = random.randint(1, 100)
    if pct <= 10:
        rand = random.randint(1, 2)
        add_to_inventory(tables, inventory, "HEAL", rand)

    # Read in Rings
    for x in xrange(2):
        item = get_ring(tables)
        inventory.append(item)

    # Read in the Rod & Staves
    for x in xrange(4):
        item = get_rod_staff(tables)
        inventory.append(item)

    # Set miscellaneous magic
    for x in xrange(12):
        item = get_misc_magic(tables)
        inventory.append(item)

    # Set Armor and Shields
    for x in xrange(4):
        item = get_armor_shield(tables)
        inventory.append(item)

    # Set swords
    for x in xrange(6):
        item = get_sword(tables)
        inventory.append(item)

    # Set Miscellaneous Weapons
    for x in xrange(6):
        item = get_misc_weapon(tables)
        inventory.append(item)

    rand = random.randint(30, 50)
    add_to_inventory(tables, inventory, "Arrow +1", rand)
    pct = random.randint(1, 100)
    if pct <= 33:
        rand = random.randint(2, 20)
        add_to_inventory(tables, inventory, "Arrow +2", rand)
    pct = random.randint(1, 100)
    if pct <= 10:
        rand = random.randint(2, 12)
        add_to_inventory(tables, inventory, "Arrow +3", rand)
    if pct <= 2:
        rand = random.randint(2, 8)
        add_to_inventory(tables, inventory, "Arrow +4", rand)

    rand = random.randint(30, 50)
    add_to_inventory(tables, inventory, "Bolt +1", 50)
    pct = random.randint(1, 100)
    if pct <= 33:
        rand = random.randint(2, 20)
        add_to_inventory(tables, inventory, "Bolt +2", rand)
    pct = random.randint(1, 100)
    if pct <= 10:
        rand = random.randint(2, 12)
        add_to_inventory(tables, inventory, "Bolt +3", rand)

    return tables, inventory


def get_response():
    action = "A"
    while not type(action) is int:
        try:
            action = input("Action - (-1 exit,98 see cart,99 checkout): ")
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
    logging.info("----------------------------------------------------------------------------")
    logging.info("-----------------------  Cart Contents -------------------------------------")
    logging.info("----------------------------------------------------------------------------")
    logging.info("    {:50}{:5d} GP X {:3d} = {:5} GP".format("Entry Fee", 1000, 1, 1000))
    if len(cart['items']) > 0:
        for x in xrange(len(cart['items'])):
            # Print out the item
            item = cart['items'][x]
            if item is not None:
                gp = int(item['gplo'])
                cnt = int(item['cnt'])
                tot = gp * cnt
                logging.info("{:3} {:50}{:5d} GP X {:3d} = {:5} GP".format(x, item['name'], gp, cnt, tot))
    logging.info("----------------------------------------------------------------------------")
    logging.info("    Total Cost: {} gp".format(cart['total']))
    logging.info("----------------------------------------------------------------------------")
    any = raw_input("Hit enter key to continue (r to remove an item) ")
    if any == 'r':
        num = input("Which item to remove? ")
        if num >= 0 and num <= len(cart['items']):
            cart['total'] = int(cart['total']) - int(cart['items'][num]['gplo'])
            cart['items'][num] = None
            show_cart(cart)


def checkout(cart, name):
    total = 1000
    logging.info("-------- Purchase for {} ----------------------------------------------------".format(name))
    logging.info("{:50}{:5d} GP X {:3d} = {:5} GP".format("Entry Fee", 1000, 1, 1000))
    for x in xrange(len(cart['items'])):
        item = cart['items'][x]
        if item is not None:
            gp = int(item['gplo'])
            cnt = int(item['cnt'])
            tot = gp * cnt
            logging.info("{:50}{:5d} GP X {:3d} = {:5} GP".format(item['name'], gp, cnt, tot))
            total = total + int(item['gplo']) * int(item['cnt'])
    logging.info("---------------------------------------------------------------------------")
    logging.info(" Total Spent: {}".format(total))
    logging.info("---------------------------------------------------------------------------")
    resp = raw_input("Are you sure you are ready to leave? (y/n) ")
    if resp == "y":
        total = 1000
        date = datetime.datetime.now().strftime("%Y%m%d%H%M")
        f = open("{}.{}.cart.txt".format(name, date), "w")
        f.write("-------- Purchase for {} ----------------------------------------------------\n".format(name))
        f.write("{:50}{:5d} GP X {:3d} = {:5} GP\n".format("Entry Fee", 1000, 1, 1000))
        for x in xrange(len(cart['items'])):
            item = cart['items'][x]
            if item is not None:
                gp = int(item['gplo'])
                cnt = int(item['cnt'])
                tot = gp * cnt
                f.write("{:50}{:5d} GP X {:3d} = {:5} GP\n".format(item['name'], gp, cnt, tot))
                total = total + int(item['gplo']) * int(item['cnt'])
        f.write("---------------------------------------------------------------------------\n")
        f.write(" Total Spent: {}\n".format(total))
        f.write("---------------------------------------------------------------------------\n")
        f.close()
        exit(0)


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

    tables, inventory = Set_Inventory()
    name = raw_input("Please enter your name: ")

    cart = {}
    cart['total'] = 1000
    cart['items'] = []

    action = "99"
    while action != -1:
        Print_Inventory(inventory)
        action = get_response()
        if action == -1:
            logging.info("Exiting without checkout...")
            resp = raw_input("Are you sure? (y/n) ")
            if resp == "y":
                exit(0)
        elif action == 98:
            show_cart(cart)
        elif action == 99:
            logging.info("Exiting with checkout...")
            checkout(cart, name)
        elif action < len(inventory):
            add_item(inventory, action, cart)
        else:
            logging.info("Please enter a valid response!!!")
