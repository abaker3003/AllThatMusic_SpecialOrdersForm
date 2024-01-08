import openpyxl
import os

class ExcelFile:

    def __init__(self):
        self.filename = 'SO_Test.xlsx'
        self.workbook = openpyxl.load_workbook(self.filename)
        self.worksheet = self.workbook.active

    def close_file(self):
        self.workbook.close()

    def countRows(self):
        # Count rows
        return self.worksheet.max_row

    def writeOnXL(self, data):

        # Add new row to worksheet
        self.worksheet.append(data)

        # Save changes to the workbook
        self.workbook.save(self.filename)


def open_excel_file(): 
    return ExcelFile()
