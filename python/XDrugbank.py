'''
# ===========================================================
# 3/31/2023
# 11/6/2022 REVISION
# 9/13/2022 add dictAllDrugClasses
# 8/6/2022
'''
# initialize
print("start init.py")
import re
from re import X

from winreg import ExpandEnvironmentStrings
import PySimpleGUI as sg
import pandas as pd
from collections import Counter
import itertools
from pyvis.network import Network
#import networkx as nx
#
# for various file handling:
import os
from datetime import datetime
import sys
import csv
import warnings
from IPython.display import display
#
# Trying to control so that no random network position does not seem to work
# https://networkx.org/documentation/stable/reference/randomness.html 
#import random
#random.seed(84309)
#import numpy
#numpy.random.seed(84309)
# try this ... does not work although may be my fault
# in not using "layout" correctly
# https://github.com/WestHealth/pyvis/issues/66
# G = Network(height="500px", width="100%")
# G.set_options('{"layout": {"randomSeed":5}}')

# ===========================================================
# from other files:
# these are all objects, not functions:
from Xshapes import *
from Xdrug_classes import *
# these are all functions:
import Xfunctions as Xf

# ===========================================================

# these depend on convenience in the display of folded text lines
lenXline = 70 # fold description at this many characters
lenXfoodDigestText = 30 # fold food digest text

# SCENARIO is determined by user selection of what to do
SCENARIO = None
'''
Scenarios:
A - taking one or more classes; test against one drug
B - taking several drugs; test for interactions
C - taking several classes; test amongst themselves

FA - Food interactions for one or more drugs
FB - Food interactions for one class due to complexity
'''

path_to_save = "save/"
# where the data is:
path_to_import = "<where the data is>"
#
dfDrugXcanonicalApp, dfFoodX, dfFoodDigest = Xf.fnReadFiles(path_to_import)
listFoodDigestGroups = list(set(dfFoodDigest['foodDigestGroup'].to_list()))
listFoodDigestGroups.sort()
# require match of groups to images:
_x = list(dictFoodDigestGroupImages.keys())
_x.sort()
if _x != listFoodDigestGroups:
    sg.Popup(F"Error: Food Digest Group Mismatch\ndictFoodDigestGroupImages: {_x}\nlistFoodDigestGroups: {listFoodDigestGroups}")
    quit()
del _x

# -----------------------------------------------

# get classes and drugs organized
dfAllDrugClassesLong, listAllDrugClasses = Xf.fnDrugClasses(dictAllDrugClasses)
dictDBnames = Xf.fnReadDBnameAppAsList(path_to_import)
# a single list composed of the drug names:
listDrugNames = [row['identifier'] for row in dictDBnames]
# use this for case-insensitive search
listDrugNamesLower = [x.lower() for x in listDrugNames]
#

# ======================= DO IT ========================

SCENARIO = None
window = Xf.fnMakeScenarioWindowX()

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break
    if event in ("-A-","-B-","-C-","-FA-","-FB-"):
        show_filter = values['-SHOW FILTER-']
        show_physics = values['-SHOW PHYSICS-']
        if values["-A-"] == True:
            # drugs
            SCENARIO = "A"
            break
        elif values["-B-"] == True:
            # drug and class
            SCENARIO = "B"
            break
        elif values["-C-"] == True:
            # classes
            SCENARIO = "C"
            break
        elif values["-FA-"] == True:
            # drugs
            SCENARIO = "FA"
            break
        elif values["-FB-"] == True:
            # classes
            SCENARIO = "FB"
            break

window.close()
if SCENARIO is None:
    quit()
if SCENARIO == "A":
    # A - taking one class; test against one drug
    #
    listDrugPicked, listClassPicked = \
        Xf.fnMakeWindowsDrugClasses(listDrugNames, listDrugNamesLower, dictAllDrugClasses, listAllDrugClasses)
    #
    # only one drug is allowed in UI
    testThisDrug = listDrugPicked[0]
    #
    dfDrugsOfInterest, dfInteractingDrugs, listInteractingDrugs, listNonInteractingDrugs = \
        Xf.fnPrepScenarioA(testThisDrug, listClassPicked, dfAllDrugClassesLong, dfDrugXcanonicalApp)
    #
    show_this = 'Interactions of ' + testThisDrug + " with " + ', '.join(listClassPicked) + \
        '<br><span style="font-size: 0.9rem; font-family: Arial, font-weight: normal">move cursor over connections for more information' + \
        ' - you can drag the icons for fun</span>'
    #
    Ga = Network(height='900px',width='90%',
                  bgcolor='white',font_color="black",
                  directed=False, heading=show_this,
                  filter_menu=show_filter)
    #
    # Ga goes in and comes out modified
    Ga = Xf.fnPyvisScenarioA(
        Ga, testThisDrug, dictNodeImages, dictNodeColors, listClassPicked, dfDrugsOfInterest, dfInteractingDrugs, 
        listInteractingDrugs, listNonInteractingDrugs, lenXline
    )
    if show_physics:
        Ga.show_buttons(['physics'])
    #
    name_this_file = (('DrugX-' + testThisDrug + '-' + '-'.join(listClassPicked))[0:250]).replace(' ','-')
    Ga.show(name_this_file + '.html')
elif SCENARIO == "B":
    # B - taking several drugs; test for interactions
    #
    listDrugPicked = Xf.fnMakeWindowsDrugs(listDrugNames, listDrugNamesLower, dictAllDrugClasses)
    #
    dfInteractingDrugs, listInteractingDrugs, listNonInteractingDrugs, dictClassPicked = \
        Xf.fnPrepScenarioB(listDrugPicked, dictAllDrugClasses, dfDrugXcanonicalApp)
    #
    show_this = 'Interactions Amongst ' + ', '.join(listDrugPicked) + \
        '<br><span style="font-size: 0.9rem; font-family: Arial, font-weight: normal">move cursor over connections for more information' + \
        ' - you can drag the icons for fun</span>'
    #
    Gb = Network(height='900px',width='90%',
                  bgcolor='white',font_color="black",
                  directed=False, heading=show_this,
                  filter_menu=show_filter)
    #
    # Gb goes in and comes out modified
    Gb = Xf.fnPyvisScenarioB(
        Gb, listInteractingDrugs, listNonInteractingDrugs, dictClassPicked, dictAllDrugClasses, dfInteractingDrugs, 
        dictNodeColors, dictNodeImages, dictNodeShapes, lenXline
    )
    if show_physics:
        Gb.show_buttons(['physics'])
    else:
        Gb.set_options("""var options = {
            "physics": {
                "forceAtlas2Based": {
                "springLength": 100
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based"
            }
        }""")
    #
    name_this_file = (('DrugX-' + '-'.join(listDrugPicked))[0:250]).replace(' ','-')
    Gb.show(name_this_file + '.html')
elif SCENARIO == "C":
    # C - taking several classes; test amongst themselves
    # GENERALLY SPEAKING, THIS IS NOT AT ALL HELPFUL
    # JUST TOO MUCH OF A VISUAL MESS
    #
    listClassPicked = Xf.fnMakeWindowsClasses(SCENARIO, listAllDrugClasses, dictAllDrugClasses)
    if len(listClassPicked) == 0:
        sg.Popup("Bye ... no classes selected.")
        quit()
    #
    # dfInteractingDrugs contains class_name and class_identifier
    dfDrugsOfInterest, dfInteractingDrugs, listInteractingDrugs, listNonInteractingDrugs = \
        Xf.fnPrepScenarioC(listClassPicked, dfAllDrugClassesLong, dfDrugXcanonicalApp)
    #
    show_this = 'Interactions Amongst Classes ' + ', '.join(listClassPicked) + \
        '<br><span style="font-size: 0.9rem; font-family: Arial, font-weight: normal">move cursor over connections for more information' + \
        ' - you can drag the icons for fun</span>'
    #
    Gc = Network(height='900px',width='90%',
                  bgcolor='white',font_color="black",
                  directed=False, heading=show_this,
                  filter_menu=show_filter)
    #
    # Gc goes in and comes out modified
    Gc = Xf.fnPyvisScenarioC(Gc, listClassPicked, dictAllDrugClasses, listInteractingDrugs, dfInteractingDrugs, 
        dfDrugsOfInterest,  dictNodeShapes, dictNodeColors, lenXline)
    # Scenario C does best with some tweaking to accommodate
    #   potential mess when interactions are saturated
    # https://github.com/WestHealth/pyvis/issues/30
    # https://github.com/WestHealth/pyvis/issues/42
    # https://pyvis.readthedocs.io/en/latest/documentation.html
    #
    pct_X_drugs = 0.1
    if show_physics:
        Gc.show_buttons(['physics'])
    else:
        # when high degree of interactions
        if len(listNonInteractingDrugs) < pct_X_drugs * len(listInteractingDrugs):
            Gc.set_options("""var options = {
                "physics": {
                "forceAtlas2Based": {
                "gravitationalConstant": -50,
                "centralGravity": 0.015,
                "springLength": 90,
                "springConstant": 0.055
                },
                "minVelocity": 0.75,
                "maxVelocity": 30,
                "solver": "forceAtlas2Based"
                }
            }""")
    #
    name_this_file = (('DrugX-' + '-'.join(listClassPicked))[0:250]).replace(' ','-')
    Gc.show(name_this_file + '.html')
elif SCENARIO == "FA":
    # FA - taking several drugs; test for food interactions
    # without Food Digest Group
    #
    listDrugPicked = Xf.fnMakeWindowsDrugs(listDrugNames, listDrugNamesLower, dictAllDrugClasses)
    # acknowledge function call
    listClassPicked = []
    dfFoodInteractingDrugs, listFoodInteractingDrugs, listFoodNonInteractingDrugs, dictClassPicked, dfDrugPicked = \
        Xf.fnPrepScenarioFX(SCENARIO, dfFoodX, listDrugPicked, listClassPicked, dictAllDrugClasses, dfAllDrugClassesLong,
        dfFoodDigest, dictFoodDigestActionColors)
    #
    show_this = 'Food Interactions For ' + ', '.join(listDrugPicked) + \
        '<br><span style="font-size: 0.9rem; font-family: Arial, font-weight: normal">move cursor over connections for more information</span>'
    #
    Gfaw = Network(height='900px',width='90%',
                  bgcolor='white',font_color="black",
                  directed=False, heading=show_this,
                  filter_menu=show_filter)
    #
    # Gfaw goes in and comes out modified
    Gfaw = Xf.fnPyvisScenarioFXw(
        Gfaw, SCENARIO, listFoodInteractingDrugs, listFoodNonInteractingDrugs, dictClassPicked, dictAllDrugClasses, dfFoodInteractingDrugs,
        dictNodeColors, dictNodeShapes, dictNodeImages, dictFoodDigestActionImages, lenXline, lenXfoodDigestText
    )
    if show_physics:
        Gfaw.show_buttons(['physics'])    
    else:
        Gfaw.set_options("""var options = {
            "physics": {
            "forceAtlas2Based": {
            "springLength": 100,
            "avoidOverlap": 0.38
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
            }
        }""")
    #
    name_this_file = (('FoodX-' + '-'.join(listDrugPicked))[0:250]).replace(' ','-')
    Gfaw.show(name_this_file + '.html')
elif SCENARIO == "FB":
    # FB - allow only one class due to image complexity
    #
    listClassPicked = Xf.fnMakeWindowsClasses(SCENARIO, listAllDrugClasses, dictAllDrugClasses)
    if len(listClassPicked) == 0:
        sg.Popup("Bye ... no classes selected.")
        quit()
    dfFoodInteractingDrugs, listFoodInteractingDrugs, listFoodNonInteractingDrugs, dictClassPicked, dfDrugPicked = \
        Xf.fnPrepScenarioFX(SCENARIO, dfFoodX, [], listClassPicked, dictAllDrugClasses, dfAllDrugClassesLong,
        dfFoodDigest, dictFoodDigestActionColors)
    #
    show_this = 'Food Interactions For Class ' + ', '.join(listClassPicked) + \
        '<br><span style="font-size: 0.9rem; font-family: Arial, font-weight: normal">move cursor over connections for more information</span>'
    #
    # do not use Food Digest Group
    #
    Gfbw = Network(height='900px',width='90%',
                  bgcolor='white',font_color="black",
                  directed=False, heading=show_this,
                  filter_menu=show_filter)
    #
    # Gfbw goes in and comes out modified
    Gfbw = Xf.fnPyvisScenarioFXw(
        Gfbw, SCENARIO, listFoodInteractingDrugs, listFoodNonInteractingDrugs, dictClassPicked, dictAllDrugClasses, dfFoodInteractingDrugs,
        dictNodeColors, dictNodeShapes, dictNodeImages, dictFoodDigestActionImages, lenXline, lenXfoodDigestText
    )
    if show_physics:
        Gfbw.show_buttons(['physics'])
    else:
        Gfbw.set_options("""var options = {
            "physics": {
            "forceAtlas2Based": {
            "springLength": 100,
            "avoidOverlap": 0.38
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
            }
        }""")
    #
    name_this_file = (('FoodX-' + '-'.join(listClassPicked))[0:250]).replace(' ','-')
    Gfbw.show(name_this_file + '.html')
# ====================================================================