import datetime
import os.path

import openpyxl

import globalvar

db_file_path = "freezer_inventory_database.xlsx"


class Column:
    def __init__(self, name, index):
        self.name = name
        self.index = index


class Database:
    def __init__(self):
        # TODO : Implement edge case of reaching id 99 999

        if os.path.isfile(db_file_path):
            self.workbook = openpyxl.load_workbook(filename=db_file_path)  # If file exists, load it
            self.ws = self.workbook.active
        else:
            self.workbook = openpyxl.Workbook()  # Else create it and create headers
            self.ws = self.workbook.active

            self.create_header()

        self.last_id = 10000

        for index, row in enumerate(self.ws.iter_rows(row_offset=1)):  # Loop through every row

            empty = True

            for cell in row:
                if cell.value != "" and cell.value is not None:
                    empty = False

            if empty:  # If empty tracker is still True after looping through all the row's cells, this line is empty
                self.lastRow = index
                break

            if self.last_id < row[Row.idColumn.index].value:
                self.last_id = row[Row.idColumn.index].value

    def create_header(self):
        for column in Row.columns:
            header_cell = self.ws.cell(row=1, column=column.index + 1)
            header_cell.value = column.name

    def save(self):
        self.workbook.save(filename=db_file_path)

    def get_info(self):
        print("Last row : " + str(self.lastRow))
        print("Last id :" + str(self.last_id))

    def add_item(self, row):
        return 0

    def remove_item(self, batch_number):
        return True

    def get_row(self, batch_number):
        return Row()


class Row:
    idColumn = Column("Batch number", 0)
    timeColumn = Column("Time stamp", 1)
    typeColumn = Column("Type", 2)
    subtypeColumn = Column("Sub-type", 3)
    weightColumn = Column("Weight", 4)

    columns = [idColumn, timeColumn, typeColumn, subtypeColumn, weightColumn]

    def __init__(self, category=None, subcategory=None, weight=None, batch_number=None, entry_date=None):
        if entry_date is None:
            entry_date = '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())

        self.row = [None] * len(self.columns)

        self.row[self.idColumn.index] = batch_number
        self.row[self.timeColumn.index] = entry_date
        self.row[self.typeColumn.index] = category
        self.row[self.subtypeColumn.index] = subcategory
        self.row[self.weightColumn.index] = weight

    def iter_row(self):
        return self.row

    def get_item(self, index):
        return self.row[index]


def get_letter(index):
    return chr(ord("A") + index)


globalvar.database = Database()
globalvar.database.save()
globalvar.database.get_info()
