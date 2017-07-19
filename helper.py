import datetime
import tkinter as tk
from math import ceil

import constants
import globalvar


# Helper methods
def getButton(master, font=constants.FONT, padx=constants.BUTTON_PADDING_X, pady=constants.BUTTON_PADDING_Y,
              foreground="white",
              background=constants.COMPANY_COLOUR,
              compound="top", borderwidth=3, **args):
    return tk.Button(master, font=font, padx=padx, pady=pady, foreground=foreground, background=background,
                     compound=compound, borderwidth=borderwidth, **args)


def turnOff():
    globalvar.app.destroy()


def generateGridSize(num_of_items):
    return int(ceil(num_of_items ** (1 / 2)))


def addOtherToMeats():
    for meat in constants.meats:
        if len(meat[1]) != 0:
            meat[1].append("Other")
    constants.meats.append(("Other", []))


def createImages():
    for image in constants.imageNames.keys():
        try:
            globalvar.images[image] = tk.PhotoImage(file=constants.imageNames[image])
        except tk.TclError:
            print("No image :" +image)


def getMaster():
    return globalvar.app.mainContainer


def formatBatch(batch):
    batch = str(batch)

    if len(batch) > 2:
        return batch[0:2] + " " + batch[2:len(batch)]

    return batch.strip()


class Row:
    def __init__(self, category, subcategory, weight, batch_number, entry_date=None):
        self.category = category
        self.subcategory = subcategory
        self.weight = weight
        self.batch_number = batch_number
        if entry_date is None:
            entry_date = '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())
        self.entry_date = entry_date
        self.container = None

    def getLabel(self, **kwargs):
        return tk.Label(self.container, font=constants.FONT, relief="groove", borderwidth=2, **kwargs)

    def getLabelTitle(self, **kwargs):
        return tk.Label(self.container, font=constants.FONT, relief="groove", borderwidth=2, **kwargs)

    def getRowFrame(self, master=None):
        self.container = tk.Frame(master)

        self.getLabelTitle(text="Batch number").grid(row=0, column=0, sticky="we")
        self.container.grid_columnconfigure(0, weight=1)

        self.getLabelTitle(text="Entry Date").grid(row=0, column=1, sticky="we")
        self.container.grid_columnconfigure(1, weight=1)

        self.getLabelTitle(text="Type").grid(row=0, column=2, sticky="we")
        self.container.grid_columnconfigure(2, weight=1)

        self.getLabelTitle(text="Sub-type").grid(row=0, column=3, sticky="we")
        self.container.grid_columnconfigure(3, weight=1)

        self.getLabelTitle(text="Weight").grid(row=0, column=4, sticky="we")
        self.container.grid_columnconfigure(4, weight=1)

        if self.batch_number is not None:
            self.getLabel(text=formatBatch(self.batch_number)).grid(row=1, column=0, sticky="we")
        else:
            self.getLabel(text="---").grid(row=1, column=0, sticky="we")

        self.getLabel(text=self.entry_date).grid(row=1, column=1, sticky="we")
        self.getLabel(text=self.category).grid(row=1, column=2, sticky="we")

        if self.subcategory is not None:
            self.getLabel(text=self.subcategory).grid(row=1, column=3, sticky="we")
        else:
            self.getLabel(text="---").grid(row=1, column=3, sticky="we")

        self.getLabel(text=str(self.weight) + " kg").grid(row=1, column=4, sticky="we")

        return self.container
