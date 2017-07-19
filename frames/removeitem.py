import tkinter as tk

import backend
import constants
import frames.baseframe
import frames.mainframes
import helper

row_id = -1


class RemoveItemFrame(frames.baseframe.EnterDataFrame):
    def __init__(self, master):
        super().__init__(master, submitBatchNumber, title="Item Number", max_digits=constants.LENGTH_OF_BATCH_NUMBER,
                         min_digits=constants.LENGTH_OF_BATCH_NUMBER, format_as_batch=True)
        self.previousFrame = frames.mainframes.HomeFrame.__name__


class ItemInfoFrame(frames.baseframe.YesNoFrame):  # Frame displaying item to remove
    def __init__(self, master=None):
        super().__init__(master, title="Remove the following item", command_no=helper.getMaster().goHome,
                         command_yes=lambda: removeItem(row_id))
        self.previousFrame = RemoveItemFrame.__name__

        self.rowFrame = None

    def setRow(self, row):
        self.rowFrame = row.getRowFrame(self.getContainer())
        self.rowFrame.pack(expand=True, fill="both")  # Displays row info in container

    def resetFrame(self):
        super().resetFrame()
        self.rowFrame.destroy()  # Reset row


class SuccessRemoveFrame(frames.baseframe.MessageFrame):

    def __init__(self, master):
        super().__init__(master, title="Successfully removed item : ")
        self.previousFrame = frames.mainframes.HomeFrame.__name__


def removeItem(item_id):
    result = backend.removeItem(item_id)

    if result:
        helper.getMaster().show_frame(SuccessRemoveFrame.__name__)
        container = helper.getMaster().getFrame(SuccessRemoveFrame.__name__).getContainer()
        tk.Label(container, text=helper.formatBatch(item_id), font=constants.FONT_HUGE).pack()


def submitBatchNumber(number):
    global row_id
    row_id = number

    row = backend.getItemInfo(number)

    helper.getMaster().show_frame(ItemInfoFrame.__name__)
    helper.getMaster().getFrame(ItemInfoFrame.__name__).setRow(row)
