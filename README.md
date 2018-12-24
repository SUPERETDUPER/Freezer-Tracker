# Freezer Tracker

This is a freezer inventory management tool.

## How it works
This project is designed to run on a Raspberry Pi with a Raspberry Pi 7'' touchscreen.

Enter an item's info (weight and type) on the screen then write the number displayed onto the item. Place the item in the freezer.

To remove the item simply enter the its number on the screen.

At anytime, check what items are currently in your freezer by consulting the excel database (in `/local`).

The database tracks the type (and sub-type), weight, entry date and removal date of all items.

The database can be setup to be shared across multiple devices via a network drive (ex. windows share drive).

![image of startup screen](/res/docs/startup_screen.png)

![image of home screen](/res/docs/home_screen.png)

![image of item weight screen](/res/docs/item_weight.png)

## Run the project

1. Download the code to your device.

2. Run `pip3 install openpyxl` to install the openpyxl library (pip must already be installed).

3. Run `main.py` once. This will generate the `/local` folder and then throw an error.

4. Open `/local/local.conf` and change the value of `project_code` to whatever you want to name your project. If you are tracking data for several different freezer on the same server, this code needs to be unique.

5. Run `main.py`.

### Further setup

- Add your logo to `/res/img` with the name `ic_logo.png`.

- Explore the settings in `/local/local.conf` to further customize your setup. 

- Edit `/local/meat_list.json` to define your own types of items. Make sure to keep the same JSON format.

## Technical details

The projects is uses the language Python. 

- Tkinter is used for graphics (GUI)
 
- Openpyxl is used to interact with the excel database

- ConfigParser is used for reading the local.conf file.

### Project structure

`/frames`: Contains code for the different layouts and windows used in the GUI. `/frames/baseframe.py` contains parent and basic windows to be customised by the other frame files.

`/res`: contains all resources including:
 
 - default config files to create `/local` during setup;
 -  `/res/img` containing images for GUI.

`/local`: auto-generated folder that contains the local installation settings and the database. Not tracked by Git.

`backend.py`: backend methods to interact with the database (using openpyxl).

`fileManager.py`: reads and manages the `/local` config files and runs the network drive upload and backup operations.

`global_var.py`: contains all app-wide constants (`app` the tkinter root and `images` a holder for all Photoimage objects).

`helper.py`: contains helper methods.

`main.py`: where the tkinter root and layout structure is built.

### Tkinter multi-window approach

The app contains multiples windows. Windows are stacked one on top of each another. The command below raises a window to the top of the stack to display it:
`helper.getContainer().show_frame(FrameToDisplay.__name__)`.

The command also calls `setup_frame()` and `reset_frame()` on the new and old window respectively.

### Backend structure

The project's master database is stored locally in `/local`.

If configured, the database can be automatically copied onto a network drive when modified. This network drive can be any folder and is set in `/local/local.conf`.

When configured, the app creates the following folders in the network drive.

`NETWORK_DRIVE/PROJECT_CODE/backups`: contains backups of the database automatically create when app is closed.

`NETWORK_DRIVE/PROJECT_CODE/recent`: contains the most recent version of the database. The folder is deleted and re-created each database modification.
