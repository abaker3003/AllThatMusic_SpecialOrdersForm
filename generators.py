import datetime
import xlfile as xl

def ticketnum():
    dt = datetime.datetime.now()
    tckt = "SO" + dt.strftime("%y%m%d") + "{:03d}".format(xl.countRows())

    return tckt