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

Backend code with database operations.

"""
import os.path

import openpyxl

import constants
import globalvar
import helper
from constants import ERROR_ITEM_REMOVED, ERROR_NO_SUCH_ITEM


class Database:
    next_id = 10000

    def __init__(self):
        if os.path.isfile(constants.db_file_path):
            self.workbook = openpyxl.load_workbook(filename=constants.db_file_path)  # If file exists, load it
            self.ws = self.workbook.active
        else:
            self.workbook = openpyxl.Workbook()  # Else create it and create headers
            self.ws = self.workbook.active

            self.create_header()

        for index, row in enumerate(self.ws.iter_rows(row_offset=1)):  # Loop through every row

            empty = True

            for cell in row:
                if cell.value != "" and cell.value is not None:
                    empty = False

            if empty:  # If empty tracker is still True after looping through all the row's cells, this line is empty
                self.lastRow = index + 1
                break

            if self.next_id < row[constants.columns[constants.idColumn]].value + 1:  # Update to get latest id assigned
                self.next_id = row[constants.columns[constants.idColumn]].value + 1

    def create_header(self):  # Used to create a new database's headers
        for column in constants.columns.keys():
            header_cell = self.ws.cell(row=1, column=constants.columns[column] + 1)
            header_cell.value = column

    def save(self):  # Save workbook
        self.workbook.save(filename=constants.db_file_path)

    def add_item(self, row):  # Add a row to the database and return generated id
        empty_row = self.ws[self.lastRow + 1]  # Empty row to fill

        for index, cell in enumerate(constants.columns):  # For every cell in empty_row

            value = row.get_row()[index]  # Get value to fill

            if value is not None:
                empty_row[index].value = row.get_row()[index]  # If value exists fill it in

            if index == 0:  # Generate index
                empty_row[index].value = self.next_id  # Assign batch number
                self.next_id += 1

        empty_row[constants.columns[constants.removedColumn]].value = "False"  # Set removed to false

        self.lastRow += 1

        self.save()

        return self.next_id - 1

    def remove_item(self, batch_number):
        row = self.get_row(batch_number)  # Get row to set to removed
        if row == ERROR_NO_SUCH_ITEM:
            return ERROR_NO_SUCH_ITEM

        if row[constants.columns[constants.removedColumn]].value == "True":
            return ERROR_ITEM_REMOVED

        row[constants.columns[constants.removedColumn]].value = "True"

        row[constants.columns[constants.removedTimeColumn]].value = helper.get_current_date()

        self.save()
        return True

    def get_info(self, batch_number):

        row = self.get_row(batch_number)  # get row with info

        if row == ERROR_NO_SUCH_ITEM:  # If row does not exist return False
            return ERROR_NO_SUCH_ITEM

        if row[constants.columns[constants.removedColumn]].value == "True":
            return ERROR_ITEM_REMOVED  # If row already removed return False

        return Row(batch_number=row[constants.columns[constants.idColumn]].value,
                   category=row[constants.columns[constants.typeColumn]].value,
                   subcategory=row[constants.columns[constants.subtypeColumn]].value,
                   weight=row[constants.columns[constants.weightColumn]].value,
                   entry_date=row[constants.columns[constants.timeColumn]].value)

    def get_row(self, batch_number):
        for index, row in enumerate(self.ws.iter_rows(row_offset=1)):  # Loop through every row
            if row[constants.columns[constants.idColumn]].value == batch_number:  # If batch number matches return row
                return row
        return ERROR_NO_SUCH_ITEM  # Else return -1


class Row:  # Row object storing row data
    def __init__(self, category=None, subcategory=None, weight=None, batch_number=None, entry_date=None):
        if entry_date is None:
            entry_date = helper.get_current_date()

        self.row = [None] * len(constants.columns)

        self.row[constants.columns[constants.idColumn]] = batch_number
        self.row[constants.columns[constants.timeColumn]] = entry_date
        self.row[constants.columns[constants.typeColumn]] = category
        self.row[constants.columns[constants.subtypeColumn]] = subcategory
        self.row[constants.columns[constants.weightColumn]] = weight

    def get_row(self):
        return self.row

    def get_item(self, index):
        return self.row[index]


globalvar.database = Database()
