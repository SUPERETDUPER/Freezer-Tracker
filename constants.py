'''
MIT License

Copyright (c) 2017 Martin Staadecker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import collections

COMPANY_COLOUR = "#EC2409"
SPACING_BETWEEN_BUTTONS = 40
BUTTON_PADDING_X = 10
BUTTON_PADDING_Y = 5
BUTTON_HEIGHT = 3
NAV_BUTTON_HEIGHT = 115
MAIN_CONTAINER_PADDING = 50
FONT_SMALL = ("TkDefaultFont", 20)
FONT = ("TkDefaultFont", 35)
FONT_LARGE = ("TkDefaultFont", 50)
FONT_HUGE = ("TkDefaultFont", 80)
meats = [("Chicken", ["Breast", "Wings", "Legs"]),
         ("Beef", ["Rib"]),
         ("Lamb", []),
         ("Bacon", []),
         ("Duck", []),
         ("Pork", []),
         ("Pork", []),
         ("Pork", []),
         ("Pork", []),
         ("Pork", []),
         ("Pork", []),
         ("Pork", [])]
imageNames = {"home": "ic_action_home.png",
              "back": "ic_action_undo.png",
              "power": "ic_action_io.png",
              "add": "ic_action_add.png",
              "remove": "ic_action_minus.png",
              "clock": "ic_action_clock.png",
              "arrowLeft": "ic_action_arrow_left.png",
              "tick": "ic_action_tick.png",
              "logo": "ic_logo.png",
              "eye": "ic_visibility_white_36pt_3x.png"
              }
DARK_COLOUR = "#B10000"
LIGHT_COLOUR = "#FF623A"
PROJECT_TITLE = "Freezer inventory"
PADDING_BUTTON_FRAME = 10
LENGTH_OF_BATCH_NUMBER = 5
idColumn = "Batch number"
timeColumn = "Time stamp"
typeColumn = "Type"
subtypeColumn = "Sub-type"
weightColumn = "Weight"
removedColumn = "Removed ?"
columns = collections.OrderedDict([(idColumn, 0),
                                   (timeColumn, 1),
                                   (typeColumn, 2),
                                   (subtypeColumn, 3),
                                   (weightColumn, 4),
                                   (removedColumn, 5)])
db_file_path = "freezer_inventory_database.xlsx"