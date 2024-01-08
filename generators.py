import datetime

def ticketnum(num):
    dt = datetime.datetime.now()
    tckt = "SO" + dt.strftime("%y%m%d") + "{:03d}".format(num)

    return tckt