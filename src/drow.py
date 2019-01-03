#!/usr/bin/python

import logging
from utils import *

def equip_DrowFighter(tables,character):
        level = int(get_character_level(character,"Fighter"))
        logging.debug("Found fighter level of {}".format(level))
        if level <= 4:
            character['armor'] = "Chain Mail +2"
            character['shield'] = "Spiked Buckler +2"
            add_to_inventory(tables,character['weapons'],"Sword +2",1)
            pct = random.randint(1,100)
            if (pct>50):
                add_to_inventory(tables,character['stuff'],"Healing",random.randint(1,2))
            pct = random.randint(1,100)
            if (pct > 95):
                character['stuff'].append(get_potion(tables))
        elif level <= 6:
            character['armor'] = "Chain Mail +3"
            character['shield'] = "Spiked Buckler +3"
            add_to_inventory(tables,character['weapons'],"Sword +3",1)
            add_to_inventory(tables,character['stuff'],"Extra-Healing",random.randint(1,2))
            character['stuff'].append(get_potion(tables))
            pct = random.randint(1,100)
            if (pct > 75):
                character['stuff'].append(get_potion(tables))
            pct = random.randint(1,100)
            if (pct > 95):
                character['stuff'].append(get_misc_magic(tables,gplimit=10000,classtype="Fighter"))
        elif level <= 9:
            character['armor'] = "Chain Mail +4"
            character['shield'] = "Spiked Buckler +4"
            add_to_inventory(tables,character['weapons'],"Sword +4",1)
            add_to_inventory(tables,character['stuff'],"Extra-Healing",random.randint(1,2))
            add_to_inventory(tables,character['stuff'],"Healing XX",random.randint(1,2))
            character['stuff'].append(get_potion(tables))
            pct = random.randint(1,100)
            if (pct > 50):
                character['stuff'].append(get_potion(tables))
                character['stuff'].append(get_misc_magic(tables,gplimit=20000,classtype="Fighter"))
            if (pct > 85):
                character['stuff'].append(get_misc_magic(tables,gplimit=40000,classtype="Fighter"))
        else:
            character['armor'] = "Chain Mail +5"
            character['shield'] = "Spiked Buckler +5"
            add_to_inventory(tables,character['weapons'],"Sword +5",1)
            add_to_inventory(tables,character['stuff'],"Extra-Healing",random.randint(1,2))
            add_to_inventory(tables,character['stuff'],"Healing XX",random.randint(1,2))
            add_to_inventory(tables,character['stuff'],"HEAL",random.randint(1,2))
            character['stuff'].append(get_potion(tables))
            character['stuff'].append(get_potion(tables))
            character['stuff'].append(get_potion(tables))
            character['stuff'].append(get_misc_magic(tables,classtype="Fighter"))
            character['stuff'].append(get_misc_magic(tables,classtype="Fighter"))
            character['stuff'].append(get_misc_magic(tables,classtype="Fighter"))
        pct = random.randint(1,100)
        if pct > 50:
            character['weapons'].append(new_item("Hand Crossbow",100,1000))
            character['weapons'].append(new_item("Sleep Darts",10,100,cnt=random.randint(4,10)))
        else:
            pct = random.randint(1,100)
            if pct > 85:
                character['weapons'].append(new_item("Atlatl",50,500))
                character['weapons'].append(new_item("Javelin",50,500,cnt=random.randint(2,6)))

def equip_DrowFM(tables,character):
        level = get_character_level(character,"Fighter")
        logging.debug("Found fighter level of {}".format(level))
        if level <= 4:
            character['armor'] = "Chain Mail +2"
            character['shield'] = "Spiked Buckler +2"
            add_to_inventory(tables,character['weapons'],"Sword +2",1)
            pct = random.randint(1,100)
            if (pct>50):
                add_to_inventory(tables,character['stuff'],"Healing",random.randint(1,2))
            pct = random.randint(1,100)
            if (pct > 95):
                character['stuff'].append(get_potion(tables))
        elif level <= 6:
            character['armor'] = "Chain Mail +3"
            character['shield'] = "Spiked Buckler +3"
            add_to_inventory(tables,character['weapons'],"Sword +3",1)
            add_to_inventory(tables,character['stuff'],"Extra-Healing",random.randint(1,2))
            character['stuff'].append(get_potion(tables))
            pct = random.randint(1,100)
            if (pct > 75):
                character['stuff'].append(get_potion(tables))
            pct = random.randint(1,100)
            if (pct > 95):
                character['stuff'].append(get_misc_magic(tables,gplimit=10000,classtype="FM"))
        elif level <= 9:
            character['armor'] = "Chain Mail +4"
            character['shield'] = "Spiked Buckler +4"
            add_to_inventory(tables,character['weapons'],"Sword +4",1)
            add_to_inventory(tables,character['stuff'],"Extra-Healing",random.randint(1,2))
            add_to_inventory(tables,character['stuff'],"Healing XX",random.randint(1,2))
            character['stuff'].append(get_potion(tables))
            pct = random.randint(1,100)
            if (pct > 50):
                character['stuff'].append(get_potion(tables))
                character['stuff'].append(get_misc_magic(tables,gplimit=20000,classtype="FM"))
            if (pct > 85):
                character['stuff'].append(get_misc_magic(tables,gplimit=40000,classtype="FM"))
        else:
            character['armor'] = "Chain Mail +5"
            character['shield'] = "Spiked Buckler +5"
            add_to_inventory(tables,character['weapons'],"Sword +5",1)
            add_to_inventory(tables,character['stuff'],"Extra-Healing",random.randint(1,2))
            add_to_inventory(tables,character['stuff'],"Healing XX",random.randint(1,2))
            add_to_inventory(tables,character['stuff'],"HEAL",random.randint(1,2))
            character['stuff'].append(get_potion(tables))
            character['stuff'].append(get_potion(tables))
            character['stuff'].append(get_potion(tables))
            character['stuff'].append(get_misc_magic(tables,classtype="FM"))
            character['stuff'].append(get_misc_magic(tables,classtype="FM"))
            character['stuff'].append(get_misc_magic(tables,classtype="FM"))
        pct = random.randint(1,100)
        if pct > 50:
            character['weapons'].append(new_item("Hand Crossbow",100,1000))
            character['weapons'].append(new_item("Sleep Darts",10,100,cnt=random.randint(4,10)))
        else:
            pct = random.randint(1,100)
            if pct > 85:
                character['weapons'].append(new_item("Atlatl",50,500))
                character['weapons'].append(new_item("Javelin",50,500,cnt=random.randint(2,6)))


def equip_DrowCleric(tables,character):
        level = int(get_character_level(character,"Cleric"))
        if level <= 4:
            character['armor'] = "Chain Mail +2"
            character['shield'] = "Buckler +2"
            add_to_inventory(tables,character['weapons'],"Mace +2",1)
            add_to_inventory(tables,character['weapons'],"Dagger +2",1)
            pct = random.randint(1,100)
            if (pct>50):
                add_to_inventory(tables,character['stuff'],"Healing",random.randint(1,2))
            pct = random.randint(1,100)
            if (pct > 95):
                character['stuff'].append(get_potion(tables))
        elif level <= 6:
            character['armor'] = "Chain Mail +3"
            character['shield'] = "Buckler +3"
            add_to_inventory(tables,character['weapons'],"Mace +3",1)
            add_to_inventory(tables,character['weapons'],"Dagger +3",1)
            add_to_inventory(tables,character['stuff'],"Extra-Healing",random.randint(1,2))
            character['stuff'].append(get_potion(tables))
            pct = random.randint(1,100)
            if (pct > 75):
                character['stuff'].append(get_potion(tables))
            pct = random.randint(1,100) 
            if (pct > 95):
                character['stuff'].append(get_misc_magic(tables,gplimit=10000,classtype="Cleric"))
        elif level <= 9:
            character['armor'] = "Chain Mail +4"
            character['shield'] = "Buckler +4"
            add_to_inventory(tables,character['weapons'],"Mace +4",1)
            add_to_inventory(tables,character['weapons'],"Dagger +3",1)
            add_to_inventory(tables,character['stuff'],"Extra-Healing",random.randint(1,2))
            add_to_inventory(tables,character['stuff'],"Healing XX",random.randint(1,2))
            character['stuff'].append(get_potion(tables))
            pct = random.randint(1,100)
            if (pct > 50):
                character['stuff'].append(get_potion(tables))
                character['stuff'].append(get_misc_magic(tables,gplimit=20000,classtype="Cleric"))
            if (pct > 85):
                character['stuff'].append(get_misc_magic(tables,gplimit=40000,classtype="Cleric"))
        else:
            character['armor'] = "Chain Mail +5"
            character['shield'] = "Buckler +5"
            add_to_inventory(tables,character['weapons'],"Mace +5",1)
            add_to_inventory(tables,character['weapons'],"Dagger +3",1)
            add_to_inventory(tables,character['stuff'],"Extra-Healing",random.randint(1,2))
            add_to_inventory(tables,character['stuff'],"Healing XX",random.randint(1,2))
            add_to_inventory(tables,character['stuff'],"HEAL",random.randint(1,2))
            character['stuff'].append(get_potion(tables))
            character['stuff'].append(get_potion(tables))
            character['stuff'].append(get_potion(tables))
            character['stuff'].append(get_misc_magic(tables,classtype="Cleric"))
            character['stuff'].append(get_misc_magic(tables,classtype="Cleric"))
            pct = random.randint(1,100)
            if pct > 75:
                character['stuff'].append(get_rod_staff(tables,classtype="Cleric"))

