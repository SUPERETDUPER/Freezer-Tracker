import tkinter as tk

import backend
import constants
import frames.baseframe
import frames.mainframes
import globalvar
import helper

productInfo = [None, None, None]  # Tracks what the user has entered for the product

gridSize = helper.generate_grid_size(len(constants.meats))  # Size of the grid for the buttons


class ButtonMainFrame(frames.baseframe.ButtonFrame):  # Selection of type of meat
    def __init__(self, master):
        super().__init__(master, button_main_call)
        self.previousFrame = frames.mainframes.HomeFrame.__name__

    def setup_frame(self):  # Populate with meats
        global productInfo
        productInfo[0] = None

        meats_main = []  # List of only main types of meat created from full list

        for meat in constants.meats:
            meats_main.append(meat[0])

        self.populate(meats_main, gridSize)


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


class ConfirmAdditionFrame(frames.baseframe.YesNoFrame):  # Frame to check input
    def __init__(self, master=None):
        super().__init__(master, title="Add the following item to freezer?", command_no=helper.get_master().go_home,
                         command_yes=add_product)
        self.previousFrame = WeightFrame.__name__

        self.rowFrame = None

    def set_row(self, row):
        self.rowFrame = frames.baseframe.RowFrame(self.get_container(), row)
        self.rowFrame.pack(expand=True, fill="both")  # Displays row info in container

    def reset_frame(self):
        super().reset_frame()
        self.rowFrame.destroy()  # Reset row


class SuccessMessage(frames.baseframe.MessageFrame):  # Message displaying batch number
    previousFrame = frames.mainframes.HomeFrame.__name__

    def __init__(self, master):
        super().__init__(master, title="Batch number (copy on product)", button_title="Finish")


def button_main_call(index):
    global productInfo
    productInfo[0] = constants.meats[index]  # Update tracker

    if (len(productInfo[0][1])) != 0:
        helper.get_master().show_frame(ButtonSecondFrame.__name__)  # If meat has sub meat go to syb meat page
    else:
        helper.get_master().show_frame(WeightFrame.__name__)  # Else go to enter weight page


def button_second_call(index):
    global productInfo
    productInfo[1] = productInfo[0][1][index]  # Update tracker

    helper.get_master().show_frame(WeightFrame.__name__)  # Go to weight page


def submit_weight(weight_submitted):
    global productInfo
    productInfo[2] = weight_submitted  # Update tracker with weight

    helper.get_master().show_frame(ConfirmAdditionFrame.__name__)  # Show confirmation page
    helper.get_master().get_frame(ConfirmAdditionFrame.__name__).set_row(
        create_row())  # Update GUI row to show selection


def add_product():  # Final call to add product to database
    # Add product to database
    if productInfo[1] is None:
        batch_id = globalvar.database.add_item(
            backend.Row(productInfo[0][0], None, productInfo[2], None))  # If product has no sub type
    else:
        batch_id = globalvar.database.add_item(
            backend.Row(productInfo[0][0], productInfo[1], productInfo[2], None))  # If product has sub type

    if batch_id == -1:
        raise Exception("Could not add to database")

    helper.get_master().show_frame(SuccessMessage.__name__)  # Show success frame

    container = helper.get_master().get_frame(SuccessMessage.__name__).get_container()  # Container for batch number
    tk.Label(container, text=helper.format_batch(batch_id),
             font=constants.FONT_HUGE).pack()  # Add batch number to container


def create_row():
    return backend.Row(productInfo[0][0], productInfo[1], productInfo[2], None)
