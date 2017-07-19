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
import tkinter as tk

import constants
import frames.baseframe
import frames.mainframes
import globalvar
import helper

idNumber = None


class RemoveItemFrame(frames.baseframe.EnterDataFrame):
    def __init__(self, master):
        super().__init__(master, submit_batch_number, title="Item Number", max_digits=constants.LENGTH_OF_BATCH_NUMBER,
                         min_digits=constants.LENGTH_OF_BATCH_NUMBER, format_as_batch=True)
        self.previousFrame = frames.mainframes.HomeFrame.__name__


class ItemInfoFrame(frames.baseframe.YesNoFrame):  # Frame displaying item to remove
    def __init__(self, master=None):
        super().__init__(master, title="Remove the following item", command_no=helper.get_master().go_home,
                         command_yes=lambda: remove_item(idNumber))
        self.previousFrame = RemoveItemFrame.__name__

        self.rowFrame = None

    def set_row(self, row):
        self.rowFrame = frames.baseframe.RowFrame(self.get_container(), row)
        self.rowFrame.pack(expand=True, fill="both")  # Displays row info in container

    def reset_frame(self):
        super().reset_frame()
        self.rowFrame.destroy()  # Reset row


class SuccessRemoveFrame(frames.baseframe.MessageFrame):
    def __init__(self, master):
        super().__init__(master, title="Successfully removed item : ")
        self.previousFrame = frames.mainframes.HomeFrame.__name__


class NoItemFrame(frames.baseframe.MessageFrame):
    def __init__(self, master):
        super().__init__(master, title="No such product")


def submit_batch_number(number):
    global idNumber

    idNumber = number

    row = globalvar.database.get_info(number)

    if row is False:
        helper.get_master().show_frame(NoItemFrame.__name__)
    else:
        helper.get_master().show_frame(ItemInfoFrame.__name__)
        helper.get_master().get_frame(ItemInfoFrame.__name__).set_row(row)


def remove_item(batch_number):
    result = globalvar.database.remove_item(batch_number)

    if result:
        helper.get_master().show_frame(SuccessRemoveFrame.__name__)
        container = helper.get_master().get_frame(SuccessRemoveFrame.__name__).get_container()
        tk.Label(container, text=helper.format_batch(batch_number), font=constants.FONT_HUGE).pack()
    else:
        raise (Exception("No such product in database"))
