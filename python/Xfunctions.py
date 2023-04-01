# ================ FUNCTIONS ===========================
import pandas as pd
import PySimpleGUI as sg
import csv

def fnCatalog(d):
    # argument should be dir()
    # https://www.geeksforgeeks.org/viewing-all-defined-variables-in-python/
    all_variables = d
    # Iterate over the whole list where dir( ) is stored.
    for _name in all_variables:
        #Print the item if it doesn't start with '__'
        if not _name.startswith('__'):
            myvalue = eval(_name)
            print(_name, "is", type(myvalue))
    #
    return 

def fnReadDBnameAppAsList(path_to_import):
    # get names: 
    file = open(path_to_import + 'DB_name_app.csv','r')
    _tmp = list(csv.DictReader(file, delimiter=","))
    file.close()
    #
    return _tmp

def fnIsDrugInClasses(testDrug, listClasses, dictAllDrugClasses):
    #print("testDrug: " + testDrug + " and listClasses: " + str(listClasses))
    _returnClass = None
    _drugInClass = False
    for _c in listClasses:
        if testDrug in dictAllDrugClasses[_c]['drugs']:
            _returnClass = _c
            _drugInClass = True
            break
    return _drugInClass, _returnClass

def fnIsDrugInAnyClass(testDrug, dictAllDrugClasses):
    # assumes in at most one class
    _returnClass = None
    _returnDesc = None
    for _key in dictAllDrugClasses:
        if testDrug in dictAllDrugClasses[_key]['drugs']:
            _returnClass = _key
            _returnDesc = dictAllDrugClasses[_key]['desc']
            break
    return _returnClass, _returnDesc

def fnReadFiles(path_to_import):
    #global dfDrugXX, dfDrugXcanonicalApp, dfFoodX, dfFoodDigest
    # read csv files 
    # drugDigest and description:
    # "weight", "drugDigest", "description", "descContains [BOTH]"
    # "description" is the text field containing <name> and <with_name>
    # 11/6/2022 drop
    # dfDrugXX = pd.read_csv(path_to_import + "drugX_X.csv", index_col=False)
    #
    # interactions:
    # "drugbankId","name","parentKey","identifier","descContains","weight","drugDigest"
    #
    # "drugbankId","name","description","parentKey","identifier","weight"
    _dfDrugXcanonicalApp = pd.read_csv(path_to_import + "drugX_canonical_app_new_series.csv", index_col=False)
    #
    # ============= food interactions ==================
    #
    # foodInteraction, drugbankId, identifier, digestCode, shortInteraction
    # foodDigestText + shortInteraction is foodInteraction
    # shortInteraction may be empty ("")
    # digestCode matches foodDigestText 
    # example:
    # "Administer vitamin supplements. Administer Vitamin D supplements to minimize the risk of bone mineral density loss.",DB11979,"Elagolix",D04,"Administer Vitamin D supplements to minimize the risk of bone mineral density loss."
    # where D04 is "Administer vitamin supplements."
    # identifier is the drug name
    # foodInteraction, drugbankId, identifier, foodDigestCode, shortInteraction
    _dfFoodX = pd.read_csv(path_to_import + 'drug_food_interactions_app.csv', index_col=False)
    _dfFoodX.rename(columns={"digestCode": "foodDigestCode"}, inplace=True)
    #
    # this is a small file, 68 lines of data 10/2022
    # foodDigestText, foodDigestCode, foodDigestGroup, foodDigestAction
    _dfFoodDigest = pd.read_csv(path_to_import + 'food_phrases_rev.csv', index_col=False)
    #
    # return dfDrugXX, dfDrugXcanonicalApp, dfFoodX, dfFoodDigest
    return _dfDrugXcanonicalApp, _dfFoodX, _dfFoodDigest

def fnGetDrugSearchList(searchFor, listDrugNames, listDrugNamesLower):
    # case insensitive search of listDrugNames
    _items = [i for (i, x) in enumerate(listDrugNamesLower) if x.startswith(searchFor.lower())]
    _len_items = len(_items)
    if _len_items == 0:
        _updatedList = []
    else:
        _updatedList = listDrugNames[_items[0] : (_items[0] + _len_items)]
    #
    return _updatedList

def fnDrugClasses(dictAllDrugClasses):
    # dictAllDrugClasses is global
    # a single list composed of the drug classes:
    #
    _listAllDrugClasses = list(dictAllDrugClasses.keys())
    #
    # dfAllDrugClassesLong composed of columns (equal to longest list), row name is class, cell as drug name:
    # use transpose to get column name as class, drug name
    # a very round-about way ...
    #
    dictAllDrugClassesDrugs = {}
    for _key in dictAllDrugClasses:
        dictAllDrugClassesDrugs[_key] = dictAllDrugClasses[_key]['drugs']
    #
    _dfAllDrugClasses = pd.DataFrame.from_dict(dictAllDrugClassesDrugs, orient='index').transpose()
    # transpose the transpose
    _dfAllDrugClassesT = _dfAllDrugClasses.transpose()
    # take care of the stubborn row name
    _dfAllDrugClassesT.reset_index( inplace=True )
    # for convenience - not necessary
    _dfAllDrugClassesT.rename(columns={'index':'class'}, inplace=True )
    # melt into two columns
    _dfAllDrugClassesLong = pd.melt(_dfAllDrugClassesT, id_vars=['class'] )
    # drop the extra column produced by melt
    _dfAllDrugClassesLong.drop(labels=['variable'], axis=1, inplace=True )
    # rename columns
    _dfAllDrugClassesLong.rename(columns={'value':'name'}, inplace=True )
    _dfAllDrugClassesLong.sort_values('class', inplace=True )
    # get rid of na rows
    _dfAllDrugClassesLong.dropna( inplace=True )
    #
    # get the drug names
    #
    return _dfAllDrugClassesLong, _listAllDrugClasses

def fnFoldTextItem(Item, lenX):
    _len_item = len(Item)
    _new_item = Item
    if _len_item > lenX:
        _space_at = Item[int(_len_item/2):].find(" ")
        if _space_at >= 0 and len(Item[int(_len_item/2):]) > 0:
            _new_item = Item[:int(_len_item/2) + _space_at] + '\n' + Item[int(_len_item/2) + _space_at + 1:]
    return(_new_item)

# WINDOWS FUNCTIONS =======================================
 
def fnMakeScenarioWindowX():
    _options_at_bottom = [sg.Text("             "), sg.CB('Show Filter/Search', enable_events=True, key='-SHOW FILTER-'),
    sg.CB('Show Physics', enable_events=True, key='-SHOW PHYSICS-')]
    #
    _col_drugX = [
        [sg.Text("                                          ", size=(20,2))],
        [sg.Text("            Select A Drug-Drug Interaction", size=(30,2))],
        [sg.Text("           "),
        sg.Radio("Select drugs", "CHOOSEDRUG", enable_events=True, default=False, key="-B-", size=(30,4)),
        sg.Text("           ")],
        [sg.Text("           "),
        sg.Radio("Select one drug and one class", "CHOOSEDRUG", enable_events=True, default=False, key="-A-", size=(30,4)),
        sg.Text("           ")],
        [sg.Text("           "),
        sg.Radio("Select classes", "CHOOSEDRUG", enable_events=True, default=False, key="-C-", size=(30,3)),
        sg.Text("           ")],
        [sg.Text("                                          ")],
        [sg.Text("           ")]
        ]
    #
    _col_buffer = [
        [sg.Text("    ")]
        ]
    #
    _col_foodX = [
        [sg.Text("                                          ", size=(20,2))],
        [sg.Text("            Select A Drug-Food Interaction", size=(30,2))],
        [sg.Text("           "),
        sg.Radio("Select one or more drugs", "CHOOSEFOOD", enable_events=True, default=False, key="-FA-", size=(30,4)),
        sg.Text("           ")],
        [sg.Text("           "),
        sg.Radio("Select only one class", "CHOOSEFOOD", enable_events=True, default=False, key="-FB-", size=(30,3)),
        sg.Text("           ")],
        [sg.Text("                                          ")],
        [sg.Text("           ")]
        ]
    #
    _bottom = [
        [_options_at_bottom],
        [sg.Text("              "), sg.Button(button_text='Exit', key="-EXIT-")]
    ]
    #
    layout = [[sg.Column(_col_drugX), sg.Column(_col_buffer), sg.Column(_col_foodX)],[_bottom]]
    #
    return sg.Window("Select Drug-Drug or Drug-Food Interaction", layout, location=(800,400), finalize=True)


def fnMakeScenarioWindowDrugX():
    _options_at_bottom = sg.pin(sg.Column([[sg.CB('Show Filter/Search', enable_events=True, key='-SHOW FILTER-'),
    sg.CB('Show Physics', enable_events=True, key='-SHOW PHYSICS-')]], pad=(0,0), key="-OPTIONS BOTTOM-"))
    #
    layout = [
        [sg.Text("                                          ", size=(20,2))],
        [sg.Text("            Select A Drug-Drug Interaction", size=(30,2))],
        [sg.Text("           "),
        sg.Radio("Select drugs", "CHOOSE", enable_events=True, default=False, key="-B-", size=(30,4)),
        sg.Text("           ")],
        [sg.Text("           "),
        sg.Radio("Select one drug and several classes", "CHOOSE", enable_events=True, default=False, key="-A-", size=(30,4)),
        sg.Text("           ")],
        [sg.Text("           "),
        sg.Radio("Select classes", "CHOOSE", enable_events=True, default=False, key="-C-", size=(30,3)),
        sg.Text("           ")],
        [sg.Text("                                          ")],
        [sg.Text("           ")],
        [_options_at_bottom],
        [sg.Text("                                          ", size=(20,1))],
        [sg.Text("", size=(12,1)), sg.Button(button_text='Exit', key="-EXIT-")],
        [sg.Text("                                          ")]
    ]
    return sg.Window("Select A Drug-Drug Interaction", layout, location=(800,400), finalize=True)

def fnMakeScenarioWindowFoodX():
    _options_at_bottom = sg.pin(sg.Column([[sg.CB('Show Filter/Search', enable_events=True, key='-SHOW FILTER-'),
    sg.CB('Show Physics', enable_events=True, key='-SHOW PHYSICS-')]], pad=(0,0), key="-OPTIONS BOTTOM-"))
    #
    layout = [
        [sg.Text("                                          ", size=(20,2))],
        [sg.Text("            Select A Drug-Food Interaction", size=(30,2))],
        [sg.Text("           "),
        sg.Radio("Select one or more drugs", "CHOOSE", enable_events=True, default=False, key="-FA-", size=(30,4)),
        sg.Text("           ")],
        #[sg.Text("           "),
        #sg.Radio("Select one drug and several classes", "CHOOSE", enable_events=True, default=False, key="-A-", size=(30,4)),
        #sg.Text("           ")],
        [sg.Text("           "),
        sg.Radio("Select one or more classes", "CHOOSE", enable_events=True, default=False, key="-FB-", size=(30,3)),
        sg.Text("           ")],
        [sg.Text("                                          ")],
        [sg.Text("           ")],
        [_options_at_bottom],
        [sg.Text("                                          ", size=(20,1))],
        [sg.Text("", size=(12,1)), sg.Button(button_text='Exit', key="-EXIT-")],
        [sg.Text("                                          ")]
    ]
    #
    return sg.Window("Select A Drug-Food Interaction", layout, location=(800,400), finalize=True)

# ====================================================================
#
# 10/01/2022
# use a listbox that will present a subset of drugs
# those starting with whatever the user types into the search box
# this to get around the problem of NOT being able to scroll the listbox display programatically
#
# ==================== Make Windows and Gather Data ==========================

# ========== DRUGCLASSES =============

def fnMakeWindowsDrugClasses(listDrugNames, listDrugNamesLower, dictAllDrugClasses, listAllDrugClasses):
    # A - taking one class; test against one drug

    # dictAllDrugClasses is global
    # listDrugNames is global
    
    #               USER INTERFACE
    # https://www.blog.pythonlibrary.org/2021/01/20/pysimplegui-working-with-multiple-windows/ 
    # starting with entire list displayed (length about 2400) from listDrugNames

    # one window

    def make_win():
        _header_section = [sg.Text("Select one drug and one class.")]

        _class_section = [[sg.Text('Note: Diuretics include Loop Diuretics, Potassium Sparing Diuretics and Thiazide Diuretics.')],
                        [sg.Text('Click to Select Class'), sg.Stretch(), sg.Text('Click to Deselect Class')],
                        [sg.Listbox(values=listAllDrugClasses, size=(30,12), enable_events=True, key="-CLASSLIST-"), 
                        sg.Listbox(values=_listClassPicked, size=(30,12), enable_events=True, key="-CLASSPICKED-"),
                        sg.Listbox(values=_listAssocDesc, size=(30,12), enable_events=False, key="-DESC-")]]

        _drug_section = [[sg.Text('Enter start of drug name.')],
                        [sg.Input(do_not_clear=True, size=(20,1),enable_events=True, key='-DRUGSEARCH-')],
                        [sg.Text('Click to Select Drug'), sg.Stretch(), sg.Text('Click to Deselect Drug')],
                        [sg.Listbox(values=listDrugNames, size=(30,12), enable_events=True, key="-DRUGLIST-"), 
                        sg.Listbox(values=_listDrugPicked, size=(30,12), enable_events=True, key="-DRUGPICKED-")]]

        _buttons_section = [[sg.Button(button_text='Proceed', key="-PROCEED-"), 
                        sg.Button(button_text="Exit", key="-EXIT-")]]

        layout = [_header_section,
            [sg.Frame("", _class_section)],
            [sg.Frame("", _drug_section)],
            [sg.Frame("", _buttons_section)]]
        return sg.Window('Select Drug and Class for Interactions', layout, location=(800,200), finalize=True)

    _listClassPicked = []
    _listAssocDesc = []
    _listDrugPicked = []

    window = make_win()
    
    # Event Loop
    # https://stackoverflow.com/questions/57072250/updating-gui-items-withing-the-process
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == '-EXIT-':
            window.close()
            quit()
        elif event == "-PROCEED-":
            # win2 event proceed
            # check to see if more than one drug selected
            if len(_listDrugPicked) > 1:
                sg.Popup("Oops - you can select only one drug or use Exit to leave.")
            elif len(_listDrugPicked) == 0:
                sg.Popup("Select a drug or use Exit to leave.")
            elif len(_listClassPicked) == 0:
                sg.Popup("Select at least one class or use Exit to leave.")
            elif len(list(_listClassPicked)) > 1:
                sg.Popup("Select only one class and one drug or use Exit to leave")
            else:
                #window.close()
                break
        elif event == "-CLASSLIST-" and values["-CLASSLIST-"]:
            _classIs = values['-CLASSLIST-'][0]
            _listClassPicked.append(_classIs)
            _listAssocDesc.append(dictAllDrugClasses[_classIs]['desc'])
            window['-CLASSPICKED-'].update(_listClassPicked)
            window['-DESC-'].update(_listAssocDesc)
            # unevent it:
            window['-CLASSLIST-'].update(set_to_index=[])
            window['-DESC-'].update(set_to_index=[])
        elif event == "-CLASSPICKED-" and values["-CLASSPICKED-"]:
            _classIs = values['-CLASSPICKED-'][0]
            _listClassPicked.remove(_classIs)
            _listAssocDesc.remove(dictAllDrugClasses[_classIs]['desc'])
            window['-CLASSPICKED-'].update(_listClassPicked)
            window['-DESC-'].update(_listAssocDesc)
            window['-CLASSPICKED-'].update(set_to_index=[])
            window['-DESC-'].update(set_to_index=[])
        elif event == "-DRUGSEARCH-" and values["-DRUGSEARCH-"]:
            if values["-DRUGSEARCH-"] != "":
                _searchFor = values["-DRUGSEARCH-"]
                if _searchFor.isalpha() == False:
                    sg.Popup('Please enter only alphabetic characters.')
                else:
                    # look for case-insensitive start string but need the properly cased list of hits
                    _updatedList = fnGetDrugSearchList(_searchFor, listDrugNames, listDrugNamesLower)
                    window["-DRUGLIST-"].update(values=_updatedList)
                    window.refresh()
        elif event == "-DRUGLIST-" and values["-DRUGLIST-"]:
            _listDrugPicked.append(values['-DRUGLIST-'][0])
            window['-DRUGPICKED-'].update(_listDrugPicked)
            # unevent it:
            window['-DRUGLIST-'].update(set_to_index=[])
            #
            # check to see if drug is in one of the selected classes
            inClass, theClass = fnIsDrugInClasses(_listDrugPicked[0], _listClassPicked, dictAllDrugClasses)
            if inClass == True:
                sg.Popup(
                    _listDrugPicked[0] + ' is in Class ' + theClass + '. Your drug cannot be in any of your classes. Please either change ' + _listDrugPicked[0] + ' or remove ' + theClass
                )
        elif event == "-DRUGPICKED-" and values["-DRUGPICKED-"]:
            _listDrugPicked.remove(values['-DRUGPICKED-'][0])
            window['-DRUGPICKED-'].update(_listDrugPicked)
            window['-DRUGPICKED-'].update(set_to_index=[])

    window.close()
    return _listDrugPicked, _listClassPicked

# ======================= CLASSES ==================

def fnMakeWindowsClasses(SCENARIO, listAllDrugClasses, dictAllDrugClasses):
    # C, FB - taking several classes; test amongst themselves
    #
    def make_win():
        layout = [
            [sg.Text('Note: Diuretics include Loop, Potassium Sparing and Thiazide.')],
            [sg.Text('Click to Select'), sg.Text('              '), sg.Text('Click to Deselect')],
            [sg.Listbox(values=listAllDrugClasses, size=(30,12), enable_events=True, key="-CLASSLIST-"), 
            sg.Listbox(values=_listClassPicked, size=(30,12), enable_events=True, key="-CLASSPICKED-"),
            sg.Listbox(values=_listAssocDesc, size=(30,12), enable_events=False, key="-DESC-")],
            [sg.Button(button_text='Proceed', key="-PROCEED-"),
            sg.Button(button_text='Exit', key="-EXIT-")]
        ]
        return sg.Window(_show_this, layout, location=(800,400), finalize=True)
    #
    if SCENARIO == "C":
        _show_this = 'Select two drug classes.'
    elif SCENARIO == "FB":
        _show_this = 'Select only one drug class.'
    else:
        sg.Popup("SCENARIO should be C or FB but is " + SCENARIO)
        quit()
    #
    _listClassPicked = []
    _listAssocDesc = []
    # there is only one window 
    window = make_win()
    # Event Loop
    while True:
        event, values = window.read()
        #
        if event == sg.WIN_CLOSED or event == '-EXIT-':
            window.close()
            quit()
        elif event == "-CLASSLIST-" and values["-CLASSLIST-"]:
            _classIs = values['-CLASSLIST-'][0]
            _listClassPicked.append(_classIs)
            #_listClassPicked.append(values['-CLASSLIST-'][0])
            _listAssocDesc.append(dictAllDrugClasses[_classIs]['desc'])
            window['-CLASSPICKED-'].update(_listClassPicked)
            window['-DESC-'].update(_listAssocDesc)
            # unevent it:
            window['-CLASSLIST-'].update(set_to_index=[])
            window['-DESC-'].update(set_to_index=[])
        elif event == "-CLASSPICKED-" and values["-CLASSPICKED-"]:
            _classIs = values['-CLASSPICKED-'][0]
            _listClassPicked.remove(_classIs)
            _listAssocDesc.remove(dictAllDrugClasses[_classIs]['desc'])
            window['-CLASSPICKED-'].update(_listClassPicked)
            window['-DESC-'].update(_listAssocDesc)
            window['-CLASSPICKED-'].update(set_to_index=[])
            window['-DESC-'].update(set_to_index=[])
        #elif event == "-PROCEED-" and values["-PROCEED-"]:
        elif event == "-PROCEED-":
            if SCENARIO == "C" and len(_listClassPicked) != 2:
                sg.Popup("Select two classes or use Exit to leave.")
            elif SCENARIO == "FB" and len(_listClassPicked) > 1:
                sg.Popup("Select only one drug class or use Exit to leave.")
            else:
                break
    #
    window.close()
    return _listClassPicked

# =========== FA ================

def fnMakeWindowsDrugs(listDrugNames, listDrugNamesLower, dictAllDrugClasses):
    # FA - taking several drugs; test for food interactions

    # only one window
    # three panels (listboxes)

    def make_win():
        layout = [
            [sg.Text('Enter start of drug name.')],
            [sg.Input(do_not_clear=True, size=(20,1),enable_events=True, key='-DRUGSEARCH-')],
            [sg.Text('Click to select a drug'), sg.Stretch(), sg.Text('Click to deselect a drug'), sg.Stretch(), sg.Text("Class"), sg.Stretch(), sg.Text('Description')],
            [sg.Listbox(values=listDrugNames, size=(30,12), enable_events=True, key="-DRUGLIST-"), 
            sg.Listbox(values=_listDrugPicked, size=(30,12), enable_events=True, key="-DRUGPICKED-"),
            sg.Listbox(values=_listAssocClasses, size=(30,12), enable_events=False, key="-CLASSES-"),
            sg.Listbox(values=_listAssocDesc, size=(30,12), enable_events=False, key="-DESC-")],
            [sg.Button(button_text='Proceed', key="-PROCEED-"),sg.Button(button_text='Exit', key="-DRUGEXIT-")]
        ]
        return sg.Window('Select one or more drugs', layout, location=(800,400), finalize=True)

    _listDrugPicked = []
    _listAssocClasses = []
    _listAssocDesc  = []
    # there is only one window
    window = make_win()

    # Event Loop
    # https://stackoverflow.com/questions/57072250/updating-gui-items-withing-the-process

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == '-DRUGEXIT-':
            window.close
            quit()
        elif event == '-PROCEED-':
            # close
            # check to see if more than one drug selected
            if len(_listDrugPicked) == 0:
                sg.Popup(
                    "Please select at least one drug or use Exit to leave."
                )
            else:
                break
        elif event == "-DRUGSEARCH-" and values["-DRUGSEARCH-"]:
            # search for drug
            if values["-DRUGSEARCH-"] != "":
                searchFor = values["-DRUGSEARCH-"]
                if searchFor.isalpha() == False:
                    sg.Popup(
                        'Please enter only alphabetic characters.'
                    )
                else:
                    # look for case-insensitive start string but need the properly cased list of hits
                    _updatedList = fnGetDrugSearchList(searchFor, listDrugNames, listDrugNamesLower)
                    window["-DRUGLIST-"].update(values=_updatedList)
                    window.refresh()
        elif event == "-DRUGLIST-" and values["-DRUGLIST-"]:
            # add a drug
            _listDrugPicked.append(values['-DRUGLIST-'][0])
            window['-DRUGPICKED-'].update(_listDrugPicked)
            # in a class?
            _returnClass, _returnDesc = fnIsDrugInAnyClass(values['-DRUGLIST-'][0], dictAllDrugClasses)
            if _returnClass is None:
                _returnClass = 'N/A'
                _returnDesc = 'N/A'
            _listAssocClasses.append(_returnClass)
            _listAssocDesc.append(_returnDesc)
            window['-CLASSES-'].update(_listAssocClasses)
            window['-DESC-'].update(_listAssocDesc)

            # unevent it:
            window['-DRUGLIST-'].update(set_to_index=[])
            window['-CLASSES-'].update(set_to_index=[])
            window['-DESC-'].update(set_to_index=[])
        elif event == "-DRUGPICKED-" and values["-DRUGPICKED-"]:
            # remove a drug
            itemIndex = _listDrugPicked.index(values['-DRUGPICKED-'][0])
            #listDrugPicked.remove(values['-DRUGPICKED-'][0])
            del _listDrugPicked[itemIndex]
            del _listAssocClasses[itemIndex]
            del _listAssocDesc[itemIndex]
            window['-DRUGPICKED-'].update(_listDrugPicked)
            window['-CLASSES-'].update(_listAssocClasses)
            window['-DESC-'].update(_listAssocDesc)
            window['-DRUGPICKED-'].update(set_to_index=[])
            window['-CLASSES-'].update(set_to_index=[])
            window['-DESC-'].update(set_to_index=[])
        else:
            # nothing
            print("How did I get here?")
    
    window.close()
    return _listDrugPicked

# ===================== Prep ===================================

# ================ A =====================

def fnPrepScenarioA(testThisDrug, listClassPicked, dfAllDrugClassesLong, dfDrugXcanonicalApp):
    # A - taking one or more classes; test against one drug

    # listClassPicked and listDrugPicked globals
    # 
    # ====================================================
    # receive selected drug classes and the subject drug as
    #   listClassPicked as a list of one or more classes
    #   listDrugPicked as a list of one drug
    #

    _dfClassPicked = pd.DataFrame(listClassPicked, columns=['class'])

    # drugs belonging to a class use dfAllDrugClassesLong
    # these are all the classes and their drugs
    # these compose the class node to drug nodes

    # THIS DOES NOT INCLUDE testThisDrug
    _dfDrugsOfInterest = _dfClassPicked.join(
        dfAllDrugClassesLong.set_index('class'),
        how  = "left",
        on = 'class'
    )
    #
    _listDrugsOfInterest = _dfDrugsOfInterest['name'].to_list()
    # make sure there are no duplicates
    _listDrugsOfInterest = list(set(_listDrugsOfInterest))

    # which drugs do and do not interact with testThisDrug
    # use dfDrugXcanonicalApp
    # narrow to testThisDrug

    _dfNarrow = dfDrugXcanonicalApp.query(f"identifier == '{testThisDrug}'")

    _dfInteractingDrugs = _dfDrugsOfInterest.join(
        _dfNarrow.set_index('name'),
        how = "inner",
        on = 'name'
    )

    _dfInteractingDrugs.dropna( inplace=True)
    
    _listInteractingDrugs = _dfInteractingDrugs['name'].to_list()
    # make sure there are no duplicates
    _listInteractingDrugs = list(set(_listInteractingDrugs))

    _listNonInteractingDrugs = list(set(_listDrugsOfInterest) - set(_listInteractingDrugs))
    #
    # dfInteractingDrugs is a dataframe (name and class). listNonInteractingDrugs is a list
    # testThisDrug IS NOT IN ANY OF THESE OBJECTS
    return _dfDrugsOfInterest, _dfInteractingDrugs, _listInteractingDrugs, _listNonInteractingDrugs

# ============================= B =========================

def fnPrepScenarioB(listDrugPicked, dictAllDrugClasses, dfDrugXcanonicalApp):
    # B - taking several drugs; test for interactions
    
    # determine classes and interactions
    # classes will be used in constructing plot but play no other role
    # use fnIsDrugInAnyClass one drug at a time
    #   returns None if not in a class

    _dictClassPicked = {}
    for _d in listDrugPicked:
        # returns None if not in a class
        # assumes in at most one class
        _x, _ = fnIsDrugInAnyClass(_d, dictAllDrugClasses)
        if _x is not None:
            _dictClassPicked[_d] = _x
    if '_d' in locals(): del _d
    if '_x' in locals(): del _x
    # get interactions amongst listDrugPicked

    _dfDrugPicked = pd.DataFrame(listDrugPicked, columns=['identifier'])

    _dfInteractingDrugsIdent = dfDrugXcanonicalApp.join(
        _dfDrugPicked.set_index('identifier'),
        how = "inner",
        on = 'identifier'
    )
    _dfInteractingDrugsIdent.dropna( inplace=True)

    _dfInteractingDrugs = _dfInteractingDrugsIdent.query(F"identifier in {listDrugPicked} and name in {listDrugPicked}")
 
    _listInteractingDrugs = _dfInteractingDrugs['identifier'].to_list() + _dfInteractingDrugs['name'].to_list()
    # make sure there are no duplicates
    _listInteractingDrugs = list(set(_listInteractingDrugs))
    
    _listNonInteractingDrugs = list(set(listDrugPicked) - set(_listInteractingDrugs))
    #
    return  _dfInteractingDrugs, _listInteractingDrugs, _listNonInteractingDrugs, _dictClassPicked

# ======================== C ==============================

def fnPrepScenarioC(listClassPicked, dfAllDrugClassesLong, dfDrugXcanonicalApp):
    # C - taking several classes; test amongst themselves
    #
    _dfClassPicked = pd.DataFrame(listClassPicked, columns=['class'])
    #
    # drugs belonging to a class use dfAllDrugClassesLong
    # these are all the classes and their drugs
    # these compose the class node to drug nodes
    # class, name
    #
    _dfDrugsOfInterest = _dfClassPicked.join(
        dfAllDrugClassesLong.set_index('class'),
        how = "left",
        on = 'class'
    )
    #
    _listDrugsOfInterest = _dfDrugsOfInterest['name'].to_list()
    # make sure there are no duplicates
    _listDrugsOfInterest = list(set(_listDrugsOfInterest))
    #
    # exclude interactions within classes
    #
    # only care about these drug interaction:

    _dfNarrow = dfDrugXcanonicalApp.query(F"identifier in {_listDrugsOfInterest} and name in {_listDrugsOfInterest}")
    _dfNarrow.reset_index(inplace=True)

    _dfInteractingDrugs = _dfNarrow.join(
        _dfDrugsOfInterest.set_index('name'),
        how = 'inner',
        on = 'name'
    )
    _dfInteractingDrugs.reset_index(drop=True, inplace=True)
    _dfInteractingDrugs.rename(columns={'class':'class_name'}, inplace=True, errors='raise')

    _dfTmp = _dfDrugsOfInterest.copy()
    _dfTmp['identifier'] = _dfTmp['name']
    _dfTmp = _dfTmp.loc[:, ~_dfTmp.columns.isin(['name'])]
    #
    _dfInteractingDrugs2 = _dfInteractingDrugs.join(
        _dfTmp.set_index('identifier'),
        how = 'inner',
        on = 'identifier'
    )
    #
    _dfInteractingDrugs2.rename(columns={'class':'class_identifier'}, inplace=True, errors='raise')
    _dfInteractingDrugs2.dropna( inplace=True)
    
    # remove where class_name == class_identifier
    # retains the two classes as well as redundant 'duplcate' rows
    # (name,identifier) <-> (identifier,name)
    _dfInteractingDrugs2.query("class_name != class_identifier", inplace=True)
    #
    _listInteractingDrugs = _dfInteractingDrugs2['name'].values.tolist()
    # make sure there are no duplicates
    _listInteractingDrugs = list(set(_listInteractingDrugs))
    _listNonInteractingDrugs = list(set(_listDrugsOfInterest) - set(_listInteractingDrugs))
    #
    # dfInteractingDrugs2 contains class_name and class_identifier
    return _dfDrugsOfInterest, _dfInteractingDrugs2, _listInteractingDrugs, _listNonInteractingDrugs

# ============================= FX =========================

def fnPrepScenarioFX(SCENARIO, dfFoodX, listDrugPicked, listClassPicked, dictAllDrugClasses, dfAllDrugClassesLong, dfFoodDigest, dictFoodDigestActionColors):
    # FA - taking several drugs; test for food interactions
    # FB - several classes
    #
    # determine foodDigestCodes for the interactions
    #
    if SCENARIO == "FA":
        # drugs
        #
        # determine classes
        # classes will be used in constructing plot but play no other role
        # use fnIsDrugInAnyClass one drug at a time
        #   returns None if not in a class
        #
        # get food interactions amongst listDrugPicked
        # use dfFoodX 
        dfDrugPicked = pd.DataFrame(listDrugPicked, columns=['identifier'])
    elif SCENARIO == "FB":
        # classes
        dfClassPicked = pd.DataFrame(listClassPicked, columns=['class'])
        #
        # drugs belonging to a class use dfAllDrugClassesLong
        # these are all the classes and their drugs
        # these compose the class node to drug nodes
        # class, name
        #
        dfDrugsOfInterest = dfClassPicked.join(
            dfAllDrugClassesLong.set_index('class'),
            how = "left",
            on = 'class'
        )
        #
        listDrugPicked = dfDrugsOfInterest['name'].to_list()
        # make sure there are no duplicates
        listDrugPicked = list(set(listDrugPicked))
        #
        # get food interactions amongst listDrugPicked
        # use dfFoodX 
        dfDrugPicked = pd.DataFrame(listDrugPicked, columns=['identifier'])
    else:
        sg.Popup("Must be passed either FA or FB but was " + SCENARIO)
        quit()
    #
    dictClassPicked = {}
    for _d in listDrugPicked:
        # returns None if not in a class
        # assumes in at most one class
        _x, _ = fnIsDrugInAnyClass(_d, dictAllDrugClasses)
        if _x is not None:
            dictClassPicked[_d] = _x
    #
    dfFoodInteractingDrugsIdent = dfFoodX.query(f'identifier in {listDrugPicked}')
    #
    # all this to gets lists of food interacting and non-interacting drugs
    if len(dfFoodInteractingDrugsIdent.index) == 0:
        listFoodInteractingDrugs = []
    else:
        listFoodInteractingDrugs = dfFoodInteractingDrugsIdent['identifier'].to_list()
        # make sure there are no duplicates
        listFoodInteractingDrugs = list(set(listFoodInteractingDrugs))
    #
    listFoodNonInteractingDrugs = list(set(listDrugPicked) - set(listFoodInteractingDrugs))
    #
    # get the digestCodes appropriate to each interacting drug
    # dfInteractingDrugsIdent holds that data
    # want a dictionary with drug as key associated with a list of foodDigestCodes
    # https://stackoverflow.com/questions/71577763/python-pandas-create-a-dictionary-from-a-dataframe-with-values-equal-to-a-list
    #
    if len(dfFoodInteractingDrugsIdent.index) == 0:
        dfFoodInteractingDrugs = pd.DataFrame()
    else:
        #
        dfFoodInteractingDrugs = dfFoodInteractingDrugsIdent[['identifier','foodDigestCode','foodInteraction','shortInteraction']].copy()
        # add foodDigestGroup, foodDigestAction
        dfFoodInteractingDrugs = dfFoodInteractingDrugs.join(dfFoodDigest.set_index('foodDigestCode'), on='foodDigestCode')
        # add foodDigestActionColor
        dfFoodInteractingDrugs['foodDigestActionColor'] = dfFoodInteractingDrugs['foodDigestAction'].map(dictFoodDigestActionColors)
        dfFoodInteractingDrugs = dfFoodInteractingDrugs[['identifier','foodDigestCode','foodDigestText','foodDigestGroup','foodDigestAction','foodDigestActionColor','foodInteraction','shortInteraction']]
    #
    return  dfFoodInteractingDrugs, listFoodInteractingDrugs, listFoodNonInteractingDrugs, dictClassPicked, dfDrugPicked

# ====================== A ===================

def fnPyvisScenarioA(
    Ga, testThisDrug, dictNodeImages, dictNodeColors, listClassPicked, dfDrugsOfInterest, dfInteractingDrugs, listInteractingDrugs, listNonInteractingDrugs, lenXline
):
    # A - taking one class; test against one drug

    # dfInteractingDrugs, listInteractingDrugs, testThisDrug globals
    #
    # nodes will be the 1) classes, 2) the drugs of interest, and 3) testThisDrug
    # classes and testThisDrug have pre-set colors class and testThisDrug
    # colors of the drugs of interest nodes will be either safeDrug or unsafeDrug
    #   depending on whether there are interactions with testThisDrug

    # testThisDrug is a separate entity and has to be handled separately

    # add one node for the test drug
    # edges will be supplied later
    Ga.add_node(
        testThisDrug, 
        shape = 'image',
        image = dictNodeImages['testThisDrug']
    )
    # in order to get the drug-class connections do one class at a time
    # however, there are two "kinds" of drugs that belong to a class:
    # those that are in listInteractingDrugs, and those that are in listNonInteractingDrugs
    # (or not in listInteractingDrugs, which should be the same)
    # color should be different for these two sets of drugs
    #
    for _c in listClassPicked:
        # drug nodes:
        listDrugsForClass = dfDrugsOfInterest.loc[dfDrugsOfInterest['class'] == _c, 'name'].to_list()
        # is testThisDrug in the class?
        # might sometime be in more than one class
        if testThisDrug in listDrugsForClass:
            Ga.add_edge(
                _c,
                testThisDrug
            )
        for _d in listDrugsForClass:
            if _d in listInteractingDrugs:
                Ga.add_node(
                    _d,
                    shape = 'image',
                    image = dictNodeImages['unsafeDrug']
                    #color = dictNodeColors['unsafeDrug']
                )
            else:
                Ga.add_node(
                    _d,
                    shape = 'image',
                    image = dictNodeImages['safeDrug']
                    #color = dictNodeColors['safeDrug']
                )
        if '_d' in locals(): del _d
    if '_c' in locals(): del _c
    # interacting drugs edges from testThisDrug
    # nothing happens if listInteractingDrugs is empty
    listEdges = []
    for _d in listInteractingDrugs:
        _from_drug = _d
        _to_drug = testThisDrug
        # https://stackoverflow.com/questions/16729574/how-can-i-get-a-value-from-a-cell-of-a-dataframe
        # NOT ONLY THAT BUT MUST COERCE numpy integer to int AND reset index of dfRet
        _dfRet = dfInteractingDrugs.query(F"name == '{_from_drug}' and identifier == '{_to_drug}'")
        _dfRet.reset_index(inplace=True)
        if len(_dfRet.index) != 1:
            print("fnPyvisScenarioC error")
            quit()
        _descrip = _dfRet.at[0, 'description']
        _fold = fnFoldTextItem(_descrip, lenXline)
        _weight = int(_dfRet.at[0,'weight'])
        if [_to_drug, _from_drug, _descrip] in listEdges or [_from_drug, _to_drug, _descrip] in listEdges:
            pass
        else:
            listEdges.append([_from_drug, _to_drug, _descrip])
            Ga.add_edge(
                _from_drug,
                _to_drug,
                width = _weight,
                title = _fold
            )
    if '_d' in locals(): del _d
    #    
    # drugs that do not interact with testThisDrug
    # only need names of non-interacting drugs
    for _d in listNonInteractingDrugs:
        Ga.add_node(
            _d,
            shape = 'image',
            image = dictNodeImages['safeDrug']
        )
    if '_d' in locals(): del _d
    #
    return Ga

# ================ B ===========================

def fnPyvisScenarioB(
    Gb, listInteractingDrugs, listNonInteractingDrugs, dictClassPicked, dictAllDrugClasses, dfInteractingDrugs, dictNodeColors, dictNodeImages, dictNodeShapes, lenXline
):
    # B - taking several drugs; test for interactions

    # dfInteractingDrugs, listInteractingDrugs, listNonInteractingDrugs, dictClassPicked globals
    #
    # nodes will be the classes, and the drugs of interest
    # classes and testThisDrug have pre-set colors class and testThisDrug
    # colors of the drugs of interest nodes will be either safeDrug or unsafeDrug
    #   depending on whether there are interactions with testThisDrug

    # add nodes for drugs of interest
    # edges will be supplied later
    #image=[dictNodeImages['testThisDrugSafe']] * len(listInteractingDrugs)
    for _key in listInteractingDrugs:
        Gb.add_node(
            _key,
            shape = 'image',
            image = dictNodeImages['testThisDrugUnsafe']
        )
    if '_key' in locals(): del _key
    #for _key in listNonInteractingDrugs:
    #    Gb.add_node(
    #        _key,
    #        shape = 'image',
    #        image = dictNodeImages['testThisDrugSafe']
    #    )
    #if '_key' in locals(): del _key

    for _i, _val in enumerate(listNonInteractingDrugs):
        Gb.add_node(
            _val, 
            shape = 'image',
            image = dictNodeImages['safeDrug']
        )
    if '_i' in locals(): del _i


    #
    if bool(dictClassPicked):
        # key is drug
        for _key in dictClassPicked:
            # class is dictClassPicked[key]
            _Class = dictClassPicked[_key]
            Gb.add_node(
                _Class, 
                label = f"Class\n{_Class}\n{dictAllDrugClasses[_Class]['desc']}",
                color = dictNodeColors['class'],
                shape = dictNodeShapes['class']
            )
            Gb.add_edge(
                dictClassPicked[_key],
                _key
            )
        if '_key' in locals(): del _key
    # interacting drugs edges from dfInteractingDrugs
    dfInteractingDrugs.reset_index(drop=True, inplace=True)
    listEdges = [] # list of lists of the edge from-to pairs
    # avoid redundant edges by checking to see if reverse has been added
    for _idx in dfInteractingDrugs.index:
        _from_drug = dfInteractingDrugs['identifier'][_idx]
        _to_drug = dfInteractingDrugs['name'][_idx]
        _dfRet = dfInteractingDrugs.query(F"name == '{_from_drug}' and identifier == '{_to_drug}'")
        _dfRet.reset_index(inplace=True)
        if len(_dfRet.index) != 1:
            print("fnPyvisScenarioB error")
            quit()
        _descrip = _dfRet.at[0, 'description']
        _fold = fnFoldTextItem(_descrip, lenXline)
        _weight = int(_dfRet.at[0,'weight'])
        #skip if edge already there
        if [_to_drug, _from_drug, _descrip] in listEdges or [_from_drug, _to_drug, _descrip] in listEdges:
            pass
        else:
            # listEdges.append([from_drug,to_drug,digest])
            listEdges.append([_from_drug, _to_drug, _descrip])
            Gb.add_edge(
                _from_drug,
                _to_drug,
                width = _weight, 
                title = _fold
            )
    #    
    return Gb

# ======================= C ==========================

def fnPyvisScenarioC(Gc, listClassPicked, dictAllDrugClasses, listInteractingDrugs, dfInteractingDrugs, dfDrugsOfInterest,  dictNodeShapes, dictNodeColors, lenXline):
    
    # C - taking several classes; test amongst themselves

    # listClassPicked, dfDrugsOfInterest, dfInteractingDrugs, listInteractingDrugs, listNonInteractingDrugs globals
    # dfInteractingDrugs contains class_name and class_identifier
    #
    # nodes will be the 1) classes, and 2) the drugs that belong to them
    # classes and testThisDrug have pre-set colors class and testThisDrug
    # colors of the drugs of interest nodes will be either safeDrug or unsafeDrug
    #   depending on whether there are interactions 

    # in order to get the drug-class connections do one class at a time
    # however, there are two "kinds" of drugs that belong to a class:
    # those that are in listInteractingDrugs, and those that are in listNonInteractingDrugs
    # (or not in listInteractingDrugs, which should be the same)
    # color should be different for these two sets of drugs
    #
    count_class = 0
    for _c in listClassPicked:
        count_class += 1
        if count_class == 1:
            node_shape = dictNodeShapes['classDrug1']
        else:
            node_shape = dictNodeShapes['classDrug2']
        # class node
        Gc.add_node(
            _c,
            label = f"Class\n{_c}\n{dictAllDrugClasses[_c]['desc']}",
            color = dictNodeColors['class'],
            shape = dictNodeShapes['class']
        )
        # drug nodes:
        listDrugsForClass = dfDrugsOfInterest.loc[dfDrugsOfInterest['class'] == _c, 'name'].to_list()
        # only two classes are permitted
        for _d in listDrugsForClass:
            if _d in listInteractingDrugs:
                Gc.add_node(
                    _d,
                    color = dictNodeColors['unsafeDrug'],
                    shape = node_shape
                )
            else:
                Gc.add_node(
                    _d,
                    color = dictNodeColors['safeDrug'],
                    shape = node_shape
                )
            # add edges one drug at a time
            Gc.add_edge(
                _c, 
                _d
            )
        if '_d' in locals(): del _d
    if '_c' in locals(): del _c
    # interacting drugs edges
    # sort dfInteractingDrugs
    #
    # interacting drugs edges from dfInteractingDrugs
    dfInteractingDrugs.reset_index(drop=True, inplace=True)
    listEdges = [] # list of lists of the edge from-to pairs
    # avoid redundant edges by checking to see if reverse has been added
    for _idx in dfInteractingDrugs.index:
        _from_drug = dfInteractingDrugs['identifier'][_idx]
        _to_drug = dfInteractingDrugs['name'][_idx]
        _dfRet = dfInteractingDrugs.query(F"name == '{_from_drug}' and identifier == '{_to_drug}'")
        _dfRet.reset_index(inplace=True)
        if len(_dfRet.index) != 1:
            print("fnPyvisScenarioC error")
            quit()
        _descrip = _dfRet.at[0, 'description']
        _fold = fnFoldTextItem(_descrip, lenXline)
        _weight = int(_dfRet.at[0,'weight'])
        #skip if edge already there
        if [_to_drug, _from_drug, _descrip] in listEdges or [_from_drug, _to_drug, _descrip] in listEdges:
            pass
        else:
            listEdges.append([_from_drug, _to_drug, _descrip])
            Gc.add_edge(
                _from_drug,
                _to_drug,
                width = _weight, 
                title = _fold
            )
    
    return Gc

# =============================== FX =========================

def fnPyvisScenarioFX(
    Gfx, SCENARIO, listFoodInteractingDrugs, listFoodNonInteractingDrugs, dictClassPicked, dictAllDrugClasses, dfFoodInteractingDrugs,
    dictNodeColors, dictNodeShapes, dictFoodDigestActionImages, dictFoodDigestGroupImages, lenXline, lenXfoodDigestText
):
    # NOT IN USE 20230117
    # FA and FB
    #
    # if SCENARIO is 'FB', DO NOT show the drug class node/edge
    #   since only one class picked
    #
    # issue of multiple edges between nodes:
    # https://github.com/WestHealth/pyvis/issues/51
    #
    # dfFoodInteractingDrugs, listFoodInteractingDrugs, listFoodNonInteractingDrugs, dictClassPicked globals
    # dfFoodDigest global: foodDigestText, foodDigestCode, foodDigestGroup, foodDigestAction (Avoid, Require, Safe)
    # Gfa is global
    #
    # nodes will be the classes, drugs of interest, foodDigestCodes, foodDigestGroups and foodDigestActions
    # foodDigestAction provides label to edge, shape to foodDigestCode node
    #
    # classes and testThisDrug have pre-set colors class and testThisDrug
    # colors of the drugs of interest nodes will be either safeDrug or unsafeDrug
    #   depending on whether there are interactions with testThisDrug
    #
    # add nodes for drugs of interest
    #
    Gfx.add_nodes(
        listFoodInteractingDrugs, 
        color = [dictNodeColors['testThisDrug']] * len(listFoodInteractingDrugs),
        shape = [dictNodeShapes['testThisDrug']] * len(listFoodInteractingDrugs)
    )
    Gfx.add_nodes(
        listFoodNonInteractingDrugs, 
        color = [dictNodeColors['safeDrug']] * len(listFoodNonInteractingDrugs),
        shape = [dictNodeShapes['safeDrug']] * len(listFoodNonInteractingDrugs)
    )
    # complete the core diagram:
    # drug classes
    if SCENARIO != 'FB':
        if bool(dictClassPicked):
            # key is drug
            for _key in dictClassPicked:
                # class is dictClassPicked[key]
                _Class = dictClassPicked[_key]
                Gfx.add_node(
                    _Class, 
                    label = f"Class\n{_Class}\n{dictAllDrugClasses[_Class]['desc']}",
                    color = dictNodeColors['class'],
                    shape = dictNodeShapes['class']
                )
                Gfx.add_edge(
                    dictClassPicked[_key],
                    _key
                )
            if '_key' in locals(): del _key
    #
    # foodDigestCodes
    # here is where things get complicated - narrow to only what are being used
    # foodDigestCodes belong to foodDigestGroups
    # show nodes for the Groups along with edge from Code to Group
    # first lay out the totality of foodDigestCode and foodDigestGroup nodes
    # then connect via edges
    #
    # the foodDigestCodes we care about are in the joined dfFoodInteractingDrugs and dfFoodDigest
    # color of foodDigestCode node depends on foodDigestAction associated with it
    # there are simpler ways to do this, but just want to get it to work! 10/26/22
    if not dfFoodInteractingDrugs.empty:
        _dfTmp = dfFoodInteractingDrugs.copy()
        # create local lists:
        _dfTmp1 = _dfTmp[['foodDigestCode','foodDigestText','foodDigestGroup','foodDigestAction','foodDigestActionColor']].drop_duplicates()
        _listDigestCode1 = _dfTmp1['foodDigestCode'].to_list() 
        _listDigestGroup1 = _dfTmp1['foodDigestGroup'].to_list() 
        _listDigestText1 = _dfTmp1['foodDigestText'].to_list()
        _listDigestAction1 = _dfTmp1['foodDigestAction'].to_list()
        #_listDigestActionColor1 = _dfTmp1['foodDigestActionColor'].to_list() 
        # foodDigestCode nodes
        for _i, _val in enumerate(_listDigestCode1):
            Gfx.add_node(
                _val,
                label=fnFoldTextItem(_listDigestText1[_i], lenXfoodDigestText),
                shape = 'image',
                image = dictFoodDigestActionImages[_listDigestAction1[_i]]
            )
        if '_i' in locals(): del _i
        # foodDigestGroup nodes
        for _i, _val in enumerate(_listDigestGroup1):
            Gfx.add_node(
                _val,
                label = _val,
                shape = 'image',
                image = dictFoodDigestGroupImages[_val]
            )
        if '_i' in locals(): del _i
        # foodDigestCode to foodDigestGroup edges
        for _index, _row in _dfTmp1.iterrows():
            Gfx.add_edge(
                _row['foodDigestCode'],
                _row['foodDigestGroup'],
                title = fnFoldTextItem(_row['foodDigestAction'], lenXfoodDigestText)
            )
        if '_i' in locals(): del _i
        #
        # identifier to foodDigestCode edges via _dfTmp
        #
        # there is no edge label property, neither is there a settable color
        # there is a weight and a value but only one can be used
        for _index, _row in _dfTmp.iterrows():
            Gfx.add_edge(
                _row['identifier'],
                _row['foodDigestCode'],
                title = fnFoldTextItem(_row['foodInteraction'], lenXline)
            )
        if '_index' in locals(): del _index
    #
    return Gfx
# =============================== FX =========================

def fnPyvisScenarioFXw(
    Gfx, SCENARIO, listFoodInteractingDrugs, listFoodNonInteractingDrugs, dictClassPicked, dictAllDrugClasses, dfFoodInteractingDrugs,
    dictNodeColors, dictNodeShapes, dictNodeImages, dictFoodDigestActionImages, lenXline, lenXfoodDigestText
):
    # does not use Food Digest Group (compare with fnPyvisScenarioFX)
    #
    # if SCENARIO is 'FB', DO NOT show the drug class node/edge
    #   since only one class picked
    #
    # issue of multiple edges between nodes:
    # https://github.com/WestHealth/pyvis/issues/51
    #
    # dfFoodInteractingDrugs, listFoodInteractingDrugs, listFoodNonInteractingDrugs, dictClassPicked globals
    # dfFoodDigest global: foodDigestText, foodDigestCode, foodDigestGroup, foodDigestAction (Avoid, Require, Safe)
    # Gfa is global
    #
    # nodes will be the classes, drugs of interest, foodDigestCodes, foodDigestGroups and foodDigestActions
    # foodDigestAction provides label to edge, shape to foodDigestCode node
    #
    # classes and testThisDrug have pre-set colors class and testThisDrug
    # colors of the drugs of interest nodes will be either safeDrug or unsafeDrug
    #   depending on whether there are interactions with testThisDrug
    #
    # add nodes for drugs of interest
    #
    Gfx.add_nodes(
        listFoodInteractingDrugs, 
        color = [dictNodeColors['testThisDrug']] * len(listFoodInteractingDrugs),
        shape = [dictNodeShapes['testThisDrug']] * len(listFoodInteractingDrugs)
    )
    for _i, _val in enumerate(listFoodNonInteractingDrugs):
        Gfx.add_node(
            _val, 
            color = dictNodeColors['safeDrug'],
            shape = 'image',
            image = dictNodeImages['safeDrug']
        )
    if '_i' in locals(): del _i
    # complete the core diagram:
    # drug classes
    if SCENARIO != 'FB':
        if bool(dictClassPicked):
            # key is drug
            for _key in dictClassPicked:
                # class is dictClassPicked[key]
                _Class = dictClassPicked[_key]
                Gfx.add_node(
                    _Class, 
                    label = f"Class\n{_Class}\n{dictAllDrugClasses[_Class]['desc']}",
                    color = dictNodeColors['class'],
                    shape = dictNodeShapes['class']
                )
                Gfx.add_edge(
                    dictClassPicked[_key],
                    _key
                )
            if '_key' in locals(): del _key
    #
    # foodDigestCodes
    # here is where things get complicated - narrow to only what are being used
    # foodDigestCodes belong to foodDigestGroups
    # show nodes for the Groups along with edge from Code to Group
    # first lay out the totality of foodDigestCode and foodDigestGroup nodes
    # then connect via edges
    #
    # the foodDigestCodes we care about are in the joined dfFoodInteractingDrugs and dfFoodDigest
    # color of foodDigestCode node depends on foodDigestAction associated with it
    # there are simpler ways to do this, but just want to get it to work! 10/26/22
    if not dfFoodInteractingDrugs.empty:
        _dfTmp = dfFoodInteractingDrugs.copy()
        # create local lists:
        _dfTmp1 = _dfTmp[['foodDigestCode','foodDigestText','foodDigestGroup','foodDigestAction','foodDigestActionColor']].drop_duplicates()
        _listDigestCode1 = _dfTmp1['foodDigestCode'].to_list() 
        _listDigestGroup1 = _dfTmp1['foodDigestGroup'].to_list() 
        _listDigestText1 = _dfTmp1['foodDigestText'].to_list()
        _listDigestAction1 = _dfTmp1['foodDigestAction'].to_list()
        #_listDigestActionColor1 = _dfTmp1['foodDigestActionColor'].to_list() 
        # foodDigestCode nodes
        for _i, _val in enumerate(_listDigestCode1):
            Gfx.add_node(
                _val,
                label=fnFoldTextItem(_listDigestText1[_i], lenXfoodDigestText),
                shape = 'image',
                image = dictFoodDigestActionImages[_listDigestAction1[_i]]
            )
        if '_i' in locals(): del _i
        '''
        # foodDigestGroup nodes
        for _i, _val in enumerate(_listDigestGroup1):
            Gfx.add_node(
                _val,
                label = _val,
                shape = 'image',
                image = dictFoodDigestGroupImages[_val]
            )
        if '_i' in locals(): del _i
        # foodDigestCode to foodDigestGroup edges
        for _index, _row in _dfTmp1.iterrows():
            Gfx.add_edge(
                _row['foodDigestCode'],
                _row['foodDigestGroup'],
                title = fnFoldTextItem(_row['foodDigestAction'], lenXfoodDigestText)
            )
        if '_i' in locals(): del _i
        '''
        #
        # identifier to foodDigestCode edges via _dfTmp
        #
        # there is no edge label property, neither is there a settable color
        # there is a weight and a value but only one can be used
        for _index, _row in _dfTmp.iterrows():
            Gfx.add_edge(
                _row['identifier'],
                _row['foodDigestCode'],
                title = fnFoldTextItem(_row['foodInteraction'], lenXline)
            )
        if '_index' in locals(): del _index
    #
    return Gfx
