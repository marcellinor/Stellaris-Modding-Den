#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, io
from stellarisTxtRead import *
from copy import deepcopy
from googletrans import Translator
import re
from locList import LocList
from custom_difficulty_files import *
from functools import reduce

debugMode=True

changeSteps = [50, 20, 10]
for s in reversed(changeSteps):
  changeSteps.append(-s)
bonusNames=["capital_building","empire_unique_building","planet_unique_building","military_building","standard_resource_building","research_resource_building","unity_resource_building","special_resource_building","replicator_building", "all"]
bonusPictures=["GFX_CGM_buildings_menu" for entry in bonusNames]
cats=["building_time_mult","building_cost_mult"]
# buildSpeedBonus=[[entry+"_building_time_mult"] for entry in bonusNames if entry !="all"]
# buildCostBonus=[[entry+"_building_cost_mult"] for entry in bonusNames if entry !="all"]
# buildSpeedBonus.append(reduce(lambda x,y: x+y, buildSpeedBonus))
# buildCostBonus.append(reduce(lambda x,y: x+y, buildCostBonus))

# possibleBoniPictures=["GFX_evt_mining_station","GFX_evt_dyson_sphere","GFX_evt_animal_wildlife", "GFX_evt_think_tank", "GFX_evt_unity_symbol","GFX_evt_arguing_senate","GFX_evt_hangar_bay", "GFX_evt_debris", "GFX_evt_sabotaged_ship","GFX_evt_pirate_armada","GFX_evt_fleet_neutral","GFX_evt_city_ruins","GFX_evt_metropolis"]





# # doTranslation=True
# doTranslation=False
# locClass=LocList(doTranslation)
# #global things: No translation needed (mod name and stuff taken from vanilla translations)
# locClass.addLoc("modName", "Dynamic Difficulty", "all")
# locClass.addLoc("minerals", "$minerals$","all")
# locClass.addLoc("energy", "$energy$","all")
# locClass.addLoc("food", "$food$","all")
# locClass.addLoc("research", "$RESEARCH$","all")
# locClass.addLoc("unity", "$unity$","all")
# locClass.addLoc("influence", "$influence$","all")
# locClass.addLoc("cap", "$NAVY_SIZE_TITLE$","all")







# locClass.addEntry("custom_difficulty_current_bonuses","@curBon:")

# # locClass.addEntry(, [])
# # locClass.addEntry(, [])






eventNameSpace="core_game_mechanics_and_ai_base.{!s}"
eventNames="core_game_mechanics_and_ai_base_{!s}"

name_mainMenuEvent="core_game_mechanics_and_ai_base.10"
id_subMainMenuEvent=11
id_Change=[20,30]  #reserved range up to 39


buildingOptionsFile=TagList("namespace","core_game_mechanics_and_ai_base")
mainMenu=TagList("id", name_mainMenuEvent)
mainMenu.add("is_triggered_only", "yes")
mainMenu.add("name", eventNames.format("main_event.name"))
mainMenu.add("desc", eventNames.format("main_event.desc"))
mainMenu.add("picture", "GFX_CGM_buildings_menu")
buildingOptionsFile.addComment("main menu")
buildingOptionsFile.add("country_event", mainMenu)
for catI,cat in enumerate(cats):
  mainSubMenu=TagList("id", eventNameSpace.format(id_subMainMenuEvent+catI))
  mainSubMenu.add("is_triggered_only", "yes")
  mainSubMenu.add("name", eventNames.format(cat+"_event.name"))
  mainSubMenu.add("desc", eventNames.format(cat+"_event.desc"))
  mainSubMenu.add("picture", "GFX_CGM_buildings_menu")
  buildingOptionsFile.addComment(cat)
  buildingOptionsFile.add("country_event", mainSubMenu)
  mainMenu.add("option", TagList("name", eventNames.format(cat)+"_option.name").add("hidden_effect", TagList("country_event", TagList("id",eventNameSpace.format(id_subMainMenuEvent+catI)))))
  bonuses=[[entry+"_"+cat] for entry in bonusNames if entry !="all"]
  bonuses.append(reduce(lambda x,y: x+y, bonuses))
  for bonusI,bonus,bonusName in zip(range(len(bonuses)),bonuses, bonusNames):
    bonusMenu=TagList("id", eventNameSpace.format(id_Change[catI]+bonusI))
    bonusMenu.add("is_triggered_only", "yes")
    bonusMenu.add("name", eventNames.format("{}_{}_event.name".format(cat, bonusName)))
    bonusMenu.add("desc", eventNames.format("{}_{}_event.desc".format(cat, bonusName)))
    bonusMenu.add("picture", "GFX_CGM_buildings_menu")
    buildingOptionsFile.addComment(bonusName+" "+cat)
    buildingOptionsFile.add("country_event", bonusMenu)
    mainSubMenu.add("option", TagList("name", eventNames.format("{}_{}_event_option.name".format(cat, bonusName))).add("hidden_effect", TagList("country_event", TagList("id",eventNameSpace.format(id_Change[catI]+bonusI)))))
    for changeStep in changeSteps:
      bonusMenu.add("option", TagList("name", eventNames.format("change_"+str(changeStep).replace("-", "neg"))))
    bonusMenu.add("option", TagList("name", "BACK").add("hidden_effect", TagList("country_event", TagList("id",eventNameSpace.format(id_subMainMenuEvent+catI)))))
  mainSubMenu.add("option", TagList("name", "BACK").add("hidden_effect", TagList("country_event", TagList("id",name_mainMenuEvent))))
mainMenu.add("option", TagList("name", "BACK").add("hidden_effect", TagList("country_event", TagList("id",1))))


# buildingOptionsFile.printAll()
outputToFolderAndFile(buildingOptionsFile, "events", "cgm_buildings_modifiers.txt", level=2, modFolder="../cgm_buildings_script_source")