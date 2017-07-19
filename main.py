import tkinter as tk

import constants
import frames.additem
import frames.mainframes
import frames.removeitem
import globalvar
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
        header = tk.Frame(self, background=constants.COMPANY_COLOUR, height=100)
        if "logo" in globalvar.images:
            tk.Label(header, image=globalvar.images["logo"], borderwidth=0).pack()
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
        frames.additem.ButtonMainFrame, frames.additem.ButtonSecondFrame, frames.additem.WeightFrame,
        frames.additem.SuccessMessage,
        frames.additem.ConfirmAdditionFrame)  # List of Interchangeable frames

    def __init__(self, master):
        super().__init__(master, padx=constants.MAIN_CONTAINER_PADDING, pady=constants.MAIN_CONTAINER_PADDING)

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

        self.add_button_to_frame(helper.get_master().go_up, globalvar.images["back"])  # Back button

        self.add_button_to_frame(helper.get_master().go_home, globalvar.images["home"])  # Home button

        self.add_button_to_frame(
            lambda: helper.get_master().show_frame(frame_name=frames.mainframes.TurnOffFrame.__name__),
            globalvar.images["power"])

    def add_button_to_frame(self, command, image):
        helper.get_button(self, command=command, background=constants.DARK_COLOUR, height=constants.NAV_BUTTON_HEIGHT,
                          image=image).pack(side='left', fill="x", expand=True)


if __name__ == "__main__":
    globalvar.app = Application()  # Create app

    globalvar.app.attributes('-fullscreen', True)  # Attributes
    globalvar.app.title(constants.PROJECT_TITLE)

    helper.create_images()
    helper.add_other_to_meats()

    globalvar.app.setup()  # Create frames

    globalvar.app.mainloop()  # Start GUI
