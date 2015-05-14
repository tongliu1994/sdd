

#CURRENT VERSION OF FEED HANDLER
#TAKES IN AN XML SCHEMA WITH ALL THE TICKER SYMBOLS
#OUTPUTS A SCHEMA WITH THE TICKER SYMBOL AND ASSOCIATED INFORMATION
#print 'Hello, world!'
from xml.dom.minidom import parse
from lxml import etree
import csv
import urllib2

#PARSES INPUT SCHEMA
xmldoc = parse("tickerData.xml")
itemlist = xmldoc.getElementsByTagName("item")

#BEGINS OUTPUT SCHEMA
root = etree.Element('TickerValues')

#RUNS THROUGH EACH ITEM ON THE SCHEMA
for s in itemlist :
    print s.attributes["ticker"].value
    tickerURL = 'http://download.finance.yahoo.com/d/quotes.csv?s=%40%5EDJI,' + s.attributes["ticker"].value + '&f=nsl1op&e=.csv'
    response = urllib2.urlopen(tickerURL)
    cr = csv.reader(response)

    #RUNS THROUGH THE RETURN VALUES FROM THE STOCKS API
    for row in cr:
      ticker = etree.Element('Ticker')
      name = etree.Element('Name')
      name.text = row[0]
      ticker.append(name)
      symbol = etree.Element('Symbol')
      symbol.text = row[1]
      ticker.append(symbol)
      latestValue = etree.Element('LatestValue')
      latestValue.text = row[2]
      ticker.append(latestValue)
      openValue = etree.Element('OpeningValue')
      openValue.text = row[3]
      ticker.append(openValue)
      closingValue = etree.Element('ClosingValue')
      closingValue.text = row[4]
      ticker.append(closingValue)
      root.append(ticker)

tree = etree.ElementTree()
tree._setroot(root)
tree.write('output.xml', xml_declaration=True, pretty_print=True)
#s = etree.tostring(root, xml_declaration=True, pretty_print=True)
