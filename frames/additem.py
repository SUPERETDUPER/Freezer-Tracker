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

Frames dealing with adding items to the database.

Tracks the current selection through productInfo which gets reset when coming back to the frame.
"""
import tkinter as tk

import backend
import fileManager
import frames.baseframe
import frames.mainframes
import global_var
import helper

productInfo = [None, None, None]  # Tracks what the user has entered for the product

meats = None
mainMeats = []
gridSize = None


def setup_meat_list():
    global meats, gridSize, mainMeats
    meats = fileManager.get_meat_list()

    helper.add_other_to_meats(meats)

    gridSize = helper.generate_grid_size(helper.generate_number_of_items(meats))  # Size of the grid for the buttons

    for meat in meats:
        mainMeats.append(meat[0])


class ButtonMainFrame(frames.baseframe.ButtonFrame):  # Selection of type of meat
    def __init__(self, master):
        super().__init__(master, button_main_call)
        self.previousFrame = frames.mainframes.HomeFrame.__name__

        setup_meat_list()

    def setup_frame(self):  # Populate with meats
        global productInfo
        productInfo[0] = None

        self.populate(mainMeats, gridSize)  # Populate based on meat list


class ButtonSecondFrame(frames.baseframe.ButtonFrame):  # Select the sub type of meat
    def __init__(self, master):
        super().__init__(master, button_second_call)
        self.previousFrame = ButtonMainFrame.__name__

    def setup_frame(self):
        global productInfo
        productInfo[1] = None  # Reset product info

        self.populate(productInfo[0][1], gridSize)  # Populate based on first selection


class WeightFrame(frames.baseframe.EnterDataFrame):  # Frame to enter weight
    def __init__(self, master=None):
        super().__init__(master, submit_weight, allow_decimal=True, title="Item weight", unit="kg", max_digits=6)
        self.previousFrame = ButtonMainFrame.__name__


class ConfirmAdditionFrame(frames.baseframe.YesNoFrame):  # Frame to confirm input
    def __init__(self, master=None):
        super().__init__(master, title="Add the following item to freezer?", command_no=helper.get_container().go_home,
                         command_yes=add_product)
        self.previousFrame = WeightFrame.__name__

        self.rowFrame = None  # Frame where the data is displayed

    def set_row(self, row):
        self.rowFrame = frames.baseframe.RowFrame(self.get_container(), row)
        self.rowFrame.pack(expand=True, fill="both")  # Displays data row in container

    def reset_frame(self):
        super().reset_frame()
        self.rowFrame.destroy()  # Reset data row


class SuccessMessage(frames.baseframe.MessageFrame):  # Message displaying generated batch number
    previousFrame = frames.mainframes.HomeFrame.__name__

    def __init__(self, master):
        super().__init__(master, title="Batch number (copy on product)", button_title="Finish")


def button_main_call(index):  # Method called when main meat type selected
    global productInfo

    productInfo[0] = meats[index]  # Update tracker

    if (len(productInfo[0][1])) != 0:
        helper.get_container().show_frame(ButtonSecondFrame.__name__)  # If meat has sub meat go to sub meat page
    else:
        helper.get_container().show_frame(WeightFrame.__name__)  # Else go to enter weight page


def button_second_call(index):  # Method called when sub meat type selected
    global productInfo
    productInfo[1] = productInfo[0][1][index]  # Update tracker

    helper.get_container().show_frame(WeightFrame.__name__)  # Go to weight page


def submit_weight(weight_submitted):  # Method called when weight submitted
    global productInfo
    productInfo[2] = weight_submitted  # Update tracker with weight

    helper.get_container().show_frame(ConfirmAdditionFrame.__name__)  # Show confirmation page
    helper.get_container().get_frame(ConfirmAdditionFrame.__name__).set_row(
        create_row())  # Update GUI row to show selection


def add_product():  # Method called when confirmed object removal
    # Add product to database
    if productInfo[1] is None:
        batch_id = global_var.database.add_item(
            backend.Row(category=productInfo[0][0], weight=productInfo[2]))  # If product has no sub type
    else:
        batch_id = global_var.database.add_item(backend.Row(category=productInfo[0][0], subcategory=productInfo[1],
                                                            weight=productInfo[2]))  # If product has sub type

    if batch_id == -1:
        raise Exception("Could not add to database")

    helper.get_container().show_frame(SuccessMessage.__name__)  # Show success frame

    container = helper.get_container().get_frame(SuccessMessage.__name__).get_container()  # Container for batch number
    tk.Label(container, text=helper.format_batch(batch_id),
             font=global_var.FONT_HUGE).pack()  # Add batch number to container


def create_row():  # Creates a row object based on tracker
    return backend.Row(productInfo[0][0], productInfo[1], productInfo[2], None)
