#hi Tony
import xml.etree.ElementTree as ET
from lxml import etree
import csv
import urllib2
from collections import namedtuple
TupSymbolMarket = namedtuple("TupSymbolMarket", ["Symbol", "Market"])
from collections import defaultdict

# def AddTickerToGroup adds a ticker to a dict to group tickers by their fields
#_groupedticker is a dict[sorted tuple of fields] = [(sym1, mar1), (sym2, mar2), ...]
#_fields is a list of fields that the ticker _symbol._market contains
def AddTickerToGroup(_groupedticker, _symbol, _market, _fields):
  if(tuple(sorted(_fields)) in _groupedticker):
    _groupedticker[tuple(sorted(_fields))].append(TupSymbolMarket(Symbol = _symbol, Market = _market))
  else:
    _groupedticker[tuple(sorted(_fields))] = [TupSymbolMarket(Symbol = _symbol, Market = _market)]

#Creates the root node of the return XML file
returnRoot = etree.Element('data')

chunkRoot = etree.Element('data')

#Parses the input XML file, and finds the root (in this case <data></data>)
tree = ET.parse('tickerData.xml')
root = tree.getroot()

# Creates a dictionary where the key is the sorted tuple of fields and
#  the contents is a list of tuples of Symbol and Market which have the corresponding fields
GroupedTickers = defaultdict(list)

# Loops through all children of the root node (in this case <ticker></ticker>)
for child in root:
  fields = []
  symbol = child.get("symbol") # Gets symbol e.g FB
  market = child.get("market") # Gets market e.g DJI
  fieldlist = child.findall("field") #all fields are enclosed in "field" tags
  for field in fieldlist: # Gets all fields for this ticker (tickers don't have to have uniform fields)
    fields.append(field.text) # Appends all field.text values from the fieldlist to a list called fields

  #adds data to dict
  AddTickerToGroup(GroupedTickers, symbol, market, fields)

  #print symbol # Debug
  #print fields # Debug
  fields.sort()
  print symbol + "." + market + ":"
  print fields

  #*Cody*: I commented this out becaue I don't know what it is and it didn't work
  #chunkRoot.append(etree.Element(fields))

#example of using the groupedTickers
print '\nGrouped Tickers:'
flag = False
for key in GroupedTickers:
  if flag == True:
    print ' '
  flag = True
  for ticker in GroupedTickers[key]:
    print ticker.Symbol + '.' + ticker.Market
  print ' have fields: ', key
