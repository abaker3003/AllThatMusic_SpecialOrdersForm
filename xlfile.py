import openpyxl

def openxl():
    # Open an existing workbook
    workbook = openpyxl.load_workbook('SO_Test.xlsx')

    # Select a specific worksheet
    worksheet = workbook['Sheet1']

    return workbook, worksheet

def countRows():

    # Open file and save workbook and worksheet
    wb, ws = openxl()

    # Count rows
    return ws.max_row

def writeOnXL(data):

    # Open file and save workbook and worksheet
    wb, ws = openxl()

    # Add new row to worksheet
    ws.append(data)

    '''# Read data from a specific cell
    cell_value = ws['A1'].value

    # Write data to a specific cell
    ws['B1'] = 'New Value'''

    # Save changes to the workbook
    wb.save('SO_Test.xlsx')
