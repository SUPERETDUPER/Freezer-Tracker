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
import tkinter as tk
from math import ceil

import constants
import globalvar
import os
import backend


# Helper methods
def get_button(master, font=constants.FONT, padx=constants.BUTTON_PADDING_X, pady=constants.BUTTON_PADDING_Y,
               foreground="white",
               background=constants.COMPANY_COLOUR,
               compound="top", borderwidth=3, **args):
    return tk.Button(master, font=font, padx=padx, pady=pady, foreground=foreground, background=background,
                     compound=compound, borderwidth=borderwidth, **args)


def turn_off():
    globalvar.app.destroy()


def generate_grid_size(num_of_items):
    return int(ceil(num_of_items ** (1 / 2)))


def add_other_to_meats():
    for meat in constants.meats:
        if len(meat[1]) != 0:
            meat[1].append("Other")
    constants.meats.append(("Other", []))


def create_images():
    for image in constants.imageNames.keys():
        try:
            globalvar.images[image] = tk.PhotoImage(file=constants.imageNames[image])
        except tk.TclError:
            print("No image :" + image)


def get_master():
    return globalvar.app.mainContainer


def format_batch(batch):
    batch = str(batch)

    if len(batch) > 2:
        return batch[0:2] + " " + batch[2:len(batch)]

    return batch.strip()


def view_in_excel():
    os.system("start " + constants.db_file_path)