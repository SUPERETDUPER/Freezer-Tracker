#!/usr/bin/python3
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

import frames.additem
import frames.mainframes
import frames.removeitem
import global_var
import helper


# Main Frame containing everything
class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.mainContainer = None  # Main container of frames

    def setup(self):
        # Expand horizontally and make middle large
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.get_header().grid(row=0, column=0, sticky="news")  # Creates header

        self.mainContainer = MainContainer(self)
        self.mainContainer.grid(row=1, column=0, sticky="news")
        self.mainContainer.setup()  # Builds all frames

        NavToolbar(self).grid(row=2, column=0, sticky="news")  # Builds nav toolbar

    def get_header(self):
        header = tk.Frame(self, background=global_var.COMPANY_COLOUR, height=100)
        if "logo" in global_var.images:
            tk.Label(header, image=global_var.images["logo"], borderwidth=0).pack()
        return header


class MainContainer(tk.Frame):
    previousFrame = None
    currentFrame = None

    homeFrame = frames.mainframes.HomeFrame.__name__
    startupFrame = frames.mainframes.HomeFrame.__name__

    frameHolder = {}

    all_frames = (
        frames.mainframes.HomeFrame, frames.mainframes.TurnOffFrame,
        frames.removeitem.RemoveItemFrame, frames.removeitem.SuccessRemoveFrame, frames.removeitem.ItemInfoFrame,
        frames.removeitem.NoItemFrame, frames.removeitem.AlreadyRemovedFrame,
        frames.additem.ButtonMainFrame, frames.additem.ButtonSecondFrame, frames.additem.WeightFrame,
        frames.additem.SuccessMessage,
        frames.additem.ConfirmAdditionFrame)  # List of Interchangeable frames

    def __init__(self, master):
        super().__init__(master, padx=global_var.MAIN_CONTAINER_PADDING, pady=global_var.MAIN_CONTAINER_PADDING)

    def setup(self):
        # Using grid to stack frames in same plane
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create and add to frames dict
        for frame in self.all_frames:
            self.frameHolder[frame.__name__] = frame(self)
            self.frameHolder[frame.__name__].grid(row=0, column=0, sticky="news")

        self.show_frame(self.startupFrame)  # Raise starting frame

    def show_frame(self, frame_name):
        self.previousFrame = self.currentFrame
        self.currentFrame = frame_name

        if self.previousFrame is not None:
            self.frameHolder[self.previousFrame].reset_frame()  # Reset the frame you're done with

        self.frameHolder[self.currentFrame].setup_frame()  # Setup the new frame

        self.frameHolder[frame_name].tkraise()  # Raise frame

    def go_home(self):
        self.show_frame(self.homeFrame)

    def get_up_frame(self):
        if self.currentFrame is not None:
            if self.frameHolder[self.currentFrame].previousFrame is None:
                return self.previousFrame  # If no previous frame defined use previous frame by time
            else:
                return self.frameHolder[self.currentFrame].previousFrame  # Else use defined previous frame

    def go_up(self):
        self.show_frame(self.get_up_frame())

    def get_frame(self, frame_name):
        return self.frameHolder[frame_name]  # Returns the requested frame


class NavToolbar(tk.Frame):  # Toolbar at the bottom of the page
    def __init__(self, master=None):
        super().__init__(master)

        self.add_button_to_frame(helper.get_master().go_up, global_var.images["back"])  # Back button

        self.add_button_to_frame(helper.get_master().go_home, global_var.images["home"])  # Home button

        self.add_button_to_frame(
            lambda: helper.get_master().show_frame(frame_name=frames.mainframes.TurnOffFrame.__name__),
            global_var.images["power"])

    def add_button_to_frame(self, command, image):
        helper.get_button(self, command=command, background=global_var.DARK_COLOUR,
                          image=image).pack(side='left', fill="x", expand=True)


if __name__ == "__main__":
    global_var.app = Application()  # Create app

    global_var.app.attributes('-fullscreen', True)  # Attributes
    global_var.app.title(global_var.PROJECT_TITLE)

    height = global_var.app.winfo_screenwidth()

    global_var.app.tk.call("tk", "scaling", height / 900)

    helper.create_images()

    global_var.app.setup()  # Create frames

    global_var.app.mainloop()  # Start GUI
