import datetime
import openpyxl

# Need to configure this to handle generating reference number when 
# file contains data from previous days so the last 3 digits does not 
# reference the total number of rows

def ticketnum(num):
    dt = datetime.datetime.now()

    tckt = "SO" + dt.strftime("%y%m%d") + "{:03d}".format(num)

    return tckt

def get_todays_date():
     dt = datetime.datetime.now()

     return dt.strftime("%m") + "/" + dt.strftime("%d") + "/" + dt.strftime("%Y")