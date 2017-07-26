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

File containing helper frames and general purpose frames. Other frames are based of these frames.

All frames which act as windows should have as parent class Frame

"""
import tkinter as tk

import global_var
import helper


class Frame(tk.Frame):  # Base frame class building all pages of GUI
    previousFrame = None

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def setup_frame(self):  # Executed before moving page to top of stack
        pass

    def reset_frame(self):  # Executed when moving away from frame, raising a new frame
        pass


class EnterDataFrame(Frame):  # GUI to enter numbers
    def __init__(self, master, command, title=None, allow_decimal=None, max_digits=None, min_digits=1, unit=None,
                 format_as_batch=False):
        super().__init__(master, background="green")

        self.maxDigits = max_digits
        self.minDigits = min_digits
        self.unit = unit
        self.formatAsBatch = format_as_batch

        self.grid_rowconfigure(0, weight=1)

        self.keypad = Keypad(self, self.key_pad_changed, allow_decimal=allow_decimal, max_digits=max_digits)

        self.keypad.grid(row=0, column=0, sticky="news")
        self.grid_columnconfigure(0, weight=1)
        self.keypad.grid_propagate(0)

        right_frame = tk.Frame(self,
                               padx=global_var.BUTTON_PADDING_X)  # Frame containing title, value and confirm button
        right_frame.grid(row=0, column=1, sticky="news")
        self.grid_columnconfigure(1, weight=1)
        right_frame.pack_propagate(0)

        message = tk.Label(right_frame, text=title, font=global_var.FONT)  # Title
        message.pack(anchor="n")

        self.label = tk.Label(right_frame, font=global_var.FONT_HUGE, text=unit)  # Value that gets updated from keypad
        self.label.pack(expand=True, anchor="e")

        self.confirm_button = helper.get_button(right_frame, text="Confirm", background="green",
                                                image=global_var.images["tick"],
                                                command=lambda: command(self.keypad.get_value()),
                                                state="disabled")  # Confirm button
        self.confirm_button.pack(expand=True, fill="both")

    def reset_frame(self):

        # Reset keypad value tracker
        self.keypad.reset()

        self.update_label(self.keypad.get_value())

        self.make_confirm_disabled()

    def update_label(self, value):
        if self.unit is not None:
            value += " " + self.unit

        if self.formatAsBatch:
            value = helper.format_batch(value)

        self.label.config(text=value)

    def key_pad_changed(self, value):  # Gets called when the keypad value changes

        # Update state of confirm button
        if self.maxDigits is None and self.minDigits <= len(value):
            self.make_confirm_active()
        elif self.minDigits <= len(value) <= self.maxDigits:
            self.make_confirm_active()
        else:
            self.make_confirm_disabled()

        self.update_label(value)

    def make_confirm_active(self):
        self.confirm_button.config(state="normal")

    def make_confirm_disabled(self):
        self.confirm_button.config(state="disabled")


class Keypad(tk.Frame):  # Class that tracks keypad input
    def __init__(self, master, callback, max_digits, allow_decimal, **kwargs):
        super().__init__(master, **kwargs)

        self.maxDigits = max_digits
        self.callback = callback
        self.value = ""

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Create key pad buttons
        self.get_keypad_button(text="1", command=lambda: self.add_digit("1")).grid(row=0, column=0, sticky="news")
        self.get_keypad_button(text="2", command=lambda: self.add_digit("2")).grid(row=0, column=1, sticky="news")
        self.get_keypad_button(text="3", command=lambda: self.add_digit("3")).grid(row=0, column=2, sticky="news")
        self.get_keypad_button(text="4", command=lambda: self.add_digit("4")).grid(row=1, column=0, sticky="news")
        self.get_keypad_button(text="5", command=lambda: self.add_digit("5")).grid(row=1, column=1, sticky="news")
        self.get_keypad_button(text="6", command=lambda: self.add_digit("6")).grid(row=1, column=2, sticky="news")
        self.get_keypad_button(text="7", command=lambda: self.add_digit("7")).grid(row=2, column=0, sticky="news")
        self.get_keypad_button(text="8", command=lambda: self.add_digit("8")).grid(row=2, column=1, sticky="news")
        self.get_keypad_button(text="9", command=lambda: self.add_digit("9")).grid(row=2, column=2, sticky="news")
        self.get_keypad_button(text="0", command=lambda: self.add_digit("0")).grid(row=3, column=1, sticky="news")
        self.get_keypad_button(command=self.remove_digit, image=global_var.images["arrowLeft"]) \
            .grid(row=3, column=2, sticky="news")

        if allow_decimal:
            self.get_keypad_button(text=".", command=lambda: self.add_digit(".")).grid(row=3, column=0, sticky="news")

    def get_keypad_button(self, command, image=None, text=None):
        return helper.get_button(self, text=text, font=global_var.FONT_HUGE, padx=30, command=command, image=image)

    def add_digit(self, digit):
        if self.maxDigits is None or len(self.value) < self.maxDigits:  # If not passed max_digits add digit
            self.value += digit
            self.callback(self.value)

    def remove_digit(self):
        if len(self.value) > 0:  # If already not min remove digit
            self.value = self.value[0:len(self.value) - 1]
            self.callback(self.value)

    def get_value(self):
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
            grid_size = helper.generate_grid_size(len(names))  # If grid size not specified compute it

        for row in range(grid_size):
            self.grid_rowconfigure(row, weight=1)
            self.grid_columnconfigure(row, weight=1)  # So that each row and column has weight 1

            for column in range(grid_size):

                index = row * grid_size + column  # Calculate index based on row and col

                if index < len(names):  # If button exists for index

                    self.buttonHolder.append(helper.get_button(self, font=global_var.FONT, text=names[index],
                                                               command=lambda i=index: self.command(
                                                                   i)))  # Append button to holder

                    self.buttonHolder[index].grid(row=row, column=column, sticky="news",
                                                  padx=global_var.PADDING_BUTTON_FRAME,
                                                  pady=global_var.PADDING_BUTTON_FRAME)  # Place button on grid

    def reset_frame(self):
        for button in self.buttonHolder:
            button.destroy()
        self.buttonHolder = []  # Delete all buttons from grid


class TitleAndContainer(tk.Frame):  # Simple frame containing a title and a container
    def __init__(self, master, title=""):
        super().__init__(master)

        label = tk.Label(self, text=title, font=global_var.FONT_LARGE)
        label.pack()

        self.container = tk.Frame(self)
        self.container.pack(fill="x", expand=True)

    def get_container(self):  # Returns container
        return self.container

    def reset_container(self):
        for child in self.container.winfo_children():
            child.destroy()


class YesNoFrame(Frame):  # Frame containing a title, container and yes and no buttons
    def __init__(self, master, title="", command_yes=None, command_no=None):
        super().__init__(master)

        self.message_frame = TitleAndContainer(self, title)  # Title and container
        self.message_frame.pack(fill="both", expand=True)

        button_frame = tk.Frame(self)  # Frame including buttons and spacer
        button_frame.pack(fill="x", expand=True)

        button_padding = 100

        # No Button
        helper.get_button(button_frame, text="No", command=command_no, height=global_var.BUTTON_HEIGHT,
                          padx=button_padding) \
            .grid(row=0, column=0)
        button_frame.grid_columnconfigure(0, weight=1)

        tk.Frame(button_frame, width=global_var.SPACING_BETWEEN_BUTTONS).grid(row=0, column=1)  # Spacer

        # Yes Button
        helper.get_button(button_frame, text="Yes", command=command_yes, background=global_var.LIGHT_COLOUR,
                          padx=button_padding,
                          height=global_var.BUTTON_HEIGHT).grid(row=0, column=2)
        button_frame.grid_columnconfigure(2, weight=1)

    def get_container(self):
        return self.message_frame.get_container()

    def reset_frame(self):
        self.message_frame.reset_container()


class MessageFrame(Frame):  # Frame displaying title, container and (home) button
    def __init__(self, master, title="", button_title="Home", command=lambda: helper.get_container().go_home()):
        super().__init__(master)

        self.message_frame = TitleAndContainer(self, title)  # Title and container
        self.message_frame.pack(fill="both", expand=True)

        helper.get_button(self, text=button_title, command=command, height=3, width=10).pack()  # (Home) Button

    def get_container(self):
        return self.message_frame.get_container()

    def reset_frame(self):
        self.message_frame.reset_container()


class RowFrame(tk.Frame):  # Frame displaying a database row
    def __init__(self, master, row):
        super().__init__(master)

        for index, column in enumerate(global_var.columns):

            # Don't display the removed column or removed timestamp in database because it's not applicable
            if column == global_var.removedColumn or column == global_var.removedTimeColumn:
                continue

            # If batch number is not existent don't show it
            if column == global_var.idColumn and row.get_item(index) is None:
                continue

            # Header cell
            tk.Label(self, font=global_var.FONT, relief="groove", borderwidth=2, text=column).grid(
                row=0, column=index, sticky="we")
            self.grid_columnconfigure(index, weight=1)

            # Data cell
            if row.get_item(index) is not None:
                tk.Label(self, font=global_var.FONT, relief="groove", borderwidth=2,
                         text=str(row.get_item(index))).grid(
                    row=1, column=index, sticky="we")  # If has a value
            else:
                tk.Label(self, font=global_var.FONT, relief="groove", borderwidth=2, text="---").grid(
                    row=1, column=index, sticky="we")  # If no value replace with "---"
