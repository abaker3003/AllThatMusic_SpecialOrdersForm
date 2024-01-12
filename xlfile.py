import openpyxl
import os
import pandas as pd

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

    def read_into_dataframe(self):
        # Read the Excel file into a pandas DataFrame
        return pd.read_excel(self.filename)

    def update_excel(self, row, new_values):
        # Update the Excel file with the new values
        for i, value in enumerate(new_values, start=1):
            self.worksheet.cell(row=row, column=i, value=value)
        self.workbook.save(self.filename)



def open_excel_file(): 
    return ExcelFile()
