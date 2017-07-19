import tkinter as tk

import constants
import frames.additem
import frames.baseframe
import frames.removeitem
import globalvar
import helper


class HomeFrame(frames.baseframe.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.add_button_to_frame(text="Add new item",
                                 command=lambda: helper.get_master().show_frame(
                                     frames.additem.ButtonMainFrame.__name__),
                                 image=globalvar.images["add"], important=True, spacer=False)  # Add item button

        self.add_button_to_frame(text="Remove item",
                                 command=lambda: helper.get_master().show_frame(
                                     frames.removeitem.RemoveItemFrame.__name__),
                                 image=globalvar.images["remove"], important=True)  # Remove item button

        self.add_button_to_frame(text="View database in excel", command=None, image=None)  # View in excel button

    def add_button_to_frame(self, text, command, image, important=False, spacer=True):
        if spacer:
            tk.Frame(self, width=constants.SPACING_BETWEEN_BUTTONS).pack(side='left')  # If spacer required add spacer

        b = helper.get_button(self, text=text, command=command, image=image)

        if not important:
            b.config(font=constants.FONT_SMALL, background=constants.LIGHT_COLOUR)  # If not main change colour and size

        b.pack(side='left', fill="x", expand=True)


class TurnOffFrame(frames.baseframe.YesNoFrame):  # Frame for the power button
    def __init__(self, master):
        super().__init__(master, title="Are you sure you want to quit?", command_yes=helper.turn_off,
                         command_no=helper.get_master().go_up)
