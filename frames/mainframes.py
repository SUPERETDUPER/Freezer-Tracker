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

Contains Home frame and turn off frame

"""
import tkinter as tk

import constants
import frames.additem
import frames.baseframe
import frames.removeitem
import globalvar
import helper


class HomeFrame(frames.baseframe.Frame):  # Frame displayed at start
    def __init__(self, master=None):
        super().__init__(master)

        self.add_button_to_frame(text="Add new item",
                                 command=lambda: helper.get_master().show_frame(
                                     frames.additem.ButtonMainFrame.__name__),
                                 image=globalvar.images["add"], spacer=False)  # Add item button

        self.add_button_to_frame(text="Remove item",
                                 command=lambda: helper.get_master().show_frame(
                                     frames.removeitem.RemoveItemFrame.__name__),
                                 image=globalvar.images["remove"])  # Remove item button

        self.add_button_to_frame(text="View database in excel", image=globalvar.images["eye"],
                                 command=helper.view_in_excel)  # View in excel button

    def add_button_to_frame(self, text, command, image,  spacer=True):
        if spacer:
            tk.Frame(self, width=constants.SPACING_BETWEEN_BUTTONS).pack(side='left')  # If spacer required add spacer

        b = helper.get_button(self, text=text, command=command, image=image)
        b.pack(side='left', fill="x", expand=True)


class TurnOffFrame(frames.baseframe.YesNoFrame):  # Frame for the power button
    def __init__(self, master):
        super().__init__(master, title="Are you sure you want to quit?", command_yes=helper.turn_off,
                         command_no=helper.get_master().go_up)
