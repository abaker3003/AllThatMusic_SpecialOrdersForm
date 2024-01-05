import openpyxl

def __init__(self):
    this.file = 'SO_Test.xlsx'

def openxl(self):
    # Open an existing workbook
    workbook = openpyxl.load_workbook(this.file)

    # Select a specific worksheet
    worksheet = workbook['Sheet1']

    return workbook, worksheet

def countRows(self):

    # Open file and save workbook and worksheet
    wb, ws = self.openxl()

    # Count rows
    return ws.max_rows

def writeOnXL(self, data):

    # Open file and save workbook and worksheet
    wb, ws = self.openxl()

    # Add new row to worksheet
    ws.append(data)

    '''# Read data from a specific cell
    cell_value = ws['A1'].value

    # Write data to a specific cell
    ws['B1'] = 'New Value'''

    # Save changes to the workbook
    wb.save(this.file)
