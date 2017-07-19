import tkinter as tk

import constants
import globalvar
import helper


class Frame(tk.Frame):  # Base frame class building all pages of GUI
    previousFrame = None

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def setupFrame(self):  # Executed before moving page to top of stack
        print("Info : No setup defined " + self.__class__.__name__)

    def resetFrame(self):  # Executed when moving away from frame, raising a new frame
        print("Info : No reset defined " + self.__class__.__name__)


class EnterDataFrame(Frame):  # GUI to enter numbers
    def __init__(self, master, command, title=None, allow_decimal=None, max_digits=None, min_digits=1, unit=None,
                 format_as_batch=False):
        super().__init__(master)

        self.maxDigits = max_digits
        self.minDigits = min_digits
        self.unit = unit
        self.formatAsBatch = format_as_batch

        self.keypad = Keypad(self, self.keyPadChanged, allow_decimal=allow_decimal, max_digits=max_digits)

        self.keypad.pack(side="left", expand=False, fill="y")

        right_frame = tk.Frame(self,
                               padx=constants.BUTTON_PADDING_X)  # Frame containing title, value and confirm button
        right_frame.pack(side="left", expand=True, fill="both")

        message = tk.Label(right_frame, text=title, font=constants.FONT)  # Title
        message.pack(anchor="n")

        self.label = tk.Label(right_frame, font=constants.FONT_HUGE, text=unit)  # Value that gets updated from keypad
        self.label.pack(expand=True, anchor="e")

        self.confirm_button = helper.getButton(right_frame, text="Confirm", background="green",
                                               image=globalvar.images["tick"],
                                               command=lambda: command(self.keypad.getValue()),
                                               state="disabled")  # Confirm button
        self.confirm_button.pack(expand=True, fill="both")

    def resetFrame(self):

        # Reset keypad value tracker
        self.keypad.reset()

        self.updateLabel(self.keypad.getValue())

    def updateLabel(self, value):
        if self.unit is not None:
            value += " " + self.unit

        if self.formatAsBatch:
            value = helper.formatBatch(value)

        self.label.config(text=value)

    def keyPadChanged(self, value):  # Gets called when the keypad value changes

        # Update state of confirm button
        if self.maxDigits is None and self.minDigits <= len(value):
            self.makeConfirmActive()
        elif self.minDigits <= len(value) <= self.maxDigits:
            self.makeConfirmActive()
        else:
            self.makeConfirmDisabled()

        self.updateLabel(value)

    def makeConfirmActive(self):
        self.confirm_button.config(state="normal")

    def makeConfirmDisabled(self):
        self.confirm_button.config(state="disabled")


class Keypad(tk.Frame):  # Class that tracks keypad input
    def __init__(self, master, callback, max_digits, allow_decimal):
        super().__init__(master)

        self.maxDigits = max_digits
        self.callback = callback
        self.value = ""

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Create key pad buttons
        self.getKeypadButton(text="1", command=lambda: self.addDigit("1")).grid(row=0, column=0, sticky="news")
        self.getKeypadButton(text="2", command=lambda: self.addDigit("2")).grid(row=0, column=1, sticky="news")
        self.getKeypadButton(text="3", command=lambda: self.addDigit("3")).grid(row=0, column=2, sticky="news")
        self.getKeypadButton(text="4", command=lambda: self.addDigit("4")).grid(row=1, column=0, sticky="news")
        self.getKeypadButton(text="5", command=lambda: self.addDigit("5")).grid(row=1, column=1, sticky="news")
        self.getKeypadButton(text="6", command=lambda: self.addDigit("6")).grid(row=1, column=2, sticky="news")
        self.getKeypadButton(text="7", command=lambda: self.addDigit("7")).grid(row=2, column=0, sticky="news")
        self.getKeypadButton(text="8", command=lambda: self.addDigit("8")).grid(row=2, column=1, sticky="news")
        self.getKeypadButton(text="9", command=lambda: self.addDigit("9")).grid(row=2, column=2, sticky="news")
        self.getKeypadButton(text="0", command=lambda: self.addDigit("0")).grid(row=3, column=1, sticky="news")
        self.getKeypadButton(command=self.removeDigit, image=globalvar.images["arrowLeft"]) \
            .grid(row=3, column=2, sticky="news")

        if allow_decimal:
            self.getKeypadButton(text=".", command=lambda: self.addDigit(".")).grid(row=3, column=0, sticky="news")

    def getKeypadButton(self, command, image=None, text=None):
        return helper.getButton(self, text=text, font=constants.FONT_HUGE, padx=70, command=command, image=image)

    def addDigit(self, digit):
        if self.maxDigits is None or len(self.value) < self.maxDigits:  # If not passed max_digits add digit
            self.value += digit
            self.callback(self.value)

    def removeDigit(self):
        if len(self.value) > 0:  # If already not min remove digit
            self.value = self.value[0:len(self.value) - 1]
            self.callback(self.value)

    def getValue(self):
        if self.value == "":  # To avoid reading self.value[-1] when empty and getting error
            return self.value

        if self.value[-1] == ".":  # If last digit is . remove it
            return int(self.value[0:len(self.value) - 1])

        if self.value.isdigit():  # If we can we return an int
            return int(self.value)

        return float(self.value)  # Return number

    def reset(self):
        self.value = ""


class ButtonFrame(Frame):
    def __init__(self, master, command):
        super().__init__(master)

        self.buttonHolder = []  # Holds all the buttons in the frame
        self.command = command

    def populate(self, names, grid_size=None):

        if grid_size is None:
            grid_size = helper.generateGridSize(len(names))  # If grid size not specified compute it

        for row in range(grid_size):
            self.grid_rowconfigure(row, weight=1)
            self.grid_columnconfigure(row, weight=1)  # So that each row and column has weight 1

            for column in range(grid_size):

                index = row * grid_size + column  # Calculate index based on row and col

                if index < len(names):  # If button exists for index

                    self.buttonHolder.append(helper.getButton(self, font=constants.FONT, text=names[index],
                                                              command=lambda i=index: self.command(
                                                                  i)))  # Append button to holder

                    self.buttonHolder[index].grid(row=row, column=column, sticky="news",
                                                  padx=constants.PADDING_BUTTON_FRAME,
                                                  pady=constants.PADDING_BUTTON_FRAME)  # Place button on grid

    def resetFrame(self):
        for button in self.buttonHolder:
            button.destroy()
        self.buttonHolder = []  # Delete all buttons from grid


class TitleAndContainer(tk.Frame):  # Simple frame containing a title and a container
    def __init__(self, master, title=""):
        super().__init__(master)

        label = tk.Label(self, text=title, font=constants.FONT_LARGE)
        label.pack()

        self.container = tk.Frame(self)
        self.container.pack(fill="x", expand=True)

    def getContainer(self):  # Returns container
        return self.container


class YesNoFrame(Frame):  # Frame containing a title, container and yes and no buttons
    def __init__(self, master, title="", command_yes=None, command_no=None):
        super().__init__(master)

        self.message_frame = TitleAndContainer(self, title)  # Title and container
        self.message_frame.pack(fill="both", expand=True)

        button_frame = tk.Frame(self)  # Frame including buttons and spacer
        button_frame.pack(fill="x", expand=True)

        button_padding = 100

        helper.getButton(button_frame, text="No", command=command_no, height=constants.BUTTON_HEIGHT,
                         padx=button_padding) \
            .grid(row=0, column=0)  # No Button
        button_frame.grid_columnconfigure(0, weight=1)

        tk.Frame(button_frame, width=constants.SPACING_BETWEEN_BUTTONS).grid(row=0, column=1)  # Spacer

        helper.getButton(button_frame, text="Yes", command=command_yes, background=constants.LIGHT_COLOUR,
                         padx=button_padding,
                         height=constants.BUTTON_HEIGHT).grid(row=0, column=2)  # Yes Button
        button_frame.grid_columnconfigure(2, weight=1)

    def getContainer(self):
        return self.message_frame.getContainer()


class MessageFrame(Frame):  # Frame displaying title, container and (home) button
    def __init__(self, master, title="", button_title="Home", command=lambda: helper.getMaster().goHome()):
        super().__init__(master)

        self.message_frame = TitleAndContainer(self, title)
        self.message_frame.pack(fill="both", expand=True)

        helper.getButton(self, text=button_title, command=command, height=3, width=10).pack()  # (Home) Button

    def getContainer(self):
        return self.message_frame.getContainer()
