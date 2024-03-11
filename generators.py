import datetime
import xlfile as xl


# Need to configure this to handle generating reference number when 
# file contains data from previous days so the last 3 digits does not 
# reference the total number of rows

def ticketnum(excel_file):
    dt = datetime.datetime.now()

    dt_data_format = get_todays_date()

    num = get_todays_entries_count(dt_data_format, excel_file)

    tckt = "SO" + dt.strftime("%y%m%d") + "{:03d}".format(num)

    return tckt

def get_todays_date():
     dt = datetime.datetime.now()

     return dt.strftime("%m") + "/" + dt.strftime("%d") + "/" + dt.strftime("%Y")

def get_todays_entries_count(today, excel_file):

    # Set count to 1 to avoid triple 0 entry
    count = 1
    for row in range(1, excel_file.countRows()+1):
        if excel_file.worksheet.cell(row=row, column=1).value == today:
            count += 1
    return count
