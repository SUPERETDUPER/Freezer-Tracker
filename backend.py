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
import datetime
import os.path

import openpyxl

import globalvar
from constants import idColumn, timeColumn, typeColumn, subtypeColumn, weightColumn, removedColumn, columns, \
    db_file_path


class Database:

    last_id = 9999

    def __init__(self):
        if os.path.isfile(db_file_path):
            self.workbook = openpyxl.load_workbook(filename=db_file_path)  # If file exists, load it
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

            if self.last_id < row[columns[idColumn]].value:  # Update to get latest id assigned
                self.last_id = row[columns[idColumn]].value

    def create_header(self):
        for column in columns.keys():
            header_cell = self.ws.cell(row=1, column=columns[column] + 1)
            header_cell.value = column

    def save(self):
        self.workbook.save(filename=db_file_path)

    def add_item(self, row):
        empty_row = self.ws[self.lastRow + 1]

        for index, cell in enumerate(columns):

            value = row.get_row()[index]

            if value is not None:
                empty_row[index].value = row.get_row()[index]

            if index == 0:
                empty_row[index].value = self.last_id + 1
                self.last_id += 1

        empty_row[columns[removedColumn]].value = False

        self.lastRow += 1
        self.save()
        return self.last_id

    def remove_item(self, batch_number):
        row = self.get_row(batch_number)
        if row == -1:
            return False

        row[columns[removedColumn]].value = True

        self.save()
        return True

    def get_info(self, batch_number):
        row = self.get_row(batch_number)
        if row == -1:
            return False
        if row[columns[removedColumn]].value is True:
            return False
        return Row(batch_number=row[columns[idColumn]].value, category=row[columns[typeColumn]].value,
                   subcategory=row[columns[subtypeColumn]].value, weight=row[columns[weightColumn]].value,
                   entry_date=row[columns[timeColumn]].value)

    def get_row(self, batch_number):
        for index, row in enumerate(self.ws.iter_rows(row_offset=1)):
            if row[columns[idColumn]].value == batch_number:
                return row
        return -1


class Row:
    def __init__(self, category=None, subcategory=None, weight=None, batch_number=None, entry_date=None):
        if entry_date is None:
            entry_date = '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())

        self.row = [None] * len(columns)

        self.row[columns[idColumn]] = batch_number
        self.row[columns[timeColumn]] = entry_date
        self.row[columns[typeColumn]] = category
        self.row[columns[subtypeColumn]] = subcategory
        self.row[columns[weightColumn]] = weight

    def get_row(self):
        return self.row

    def get_item(self, index):
        return self.row[index]


globalvar.database = Database()
