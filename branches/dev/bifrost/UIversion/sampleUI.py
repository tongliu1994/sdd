

#SIMPLE USER INTERFACE IMPLEMENTATION OF BIFROST
#USER INPUTS STOCK TICKER, NAME, LATEST VALUE, OPENING VALUE, AND CLOSING VALUE ARE DISPLAYED

import Tkinter
from Tkinter import *
import ttk
import csv
import urllib2


def Pull(*args):
    try:
        s = ticker.get()
        tickerURL = 'http://download.finance.yahoo.com/d/quotes.csv?s=%40%5EDJI,' + s + '&f=nsl1op&e=.csv'
        response = urllib2.urlopen(tickerURL)
        cr = csv.reader(response)
        for row in cr:
            name.set(row[0])
            latestValue.set(row[2])
            openValue.set(row[3])
            closingValue.set(row[4])

    except ValueError:
        pass

root = Tk()
root.title("Stock Information via Ticker")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

name = StringVar()
ticker = StringVar()
latestValue = StringVar()
openValue = StringVar()
closingValue = StringVar()

ticker_entry = ttk.Entry(mainframe, width=7, textvariable=ticker)
ticker_entry.grid(column=1, row=1, sticky=(W, E))
ttk.Label(mainframe, text="Ticker").grid(column=2, row=1, sticky=W)
ttk.Button(mainframe, text="Pull Data", command=Pull).grid(column=3, row=1, sticky=W)

ttk.Label(mainframe, textvariable=name).grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, textvariable=latestValue).grid(column=2, row=2, sticky=(W, E))
ttk.Label(mainframe, text="(Latest Value)").grid(column=3, row=2, sticky=W)

ttk.Label(mainframe, textvariable=openValue).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, text="(Opening Value)").grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, textvariable=closingValue).grid(column=2, row=4, sticky=(W, E))
ttk.Label(mainframe, text="(Closing Value)").grid(column=3, row=4, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

ticker_entry.focus()
root.bind('<Return>', Pull)

root.mainloop()
