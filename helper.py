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

Helper methods for the project

"""
import os
import tkinter as tk
from math import ceil

import constants
import globalvar

import datetime


def get_button(master, font=constants.FONT, padx=constants.BUTTON_PADDING_X, pady=constants.BUTTON_PADDING_Y,
               foreground="white",
               background=constants.COMPANY_COLOUR,
               compound="top", borderwidth=3, **args):
    # Returns a button to keep constant formatting across the project, especially color
    return tk.Button(master, font=font, padx=padx, pady=pady, foreground=foreground, background=background,
                     compound=compound, borderwidth=borderwidth, **args)


def turn_off():
    globalvar.app.destroy()  # Quit project


def generate_number_of_items():
    max_len = len(constants.meats)

    for index in range(len(constants.meats)):
        if len(constants.meats[index][1]) > max_len:
            max_len = len(constants.meats[index][1])

    return max_len


def generate_grid_size(num_of_items):  # Generate optimal grid side length based on number of items
    return int(ceil(num_of_items ** (1 / 2)))


def add_other_to_meats():  # Add the "Other" option to meat cuts
    for meat in constants.meats:
        if len(meat[1]) != 0:
            meat[1].append("Other")
    constants.meats.append(("Other", []))


def create_images():  # Creates the images and assigns them to the global variable images.
    for image in constants.imageNames.keys():
        try:
            globalvar.images[image] = tk.PhotoImage(file="res/" + constants.imageNames[image][0]).subsample(constants.imageNames[image][1])
        except tk.TclError:
            print("No image :" + image)


def get_master():  # Return the container for the frames
    return globalvar.app.mainContainer


def format_batch(batch):  # Formats a 5 digit batch number in the form 10 000
    batch = str(batch)

    if len(batch) > 2:
        return batch[0:2] + " " + batch[2:len(batch)]

    return batch.strip()


def view_in_excel():  # Opens the database in excel
    os.system("start " + constants.db_file_path)


def get_current_date():
    return '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())
