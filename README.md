# Freezer Tracker

This project is a inventory management tool. It allows you to easily add, remove and track item's in a freezer.

It keeps track of the type, sub-type, weight, entry date and removal date of all items that went through the freezer.

Further more, this project can be setup to share the database on a network drive like a windows share drive.

This project was built for and run on a Raspberry Pi connected to the Raspberry Pi 7'' touchscreen display.

## First time setup

1. Download the code on your device.

2. Run `main.py` once. Nothing will happen but this will generate a `/local` folder.

3. Open `/local/local.conf` and change the value of `project_code` to whatever you want to name your project. If you are tracking data for several different freezer on the same server, this code needs to be unique.

4. Run `main.py`

#### Optional further setup

- Add your logo to `/res/img` under the name `ic_logo.png`

In `/local/local.conf`:

- To have your database synced across multiples computers via a network drive, edit `server_path` to point to your network drive (ex. Windows Share Drive).

- If you want the computer to shutdown when quiting the program, set `shutdown_on_quit` to `True`.

In `meat_list.json` : 

- Change the data to fit your needs. Make sure to keep the same JSON format!

## Technical details

The projects is built using Python.

The GUI is built with the tkinter library.

Interaction with the excel database goes through the openpyxl library.

ConfigParser is used for reading the local.conf file.

JSON is used for the list of meat types.

### Project structure

The `/frames` folder contains the code for the different layouts and windows used in the GUI. The `/frames/baseframe.py` file contains parent frames and basic frames to be customised by the other frame files.

The `/res` folder contains all resources. It contains the default files to create a local folder. It contains the `/res/img` folder containing all images.

The `/local` folder is a generated folder that contains the settings for that copy of the project. It is not tracked by Git.

The `backend.py` file contains all backend methods to interact with the database (using openpyxl).

The `fileManager.py` file reads and manages the `/local` folder. It also makes runs the network drive upload and backup operations.

The `global_var.py` file contains all the constants, the `app` variable (the tkinter root) and the `images` dictionary (holder for all Photoimage objects).

The `helper.py` file contains helper methods.

The `main.py` file is where the tkinter root and base layout structure is built.

### Tkinter structure

This projects contains several windows or pages. To manage this, the pages are stacked one on top of each other. To display a page, you raise the page to the top of the stack using :

`helper.getContainer().show_frame(FrameToDisplay.__name__)`.

When raising (displaying) a frame its `setup_frame()` method is called. The `reset_frame()` method is called on the frame you are leaving.

All frames specify a `previousFrame` instance variable. This indicates what the back button should do. If set to `None` the back button goes to the previous visited frame (chronologically).

### Backend structure

The project's master database is stored locally in the `/local` folder.

However, if configured, the database is automatically copied into your network drive when modified. This network drive can be any folder and it is specified in the `/local/local.conf` file.

The structure of the specified network drive is as follow.

`"Project code"` : A parent folder containing the data for that copy of the project. Useful if you have several projects that all need to be update in one network drive.

----`backups` :  A folder containing backups for the database.A backup is added every time the application is closed.

----`recent` : A folder containing one file; the most recent version of the database. Do not put anything in this folder since it will automatically delete it.

#### backend.py file

The project uses the openpyxl library to read, write and update a generated excel file. The `backend.py` module is responsible for these tasks and has three main functions.

`add_item(Row)` : Adds a row to the database and returns its generated ID.

`remove_item(id)` : Change the value of the `Removed` column to `True` for the row with that id.

`get_info(id)` : Returns the row with the parameters id. May return a `NO_SUCH_ITEM` error code or a `ITEM_REMOVED` error code.

The `backend.py` file also defines a Row object for passing a row of data around the application.
