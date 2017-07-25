# Freezer Tracker

## Description

This project is a inventory management tool. It allows you to easily add, remove and track item's in a freezer or fridge.

It keeps track of the type, sub-type, weight, entry date and removal date of all items that went through the freezer.

This project was built to run on a raspberry pi with a 7'' touchscreen display.

## Technical details

The projects is built using Python. The GUI is built with the tkinter library and interaction with the excel database goes through the openpyxl library.

The `/res` folder contains all images to be loaded in the program.

The `/frames` folder contains the code for the different layouts and windows used in the GUI.

The `global_var.py` file contains all the constants. The `app` variable (the tkinter root). The `images` dictionary (holder for all Photoimage objects).

The `backend.py` file contains all backend methods to interact with the database (using openpyxl).

The `helper.py` file contains helper methods.

The `main.py` file is where the tkinter root and base layout structure is built.

### Tkinter structure

This projects contains several windows or pages. To manage this, the pages are stacked one on top of each other. To display a page, you raise the page to the top of the stack using :
`helper.getMaster().show_frame(CustomFrameToDisplay.__name__)`.

When raising a frame its `setup_frame()` method is called. The `reset_frame()` method is called on the frame you are leaving.

All frames specify a `previousFrame` instance variable. This indicates what the back button should do. If set to `None` the back button goes to the previous visited frame.

### Backend structure

The project uses the openpyxl library to read, write and update a generated excel file. The `backend.py` module is responsible for these tasks and has three main functions.

`add_item(Row)` : Adds a row to the database and returns its generated ID.

`remove_item(id)` : Change the value of the `Removed` column to `True` for the row with that id.

`get_info(id)` : Returns the row with the parameters id. May return a `NO_SUCH_ITEM` error code or a `ITEM_REMOVED` error code.

The `backend.py` file also defines a Row object for passing data around the application.

The project's master database is stored on the device locally (location depends on the `config.py` file). However, a copy of the database is automatically copied into a folder which could sync on the network. This folder is specified in the `config.py` file.

### Config file

The `config.py` file stores information that varies depending on the device and implementation.

It indicates where the local database should be stored (usually in the working directory). It indicates where on the network should the database be copied. It also provides the lists of products and sub categories for your database.
