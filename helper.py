import tkinter as tk
from math import ceil

import constants
import globalvar


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
