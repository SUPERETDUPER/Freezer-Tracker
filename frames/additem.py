import tkinter as tk

import backend
import constants
import frames.baseframe
import frames.mainframes
import helper

productInfo = [None, None, None]  # Tracks what the user has entered for the product

gridSize = helper.generateGridSize(len(constants.meats))  # Size of the grid for the buttons


class ButtonMainFrame(frames.baseframe.ButtonFrame):  # Selection of type of meat
    def __init__(self, master):
        super().__init__(master, buttonMainCall)
        self.previousFrame = frames.mainframes.HomeFrame.__name__

    def setupFrame(self):  # Populate with meats
        global productInfo
        productInfo[0] = None

        meats_main = []  # List of only main types of meat created from full list

        for meat in constants.meats:
            meats_main.append(meat[0])

        self.populate(meats_main, gridSize)


class ButtonSecondFrame(frames.baseframe.ButtonFrame):  # Select the sub type of meat
    def __init__(self, master):
        super().__init__(master, buttonSecondCall)
        self.previousFrame = ButtonMainFrame.__name__

    def setupFrame(self):
        global productInfo
        productInfo[1] = None  # Reset product info

        self.populate(productInfo[0][1], gridSize)  # Populate based on first selection


class WeightFrame(frames.baseframe.EnterDataFrame):  # Frame to enter weight
    def __init__(self, master=None):
        super().__init__(master, submitWeight, allow_decimal=True, title="Item weight", unit="kg", max_digits=6)
        self.previousFrame = ButtonMainFrame.__name__


class ConfirmAdditionFrame(frames.baseframe.YesNoFrame):  # Frame to check input
    def __init__(self, master=None):
        super().__init__(master, title="Add the following item to freezer?", command_no=helper.getMaster().goHome,
                         command_yes=addProduct)
        self.previousFrame = WeightFrame.__name__

        self.rowFrame = None

    def setRow(self, row):
        self.rowFrame = row.getRowFrame(self.getContainer())
        self.rowFrame.pack(expand=True, fill="both")  # Displays row info in container

    def resetFrame(self):
        super().resetFrame()
        self.rowFrame.destroy()  # Reset row


class SuccessMessage(frames.baseframe.MessageFrame):  # Message displaying batch number
    previousFrame = frames.mainframes.HomeFrame.__name__

    def __init__(self, master):
        super().__init__(master, title="Batch number (copy on product)", button_title="Finish")


def buttonMainCall(index):
    global productInfo
    productInfo[0] = constants.meats[index]  # Update tracker

    if (len(productInfo[0][1])) != 0:
        helper.getMaster().show_frame(ButtonSecondFrame.__name__)  # If meat has sub meat go to syb meat page
    else:
        helper.getMaster().show_frame(WeightFrame.__name__)  # Else go to enter weight page


def buttonSecondCall(index):
    global productInfo
    productInfo[1] = productInfo[0][1][index]  # Update tracker

    helper.getMaster().show_frame(WeightFrame.__name__)  # Go to weight page


def submitWeight(weight_submitted):
    global productInfo
    productInfo[2] = weight_submitted  # Update tracker with weight

    helper.getMaster().show_frame(ConfirmAdditionFrame.__name__)  # Show confirmation page
    helper.getMaster().getFrame(ConfirmAdditionFrame.__name__).setRow(createRow())  # Update GUI row to show selection


def addProduct():  # Final call to add product to database
    # Add product to database
    if productInfo[1] is None:
        batch_id = backend.addItem(
            helper.Row(productInfo[0][0], None, productInfo[2], None))  # If product has no sub type
    else:
        batch_id = backend.addItem(
            helper.Row(productInfo[0][0], productInfo[1], productInfo[2], None))  # If product has sub type

    if batch_id == -1:
        raise Exception("Could not add to database")

    helper.getMaster().show_frame(SuccessMessage.__name__)  # Show success frame

    container = helper.getMaster().getFrame(SuccessMessage.__name__).getContainer()  # Container for batch number
    tk.Label(container, text=helper.formatBatch(batch_id),
             font=constants.FONT_HUGE).pack()  # Add batch number to container


def createRow():
    return helper.Row(productInfo[0][0], productInfo[1], productInfo[2], None)
