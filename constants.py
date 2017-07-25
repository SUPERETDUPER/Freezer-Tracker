"""
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
"""
import collections

COMPANY_COLOUR = "#EC2409"
SPACING_BETWEEN_BUTTONS = 40
BUTTON_PADDING_X = 10
BUTTON_PADDING_Y = 5
BUTTON_HEIGHT = 4
MAIN_CONTAINER_PADDING = 15

FONT = ("TkDefaultFont", 17)
FONT_LARGE = ("TkDefaultFont", 25)
FONT_HUGE = ("TkDefaultFont", 40)

meats = [("Turkey", ["Breast", "Thigh", "Skin", "Fine textured", "Scap", "MSM", "Dark trim", "White trim", "Fat"]),
         ("Chicken", ["Breast", "Thigh", "Skin", "Fine textured", "MSM", "Wings", "Drums", "Dark trim", "White trim"]),
         ("Pork",
          ["Backfat", "Ham fat", "Belly", "Whole Ham", "Picnic shoulder", "Shanks", "Skin", "Loin", "Tenderloin",
           "Hearts", "Jowls", "Fine textured"]),
         ("Beef",
          ["50/50 trim", "60/40 trim", "65/35 trim", "70/30 trim", "80/20 trim", "85/15 trim", "90/10 trim", "Chuck",
           "Eye of round", "Inside", "Outside", "Heart"])]

imageNames = {"home": ("ic_action_home.png", 2),
              "back": ("ic_action_undo.png", 2),
              "power": ("ic_action_io.png", 2),
              "add": ("ic_action_add.png", 2),
              "remove": ("ic_action_minus.png", 2),
              "clock": ("ic_action_clock.png", 1),
              "arrowLeft": ("ic_action_arrow_left.png", 1),
              "tick": ("ic_action_tick.png", 1),
              "logo": ("ic_logo.png", 3),
              "eye": ("ic_visibility_white_36pt_3x.png", 2)
              }

DARK_COLOUR = "#B10000"
LIGHT_COLOUR = "#FF623A"
PROJECT_TITLE = "Freezer Tracker"

PADDING_BUTTON_FRAME = 5
LENGTH_OF_BATCH_NUMBER = 5

idColumn = "Batch number"
timeColumn = "Time stamp"
typeColumn = "Type"
subtypeColumn = "Sub-type"
weightColumn = "Weight"
removedColumn = "Removed ?"
removedTimeColumn = "Removal time stamp"
columns = collections.OrderedDict([(idColumn, 0),
                                   (timeColumn, 1),
                                   (typeColumn, 2),
                                   (subtypeColumn, 3),
                                   (weightColumn, 4),
                                   (removedColumn, 5),
                                   (removedTimeColumn, 6)])

db_file_path = "freezer_inventory_database.xlsx"
ERROR_ITEM_REMOVED = 100
ERROR_NO_SUCH_ITEM = 101
