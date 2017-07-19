import tkinter as tk

import backend
import constants
import frames.baseframe
import frames.mainframes
import globalvar
import helper

selectedRow = None


class RemoveItemFrame(frames.baseframe.EnterDataFrame):
    def __init__(self, master):
        super().__init__(master, submit_batch_number, title="Item Number", max_digits=constants.LENGTH_OF_BATCH_NUMBER,
                         min_digits=constants.LENGTH_OF_BATCH_NUMBER, format_as_batch=True)
        self.previousFrame = frames.mainframes.HomeFrame.__name__


class ItemInfoFrame(frames.baseframe.YesNoFrame):  # Frame displaying item to remove
    def __init__(self, master=None):
        super().__init__(master, title="Remove the following item", command_no=helper.get_master().go_home,
                         command_yes=lambda: remove_item(selectedRow))
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


def submit_batch_number(number):
    global selectedRow

    selectedRow = globalvar.database.get_row(number)

    helper.get_master().show_frame(ItemInfoFrame.__name__)
    helper.get_master().get_frame(ItemInfoFrame.__name__).set_row(selectedRow)


def remove_item(row):
    result = globalvar.database.remove_item(row)

    if result:
        helper.get_master().show_frame(SuccessRemoveFrame.__name__)
        container = helper.get_master().get_frame(SuccessRemoveFrame.__name__).get_container()
        tk.Label(container, text=helper.format_batch(row.getRow()[backend.idColumn]), font=constants.FONT_HUGE).pack()
