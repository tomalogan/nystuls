#!/usr/bin/python

import logging
from utils import *
from rings import set_ring_subtype
from misc_magic import get_misc_cloak_type


def read_equipment(fi):
    f = open(fi, "r")
    table = []
    pctlo = 0
    for line in f:
        t = line.strip().split(",")
        item = {}
        item['pctlo'] = int(pctlo)
        item['pcthi'] = int(t[0])
        pctlo = item['pcthi'] + 1
        item['name'] = t[1]
        #        logging.debug("added item {}".format(item))
        table.append(item)
    table[-1]['pcthi'] = 10000
    return (table)


def get_fighter_sword(c):
    etcFile = "magic_swords.txt"
    etcPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'etc'))
    etcFile = os.path.join(etcPath, etcFile)

    swords = read_equipment(etcFile)
    level = int(get_character_level(c, "Fighter"))
    pct1 = random.randint(1, 100)
    pct2 = random.randint(1, 100) + 11 * (level - 3)
    if pct2 > 200:
        pct2 = random.randint(100, 200)
    got_magic = False
    if level < 4:
        if pct1 < level * 25:
            got_magic = True
    else:
        got_magic = True

    if got_magic:
        logging.debug("Got magic sword! pct2 is {}".format(pct2))
        for item in swords:
            if item['pctlo'] <= pct2 and pct2 <= item['pcthi']:
                new = copy.deepcopy(item)
                new['cnt'] = 1
                set_sword_subtype(new)
                c['weapons'].append(new)
    else:
        item = new_item("Sword", 1, 10)
        set_sword_subtype(item)
        c['weapons'].append(item)


def get_fighter_armor(c, class_type="Fighter"):
    etcFile = "magic_armor.txt"
    etcPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'etc'))
    etcFile = os.path.join(etcPath, etcFile)
    magic_armor = read_equipment(etcFile)
    level = int(get_character_level(c, class_type))
    pct1 = random.randint(1, 100)
    pct2 = random.randint(1, 100) + 11 * (level - 3)
    got_magic = False
    if level < 4:
        if pct1 < level * 25:
            got_magic = True
    else:
        got_magic = True

    if got_magic:
        logging.debug("Got magic armor! pct2 is {}".format(pct2))
        for item in magic_armor:
            if item['pctlo'] <= pct2 and pct2 <= item['pcthi']:
                c['armor'] = item['name']
        logging.debug("Selected armor is {}".format(c['armor']))
    else:
        if level == 1:
            c['armor'] = "Scale Mail"
        elif level == 2:
            c['armor'] = "Plate Mail"
        elif level == 3:
            c['armor'] = "Plate Armor; Field"
        else:
            c['armor'] = "Plate Armor; Full"


def get_fighter_shield(c, class_type="Fighter"):
    level = int(get_character_level(c, class_type))
    pct1 = random.randint(1, 100)
    pct2 = random.randint(1, 100) + 11 * (level - 3)
    got_magic = False
    if level < 4:
        if pct1 < level * 25:
            got_magic = True
    else:
        got_magic = True

    if got_magic:
        plus = int(level / 4 + 1)
        pct_extra = (float(level % 4) / 4.0) * 100.0
        if pct2 < pct_extra:
            plus = plus + 1
        if plus > 5:
            plus = 5
        c['shield'] = "Shield +{}".format(plus)
    else:
        c['shield'] = "Shield"


arrow_table = [[20, 0, 0, 0], [30, 0, 0, 0], [50, 20, 0, 0], [70, 30, 0, 0], [90, 50, 0, 0],
               [90, 70, 30, 0], [90, 70, 40, 0], [90, 70, 50, 30], [100, 70, 50, 40]]


def get_arrows(tables, c):
    level = int(get_character_level(c, "Fighter")) - 1
    total_left = 40
    plus = []
    if level > 8:
        level = 8
    plus.append(arrow_table[level][0])
    plus.append(arrow_table[level][1])
    plus.append(arrow_table[level][2])
    plus.append(arrow_table[level][3])
    logging.debug("plus table is {}".format(plus))
    pct = random.randint(1, 100)
    if pct < plus[3] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[3]))
        add_to_inventory(tables, c['weapons'], "Arrow +4", random.randint(4, 14))
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[2] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[2]))
        add_to_inventory(tables, c['weapons'], "Arrow +3", random.randint(4, 14))
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[1] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[1]))
        add_to_inventory(tables, c['weapons'], "Arrow +2", random.randint(4, 14))
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[0]:
        logging.debug("got percent of {} < {}".format(pct, plus[0]))
        add_to_inventory(tables, c['weapons'], "Arrow +1", random.randint(4, 14))
        total_left = total_left - c['weapons'][-1]['cnt']
    if total_left > 0:
        c['weapons'].append(new_item("Arrow", 1, 10, cnt=random.randint(1, total_left)))


def equip_Fighter(tables, c):
    level = int(get_character_level(c, "Fighter"))
    logging.debug("Found fighter level of {}".format(level))

    get_fighter_armor(c)
    get_fighter_shield(c)
    get_fighter_sword(c)

    pct = random.randint(1, 100)
    if pct > 50:
        if level < 6:
            c['weapons'].append(new_item("Bow", 10, 100))
            c['weapons'].append(new_item("Arrow", 1, 10, cnt=random.randint(14, 20)))
        else:
            add_to_inventory(tables, c['weapons'], "Bow +1", 1)
            get_arrows(tables, c)

    if level <= 4:
        pct = random.randint(1, 100)
        if (pct > 50):
            add_to_inventory(tables, c['stuff'], "Healing", random.randint(1, 2))
        pct = random.randint(1, 100)
        if (pct > 95):
            c['stuff'].append(get_potion(tables))
    elif level <= 6:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 75):
            c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 95):
            c['stuff'].append(get_misc_magic(tables, gplimit=10000, classtype="Fighter"))
    elif level <= 9:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "Healing XX", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 50):
            c['stuff'].append(get_potion(tables))
            c['stuff'].append(get_misc_magic(tables, gplimit=20000, classtype="Fighter"))
        if (pct > 85):
            c['stuff'].append(get_misc_magic(tables, gplimit=40000, classtype="Fighter"))
    else:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "Healing XX", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "HEAL", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_misc_magic(tables, classtype="Fighter"))
        c['stuff'].append(get_misc_magic(tables, classtype="Fighter"))
        c['stuff'].append(get_misc_magic(tables, classtype="Fighter"))


def get_cleric_weapon(c):
    etcFile = "magic_maces.txt"
    etcPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'etc'))
    etcFile = os.path.join(etcPath, etcFile)
    weapons = read_equipment(etcFile)
    level = int(get_character_level(c, "Cleric"))
    pct1 = random.randint(1, 100)
    pct2 = random.randint(1, 100) + 11 * (level - 3)
    if pct2 > 200:
        pct2 = random.randint(100, 200)
    got_magic = False
    if level < 4:
        if pct1 < level * 25:
            got_magic = True
    else:
        got_magic = True

    if got_magic:
        logging.debug("Got magic mace! pct2 is {}".format(pct2))
        for item in weapons:
            if item['pctlo'] <= pct2 and pct2 <= item['pcthi']:
                new = copy.deepcopy(item)
                new['cnt'] = 1
                c['weapons'].append(new)
    else:
        pct = random.randint(1, 100)
        if pct <= 25:
            c['weapons'].append(new_item("Mace", 1, 10))
        elif pct <= 50:
            c['weapons'].append(new_item("Flail", 1, 10))
        if pct <= 75:
            c['weapons'].append(new_item("Hammer", 1, 10))
        if pct <= 100:
            c['weapons'].append(new_item("Staff", 1, 10))


def equip_Cleric(tables, c):
    level = int(get_character_level(c, "Cleric"))
    logging.debug("Found cleric level of {}".format(level))

    get_fighter_armor(c, class_type="Cleric")
    get_fighter_shield(c, class_type="Cleric")
    get_cleric_weapon(c)
    get_pro_ring(tables, c, classtype="Cleric")

    if level <= 4:
        pct = random.randint(1, 100)
        if (pct > 50):
            add_to_inventory(tables, c['stuff'], "Healing", random.randint(1, 2))
        pct = random.randint(1, 100)
        if (pct > 95):
            c['stuff'].append(get_potion(tables))
    elif level <= 6:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 75):
            c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 95):
            c['stuff'].append(get_misc_magic(tables, gplimit=10000, classtype="Cleric"))
    elif level <= 9:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "Healing XX", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 50):
            c['stuff'].append(get_potion(tables))
            c['stuff'].append(get_misc_magic(tables, gplimit=20000, classtype="Cleric"))
        if (pct > 85):
            c['stuff'].append(get_misc_magic(tables, gplimit=40000, classtype="Cleric"))
    else:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "Healing XX", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "HEAL", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_misc_magic(tables, classtype="Cleric"))
        c['stuff'].append(get_misc_magic(tables, classtype="Cleric"))
        c['stuff'].append(get_misc_magic(tables, classtype="Cleric"))
        pct = random.randint(1, 100)
        if pct > 75:
            c['stuff'].append(get_rod_staff(tables, classtype="Cleric"))


bracer_chance = [0, 10, 30, 70, 100, 100, 100, 100, 100, 100, 100]
bracer_range = [[10, 10], [7, 8], [6, 8], [6, 8], [5, 7], [5, 7], [4, 6], [4, 6], [2, 6], [2, 6], [2, 4]]


def get_mage_protection(c):
    level = int(get_character_level(c, "Magic-User"))
    level = level - 1
    if level > 11:
        level = 11
    pct1 = random.randint(1, 100)
    got_bracers = False
    logging.debug("pct1 is {}; bracer_chance is {}".format(pct1, bracer_chance[level]))
    if pct1 < bracer_chance[level]:
        got_bracers = True

    if got_bracers:
        pct2 = random.randint(1, 100)
        logging.debug("Got magic bracers! pct2 is {}".format(pct2))
        ac = random.randint(bracer_range[level][0], bracer_range[level][1])
        c['armor'] = "Bracers of Defense AC {}".format(ac)


def get_pro_ring(tables, c, classtype="Magic-User"):
    level = int(get_character_level(c, classtype))
    pct1 = random.randint(1, 100)
    success = False
    if level < 5:
        if pct1 < (level - 1) * 25:
            success = True
    else:
        success = True
    if success:
        pct2 = random.randint(1, 70) + level * 3
        if pct2 > 100:
            pct2 = 100
        logging.debug("Got magic ring! pct2 is {}".format(pct2))
        add_to_inventory(tables, c['stuff'], "Protection", 1)
        set_ring_subtype(c['stuff'][-1], rand=pct2)
        c['stuff'][-1]['name'] = "Ring of " + c['stuff'][-1]['name']


def get_pro_cloak(tables, c, classtype="Magic-User"):
    level = int(get_character_level(c, classtype))
    pct1 = random.randint(1, 100)
    success = False
    if level < 5:
        if pct1 < (level - 1) * 25:
            success = True
    else:
        success = True
    if success:
        pct2 = random.randint(1, 50) + level * 6
        if pct2 > 100:
            pct2 = 100
        logging.debug("Got magic cloak! pct2 is {}".format(pct2))
        add_to_inventory(tables, c['stuff'], "Cloak of Protection", 1)
        get_misc_cloak_type(c['stuff'][-1], rand=pct2)


bullet_table = [[20, 0, 0, 0], [30, 0, 0, 0], [50, 20, 0, 0], [70, 30, 0, 0], [90, 50, 0, 0],
                [90, 70, 30, 0], [90, 70, 40, 0], [90, 70, 50, 30], [100, 70, 50, 40]]


def get_bullets(tables, c, class_type="Magic-User"):
    level = int(get_character_level(c, class_type)) - 1
    total_left = 40
    plus = []
    if level > 8:
        level = 8
    plus.append(bullet_table[level][0])
    plus.append(bullet_table[level][1])
    plus.append(bullet_table[level][2])
    plus.append(bullet_table[level][3])
    logging.debug("plus table is {}".format(plus))
    pct = random.randint(1, 100)
    if pct < plus[3] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[3]))
        add_to_inventory(tables, c['weapons'], "Sling Bullet of Impact", random.randint(1, 4))
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[2] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[2]))
        add_to_inventory(tables, c['weapons'], "+3 Sling Bullet", random.randint(2, 8))
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[1] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[1]))
        add_to_inventory(tables, c['weapons'], "+2 Sling Bullet", random.randint(3, 12))
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[0]:
        logging.debug("got percent of {} < {}".format(pct, plus[0]))
        add_to_inventory(tables, c['weapons'], "+1 Sling Bullet", random.randint(5, 20))
        total_left = total_left - c['weapons'][-1]['cnt']
    if total_left > 0:
        c['weapons'].append(new_item("Sling Bullet", 1, 10, cnt=random.randint(1, total_left)))


dart_table = [[20, 0, 0, 0, 0], [30, 0, 0, 0, 0], [50, 20, 0, 0, 0], [70, 30, 0, 0, 0], [90, 50, 0, 0, 0],
              [90, 70, 30, 0, 0], [90, 70, 40, 0, 0], [90, 70, 50, 30, 10], [100, 70, 50, 40, 10]]


def get_darts(tables, c, class_type="Magic-User"):
    level = int(get_character_level(c, class_type)) - 1
    total_left = 16
    plus = []
    if level > 8:
        level = 8
    plus.append(dart_table[level][0])
    plus.append(dart_table[level][1])
    plus.append(dart_table[level][2])
    plus.append(dart_table[level][3])
    plus.append(dart_table[level][4])
    logging.debug("plus table is {}".format(plus))
    pct = random.randint(1, 100)
    if pct < plus[4] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[4]))
        add_to_inventory(tables, c['weapons'], "Dart of the Hornet's Nest", 1)
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[3] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[3]))
        add_to_inventory(tables, c['weapons'], "Dart of Homing", random.randint(1, 2))
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[2] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[2]))
        add_to_inventory(tables, c['weapons'], "Dart +3", random.randint(2, 8))
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[1] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[1]))
        add_to_inventory(tables, c['weapons'], "Dart +2", random.randint(3, 12))
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[0] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[0]))
        add_to_inventory(tables, c['weapons'], "Dart +1", random.randint(5, 20))
        total_left = total_left - c['weapons'][-1]['cnt']
    if total_left > 0:
        logging.debug("total_left is {}".format(total_left))
        c['weapons'].append(new_item("Dart", 1, 10, cnt=random.randint(1, total_left)))


dagger_table = [[20, 0, 0, 0], [30, 0, 0, 0], [50, 20, 0, 0], [70, 30, 0, 0], [90, 50, 0, 0],
                [90, 70, 30, 0], [90, 70, 40, 0], [90, 70, 50, 30], [100, 70, 50, 40]]


def get_throwing_daggers(tables, c, class_type="Magic-User"):
    level = int(get_character_level(c, class_type)) - 1
    total_left = 6
    plus = []
    if level > 8:
        level = 8
    plus.append(dagger_table[level][0])
    plus.append(dagger_table[level][1])
    plus.append(dagger_table[level][2])
    plus.append(dagger_table[level][3])
    logging.debug("plus table is {}".format(plus))
    pct = random.randint(1, 100)
    if pct < plus[3] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[3]))
        add_to_inventory(tables, c['weapons'], "Dagger of Throwing", random.randint(1, 2))
        c['weapons'][-1]['name'] = c['weapons'][-1]['name'] + " +4"
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[2] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[2]))
        add_to_inventory(tables, c['weapons'], "Dagger of Throwing", random.randint(1, 2))
        c['weapons'][-1]['name'] = c['weapons'][-1]['name'] + " +3"
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[1] and total_left > 0:
        logging.debug("got percent of {} < {}".format(pct, plus[1]))
        add_to_inventory(tables, c['weapons'], "Dagger of Throwing", random.randint(1, 3))
        c['weapons'][-1]['name'] = c['weapons'][-1]['name'] + " +2"
        total_left = total_left - c['weapons'][-1]['cnt']
    pct = random.randint(1, 100)
    if pct < plus[0]:
        logging.debug("got percent of {} < {}".format(pct, plus[0]))
        add_to_inventory(tables, c['weapons'], "Dagger of Throwing", random.randint(1, 3))
        c['weapons'][-1]['name'] = c['weapons'][-1]['name'] + " +1"
        total_left = total_left - c['weapons'][-1]['cnt']
    if total_left > 0:
        c['weapons'].append(new_item("Throwing Dagger", 1, 10, cnt=random.randint(1, total_left)))


def get_mage_weapon(tables, c):
    level = int(get_character_level(c, "Magic-User"))
    etcFile = "mu_hand_weapons.txt"
    etcPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'etc'))
    etcFile = os.path.join(etcPath, etcFile)
    hand_weapons = read_equipment(etcFile)
    #    range_weapons = read_equipment("mu_range_weapons.txt")
    pct1 = random.randint(1, 100)
    success = False
    if level < 5:
        if pct1 < (level - 1) * 25:
            success = True
    else:
        success = True
    if success:
        pct2 = random.randint(1, 70) + level * 3
        if pct2 > 100:
            pct2 = 100
        logging.debug("Got magic hand weapon! pct2 is {}".format(pct2))
        for item in hand_weapons:
            if item['pctlo'] <= pct2 and pct2 <= item['pcthi']:
                new = copy.deepcopy(item)
                new['cnt'] = 1
                c['weapons'].append(new)
    else:
        pct = random.randint(1, 100)
        if pct <= 50:
            item = new_item("Dagger", 1, 10)
        else:
            item = new_item("Staff", 1, 10)
        c['weapons'].append(item)

    if level >= 7:
        pct = random.randint(1, 100)
        if pct <= 33:
            # Sling
            pct = random.randint(1, 100)
            if pct > 90:
                add_to_inventory(tables, c['weapons'], "Sling of Seeking +2", 1)
            else:
                item = new_item("Sling", 1, 10)
                c['weapons'].append(item)
            get_bullets(tables, c)
        elif pct <= 66:
            get_darts(tables, c)
        else:
            get_throwing_daggers(tables, c)


def equip_Mage(tables, c):
    level = int(get_character_level(c, "Magic-User"))
    logging.debug("Found magic user level of {}".format(level))

    get_mage_protection(c)
    get_pro_ring(tables, c)
    get_pro_cloak(tables, c)
    get_mage_weapon(tables, c)

    if level <= 3:
        pct = random.randint(1, 100)
        if (pct < (level - 1) * 25):
            add_to_inventory(tables, c['stuff'], "Healing", 1)
        pct = random.randint(1, 100)
        if (pct > 95):
            c['stuff'].append(get_potion(tables))
    elif level <= 6:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 75):
            c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 95):
            c['stuff'].append(get_misc_magic(tables, gplimit=10000, classtype="Magic-User"))
    elif level <= 9:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "Healing XX", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 50):
            c['stuff'].append(get_potion(tables))
            c['stuff'].append(get_misc_magic(tables, gplimit=20000, classtype="Magic-User"))
        if (pct > 85):
            c['stuff'].append(get_misc_magic(tables, gplimit=40000, classtype="Magic-User"))
    else:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "Healing XX", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "HEAL", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_misc_magic(tables, classtype="Magic-User"))
        c['stuff'].append(get_misc_magic(tables, classtype="Magic-User"))
        c['stuff'].append(get_misc_magic(tables, classtype="Magic-User"))
        pct = random.randint(1, 100)
        if pct > 75:
            c['stuff'].append(get_rod_staff(tables, classtype="Cleric"))


def get_thief_protection(c):
    etcFile = "thief_protection.txt"
    etcPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'etc'))
    etcFile = os.path.join(etcPath, etcFile)
    protection = read_equipment(etcFile)
    level = int(get_character_level(c, "Thief"))
    pct1 = random.randint(1, 100)
    pct2 = random.randint(1, 50) + 10 * (level - 3)
    if pct2 > 100:
        pct2 = 100
    got_magic = False
    if level < 4:
        if pct1 < level * 25:
            got_magic = True
    else:
        got_magic = True

    if got_magic:
        logging.debug("Got protection! pct2 is {}".format(pct2))
        for item in protection:
            if item['pctlo'] <= pct2 and pct2 <= item['pcthi']:
                c['armor'] = item['name']
    else:
        c['armor'] = "Leather"


def get_thief_weapon(tables, c):
    level = int(get_character_level(c, "Thief"))
    etcPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'etc'))
    etcFile = os.path.join(etcPath, "magic_swords.txt")
    swords = read_equipment(etcFile)
    etcFile = os.path.join(etcPath, "magic_daggers.txt")
    daggers = read_equipment(etcFile)
    #    range_weapons = read_equipment("thief_range_weapons.txt")

    # First check for a sword
    pct1 = random.randint(1, 100)
    success = False
    if level < 5:
        if pct1 < (level - 1) * 25:
            success = True
    else:
        success = True
    if success:
        pct2 = random.randint(1, 100) + 11 * (level - 3)
        if pct2 > 200:
            pct2 = random.randint(100, 200)
        logging.debug("Got magic sword! pct2 is {}".format(pct2))
        for item in swords:
            if item['pctlo'] <= pct2 and pct2 <= item['pcthi']:
                new = copy.deepcopy(item)
                new['cnt'] = 1
                c['weapons'].append(new)

    # Next check for a dagger 
    pct1 = random.randint(1, 100)
    success = False
    if level < 5:
        if pct1 < (level - 1) * 25:
            success = True
    else:
        success = True
    if success:
        pct2 = random.randint(1, 70) + level * 3
        if pct2 > 100:
            pct2 = 100
        logging.debug("Got magic dagger! pct2 is {}".format(pct2))
        for item in daggers:
            if item['pctlo'] <= pct2 and pct2 <= item['pcthi']:
                new = copy.deepcopy(item)
                new['cnt'] = 1
                c['weapons'].append(new)

    if len(c['weapons']) == 0:
        pct = random.randint(1, 100)
        if pct <= 33:
            item = new_item("Dagger", 1, 10)
        elif pct <= 66:
            item = new_item("Club", 1, 10)
        else:
            item = new_item("Sword (short)", 1, 10)
        c['weapons'].append(item)

    if level >= 5:
        pct = random.randint(1, 100)
        if pct <= 33:
            # Sling
            pct = random.randint(1, 100)
            if pct > 90:
                add_to_inventory(tables, c['weapons'], "Sling of Seeking +2", 1)
            else:
                item = new_item("Sling", 1, 10)
                c['weapons'].append(item)
            get_bullets(tables, c, class_type="Thief")
        elif pct <= 66:
            get_darts(tables, c, class_type="Thief")
        else:
            get_throwing_daggers(tables, c, class_type="Thief")


def equip_Thief(tables, c):
    level = int(get_character_level(c, "Thief"))
    logging.debug("Found thief level of {}".format(level))

    get_thief_protection(c)
    get_pro_ring(tables, c, classtype="Thief")
    get_pro_cloak(tables, c, classtype="Thief")
    get_thief_weapon(tables, c)

    if level <= 4:
        pct = random.randint(1, 100)
        if (pct > 50):
            add_to_inventory(tables, c['stuff'], "Healing", random.randint(1, 2))
        pct = random.randint(1, 100)
        if (pct > 95):
            c['stuff'].append(get_potion(tables))
    elif level <= 6:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 75):
            c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 95):
            c['stuff'].append(get_misc_magic(tables, gplimit=10000, classtype="Thief"))
    elif level <= 9:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "Healing XX", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        pct = random.randint(1, 100)
        if (pct > 50):
            c['stuff'].append(get_potion(tables))
            c['stuff'].append(get_misc_magic(tables, gplimit=20000, classtype="Thief"))
        if (pct > 85):
            c['stuff'].append(get_misc_magic(tables, gplimit=40000, classtype="Thief"))
    else:
        add_to_inventory(tables, c['stuff'], "Extra-Healing", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "Healing XX", random.randint(1, 2))
        add_to_inventory(tables, c['stuff'], "HEAL", random.randint(1, 2))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_potion(tables))
        c['stuff'].append(get_misc_magic(tables, classtype="Thief"))
        c['stuff'].append(get_misc_magic(tables, classtype="Thief"))
        c['stuff'].append(get_misc_magic(tables, classtype="Thief"))
