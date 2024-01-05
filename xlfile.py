import openpyxl

def openxl():
    # Open an existing workbook
    workbook = openpyxl.load_workbook('SO_Test.xlsx')

    # Select a specific worksheet
    worksheet = workbook['Sheet1']

    # Read data from a specific cell
    cell_value = worksheet['A1'].value

    # Write data to a specific cell
    worksheet['B1'] = 'New Value'

    # Save changes to the workbook
    workbook.save('SO_Test.xlsx')
