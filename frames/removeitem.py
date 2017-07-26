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

Frames for removing item from database
"""
import tkinter as tk

import frames.baseframe
import frames.mainframes
import global_var
import helper

idNumber = None


class RemoveItemFrame(frames.baseframe.EnterDataFrame):  # Key pad to enter batch number
    def __init__(self, master):
        super().__init__(master, submit_batch_number, title="Item Number", max_digits=global_var.LENGTH_OF_BATCH_NUMBER,
                         min_digits=global_var.LENGTH_OF_BATCH_NUMBER, format_as_batch=True)
        self.previousFrame = frames.mainframes.HomeFrame.__name__


class ItemInfoFrame(frames.baseframe.YesNoFrame):  # Frame displaying item to remove
    def __init__(self, master=None):
        super().__init__(master, title="Remove the following item", command_no=helper.get_container().go_home,
                         command_yes=lambda: remove_item(idNumber))
        self.previousFrame = RemoveItemFrame.__name__

        self.rowFrame = None

    def set_row(self, row):
        self.rowFrame = frames.baseframe.RowFrame(self.get_container(), row)
        self.rowFrame.pack(expand=True, fill="both")  # Displays row info in container

    def reset_frame(self):
        super().reset_frame()
        self.rowFrame.destroy()  # Reset row


class SuccessRemoveFrame(frames.baseframe.MessageFrame):  # Frame showing item successfully removed
    def __init__(self, master):
        super().__init__(master, title="Successfully removed item : ")
        self.previousFrame = frames.mainframes.HomeFrame.__name__


class NoItemFrame(frames.baseframe.MessageFrame):  # Frame showing the batch number does not correspond
    def __init__(self, master):
        super().__init__(master, title="No such product")


class AlreadyRemovedFrame(frames.baseframe.MessageFrame):  # Frame showing the batch number does not correspond
    def __init__(self, master):
        super().__init__(master, title="Product already removed")


def submit_batch_number(number):
    global idNumber
    idNumber = number

    row = global_var.database.get_info(number)  # Get row object for batch number

    if row == global_var.ERROR_NO_SUCH_ITEM:
        helper.get_container().show_frame(NoItemFrame.__name__)  # If no such row show no item frame
    elif row == global_var.ERROR_ITEM_REMOVED:
        helper.get_container().show_frame(AlreadyRemovedFrame.__name__)  # If row already removed show frame
    else:
        helper.get_container().show_frame(ItemInfoFrame.__name__)  # Else show confirm frame
        helper.get_container().get_frame(ItemInfoFrame.__name__).set_row(row)  # And display data


def remove_item(batch_number):  # Called when asked to remove item
    result = global_var.database.remove_item(batch_number)  # Remove item from db

    if result:  # If success
        helper.get_container().show_frame(SuccessRemoveFrame.__name__)
        container = helper.get_container().get_frame(SuccessRemoveFrame.__name__).get_container()  # Show success frame
        tk.Label(container, text=helper.format_batch(batch_number),
                 font=global_var.FONT_HUGE).pack()  # Add label with product number
    else:
        raise (Exception("Unable to complete database operation"))  # If failed raise Exception
