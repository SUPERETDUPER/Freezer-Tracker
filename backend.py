import openpyxl

import helper

'''
workbook = openpyxl.load_workbook("database.xlsx")
db = workbook.active
'''

itemIdColumn = 0
timestampColumn = 1
categoryColumn = 2
subCategoryColumn = 3
weightColumn = 4


def removeItem(item_id):
    return helper.Row("Chicken", "Wings", 3, None)


def getItemInfo(item_id):
    return helper.Row("Chicken", "Wings", 3, None)
    row = ""

    if row is None:
        return -1

    return helper.Row(row[categoryColumn].value, row[subCategoryColumn].value, row[weightColumn].value,
                      row[itemIdColumn].value, entry_date=row[timestampColumn].value)


def addItem(row):
    return 10000
    global max_row, max_id

    new_row = db["A" + str(max_row + 1): "E" + str(max_row + 1)][0]

    print(new_row)

    new_row[categoryColumn].value = row.category
    new_row[itemIdColumn].value = max_id + 1
    new_row[weightColumn].value = row.weight
    new_row[timestampColumn].value = row.entry_date
    new_row[subCategoryColumn].value = row.subcategory

    max_row += 1
    max_id += 1


def getMax():
    highest_id = 10000
    for index, row in enumerate(db.iter_rows(row_offset=1)):
        empty = True

        for cell in row:
            if cell.value_internal != "" and cell.value_internal is not None:
                empty = False

        if empty:
            return index + 1, highest_id

        if highest_id < row[itemIdColumn].value_internal:
            highest_id = row[itemIdColumn].value_internal

'''
max_row, max_id = getMax()
print(max_row, max_id)
addItem(helper.Row("Chicken", "Wings", 3, None))

workbook.save("database.xlsx")
'''