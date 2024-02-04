import openpyxl
import pandas as pd

class ExcelFile:

    def __init__(self, file_name):
        self.filename = file_name
        self.workbook = openpyxl.load_workbook(self.filename)
        self.worksheet = self.workbook.active

    def close_file(self):
        self.workbook.close()

    def countRows(self):
        # Count rows
        return self.worksheet.max_row

    def writeOnXL(self, data):

        # Change dtype for phone number to string
        # Add new row to worksheet
        self.worksheet.append(data)

        # Save changes to the workbook
        self.workbook.save(self.filename)
        
        self.workbook.close()

    # ---> FOR SO_FORM <--- #
    def read_into_dataframe_SO(self):
        # Read the Excel file into a pandas DataFrame
        return pd.read_excel(self.filename,  dtype={'PHONE': str})

    # ---> FOR AI_FORM <--- #
    def read_into_dataframe(self):
        # Read the Excel file into a pandas DataFrame
        return pd.read_excel(self.filename, 'Current Master')
    
    def update_excel(self, row, new_values):
        # Update the Excel file with the new values
        for i, value in enumerate(new_values, start=1):
            self.worksheet.cell(row=row, column=i, value=value)
        self.workbook.save(self.filename)
        self.close_file()



def open_excel_file(file_name): 
    return ExcelFile(file_name)
