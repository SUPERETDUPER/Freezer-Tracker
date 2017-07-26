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

import configparser
import json
import os
import shutil

import global_var
import helper

project_code = None
upload_path = None
shutdown_on_quit = None
backup_path = None
meat_list = None
backups = None

working_dir = os.getcwd()

LOCAL_FOLDER_NAME = "local"

LOCAL_FOLDER_PATH = os.path.join(working_dir, LOCAL_FOLDER_NAME)

MEAT_LIST_DEFAULT_PATH = os.path.join(working_dir, "res/default_meat_list.json")
MEAT_LIST_LOCAL_PATH = os.path.join(LOCAL_FOLDER_PATH, "meat_list.json")

DEFAULT_CONFIG_PATH = os.path.join(working_dir, "res/default_local.conf")
LOCAL_CONFIG_PATH = os.path.join(LOCAL_FOLDER_PATH, "local.conf")


def setup():
    global project_code, upload_path, shutdown_on_quit, backup_path, meat_list, backups

    if not os.path.isdir(LOCAL_FOLDER_PATH):  # If local dir does not exist make it
        os.makedirs(LOCAL_FOLDER_PATH)

    if not os.path.isfile(MEAT_LIST_LOCAL_PATH):  # If meat list not created create it from default one
        shutil.copy(MEAT_LIST_DEFAULT_PATH, MEAT_LIST_LOCAL_PATH)

    if not os.path.isfile(LOCAL_CONFIG_PATH):  # If local conf does not exist make copy the default one
        shutil.copy(DEFAULT_CONFIG_PATH, LOCAL_CONFIG_PATH)

    with open(MEAT_LIST_LOCAL_PATH) as json_data:  # Open meat_list.json and extract data into variable
        meat_list = json.load(json_data)
    json_data.close()

    config = configparser.ConfigParser()  # Create config object and read file
    config.read(LOCAL_CONFIG_PATH)

    main_section = config["DEFAULT"]

    project_code = main_section["project_code"]

    if project_code == "NOT_SET":
        raise Exception("Project code not set. Please edit /local/local.conf file.")

    server_path = main_section["server_path"]

    if server_path == "None":
        server_path = None
    else:
        server_path = os.path.abspath(server_path)

    if server_path is not None:
        upload_path = os.path.join(server_path, project_code, "recent")

        if not os.path.isdir(upload_path):
            os.makedirs(upload_path)

        backup_path = os.path.join(server_path, project_code, "backups")

        if not os.path.isdir(backup_path):
            os.makedirs(backup_path)

    shutdown_on_quit = main_section["shutdown_on_quit"] == "True"

    backups = main_section["backups"] == "True"


def get_meat_list():
    return meat_list


def get_upload_db_path():
    return upload_path


def is_shutdown_on_quit():
    return shutdown_on_quit


def get_backup_db_path():
    return backup_path


def get_project_code():
    return project_code


def get_db_name(timestamp=True):
    if timestamp:
        return global_var.db_basename + "_" + helper.get_current_date().replace(":", "") + global_var.db_extension
    return global_var.db_basename + global_var.db_extension


def get_db_local_path():
    return os.path.join(LOCAL_FOLDER_PATH, get_db_name(timestamp=False))


def get_upload_db_path_full():
    if get_upload_db_path() is None:
        return None
    return os.path.join(get_upload_db_path(), get_db_name())


# noinspection PyTypeChecker
def get_backup_db_path_full():
    if get_backup_db_path() is None:
        return None
    return os.path.join(get_backup_db_path(), get_db_name())


def upload():
    if upload_path is not None:
        for file in os.listdir(get_upload_db_path()):
            file_path = os.path.join(get_upload_db_path(), file)
            os.remove(file_path)

        shutil.copy(get_db_local_path(), get_upload_db_path_full())
        print("Uploaded : " + get_db_local_path() + " to " + get_upload_db_path_full())


def backup():
    if backup_path is not None and backups:
        try:
            shutil.copy(get_db_local_path(), get_backup_db_path_full())
            print("Backed up : " + get_db_local_path() + " to " + get_backup_db_path_full())
        except (PermissionError, OSError) as e:
            print("Error")
            print(e)
