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


class Reader:
    def __init__(self):
        working_dir = os.getcwd()

        # LOCAL FOLDER
        self.local_folder = os.path.join(working_dir, "local")  # Path to local folder

        if not os.path.isdir(self.local_folder):  # If local dir does not exist make it
            os.makedirs(self.local_folder)

        # MEAT LIST FILE
        meat_list_path = os.path.join(self.local_folder, "meat_list.json")  # Path to meat list file

        if not os.path.isfile(meat_list_path):  # If meat list not created create it from default one
            shutil.copy(os.path.join(working_dir, "res", "default_meat_list.json"), meat_list_path)

        with open(meat_list_path) as json_data:  # Open meat_list.json and extract data into variable
            self.meat_list = json.load(json_data)
        json_data.close()

        # CONFIG FILE
        local_conf_path = os.path.join(self.local_folder, "local.conf")  # Path to local configuration file

        if not os.path.isfile(local_conf_path):  # If local conf does not exist make copy the default one
            shutil.copy(os.path.join(working_dir, "res", "default_local.conf"), local_conf_path)

        config = configparser.ConfigParser()  # Create config object and read file
        config.read(local_conf_path)

        self.default_section = config["DEFAULT"]

        # UPLOAD FOLDER
        upload_dir_path = os.path.dirname(self.get_upload_db_path())  # Upload folder
        if not os.path.isdir(upload_dir_path):
            os.makedirs(upload_dir_path)

        backup_dir_path = os.path.join(upload_dir_path, "backups")  # Backups
        if not os.path.isdir(backup_dir_path):
            os.makedirs(backup_dir_path)

    def get_meat_list(self):
        return self.meat_list

    def get_upload_db_path(self):
        return os.path.normpath(self.default_section["upload_db_path"])

    def get_local_db_path(self):
        return os.path.normpath(os.path.join(self.local_folder, os.path.normpath(self.default_section["db_name"])))

    def is_shutdown_on_quit(self):
        return self.default_section["shutdown_on_quit"] == "True"

    def get_backup_db_path(self):
        return os.path.abspath(self.default_section["backup_db_path"])
