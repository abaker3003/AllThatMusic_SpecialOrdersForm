import datetime

def ticketnum():
    dt = datetime.datetime.now()
    tckt = "SO" + dt.strftime("%y%m%d")
    return tckt