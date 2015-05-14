#########################################################
#                                                       #
#   Chirs Weir                                          #
#   Tondiggidy Simonutti                                #
#   T0ng Liu                                            #
#   Codigail Doyle                                      #
#                                                       #
#   RPI Software Design and Documentation Fall 2014     #
#                                                       #
#   feed.py                                             #
#   run with ~$ python feed.py                          #
#                                                       #
#########################################################

import xml.etree.ElementTree as ET
from lxml import etree
import csv
import time
import urllib2
import socket

def fetchTicker(initialTickerData):
  #Creates the root node of the return XML file
  returnRoot = etree.Element('data')

  #Parses the input XML file, and finds the root (in this case <data></data>)
  tree = ET.fromstring(initialTickerData)

  # Loops through all children of the root node (in this case <ticker></ticker>)
  for child in tree: #root:
    fields = []
    symbol = child.get("symbol") # Gets symbol e.g FB
    market = child.get("market") # Gets market e.g DJI
    fieldlist = child.findall("field") #all fields are enclosed in "field" tags
    for field in fieldlist: # Gets all fields for this ticker (tickers don't have to have uniform fields)
      fields.append(field.text) # Appends all field.text values from the fieldlist to a list called fields

    print symbol # Debug
    print fields # Debug

    # Loops through all the fields and builds the fields request for the URL
    fieldRequest = ""
    for field in fields:
      fieldRequest += field # Adds fields to field request (it should be one bigass string (HINT: IT IS))

    #print fieldRequest #debug

    #TODO add functionality to get chunked fetches
    # Consider using some sort of map to fetch stock with matching fields
    # Builds the tickerURL request
    tickerURL = 'http://download.finance.yahoo.com/d/quotes.csv?s=%40%5E'+ market +',' + symbol + '&f=' + fieldRequest + '&e=.csv'
    #print tickerURL # Debug
    response = urllib2.urlopen(tickerURL) # Gets data from the URL
    cr = csv.reader(response) # Parses data from the csv

    # Loops through the rows of the csv and builds the return XML tree
    # (Currently some of this code is unnecessary, it is written in such a way that it can be
    #  extended when the csv holds more than just one tickers return information)
    for row in cr:
      rootChild = etree.Element('ticker') # Creates the returnRoot's child and names it (in this case <ticker></ticker>)
      rootChild.set("symbol", symbol) # Adds the symbol (eg symbol="")
      rootChild.set("market", market) # Adds the market (eg market="")
      #Loops through all data points in the row
      for i in xrange(0, len(row)):
        field = etree.Element(fields[i]) # Creates the rootChilds' child and names it (int this case <fields[i]></fields[i]>)
        field.text = row[i] # Adds the field return value (eg <fields[i]>row[i]</fields[i]>)
        rootChild.append(field) # Appends the field child to the rootChild

      returnRoot.append(rootChild) # Appends the rootChild to the returnRoot

  #returnTree = etree.ElementTree(returnRoot) # Builds the XML tree given the returnRoot
  return etree.tostring(returnRoot) # Writes the XML tree to a file

def main():
  #main server is 1337
  #feed handler talks on 1437
  print "Starting Bifrost!"
  serverIP = '' # IP of the server feed.py creates
  serverPort = 1437 # Port used to communicate as a server
  yggdrasilAddr = '' # Yggdrasil address
  yggdrasilPort = '' # Yggdrasil port

  BUFFER_SIZE = 102400 #define buffer size for XML

  # Creates a socket, and opens it using home server IP and Port
  # Listens on the port for a connection
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.bind((serverIP,serverPort))
  except:
    #bind failed, try again after port unbinds
    print "waiting for port to unbind..."
    time.sleep(5)
    return 2
  s.listen(1)

  # Once a connection is established accept it and begin sending data
  print "Finding Yggdrasil..."
  conn, addr = s.accept()
  print 'Connection from:',addr
  # Attempt to handshake with the connection (hoping for yggdrasil)
  while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break #go find Yggdrasil again
    print "received data:", data
    # Checks if the handshaking recieved the correct passcode
    if(data == "I am yggdrasil"):
      print "Yggdrasil found! Waiting for Yggdrasil server startup..."
      # Sends the correct passcode back, and recieve the IP and port of Yggdrasil
      sendData = "I am bifrost" #ident string
      conn.send(sendData)
      recvData = conn.recv(BUFFER_SIZE)
      print addr[0], recvData
      yggdrasilAddr = addr[0] #getting yggdrasil data for connection
      yggdrasilPort = recvData
      break
    else:
      # Connection is not Yggdrasil, loop around and check next connection
      print "Not Yggdrasil."
      recData = "I DON'T KNOW YOU!"
      conn.send(recData)

  conn.close()

  # Set up the client socket and connect to yggdrasil now that we are connected
  print "Setting up client..."
  c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connected=0
  while not connected: #attempt to connect
    try:
      c.connect((yggdrasilAddr, int(yggdrasilPort)))
      connected=1
    except:
      #try to connect
      print "Yggdrasil rejected our connection, reattempting..."
      time.sleep(5)

  print 'I am client!'
  while 1:
    # Receive input from yggdrasil
    print "Waiting to recieve XML request from Yggdrasil..."
    try: #try to recv, if it fails, reboot bifrost
      data = c.recv(BUFFER_SIZE)
    except:
      print "Connection Error!"
      c.close()
      print "Rebooting bifrost..."
      return 1 #error, reboot
    # If Yggdrasil sends an XML schema, attempt to fetch ticker data
    try:
      print "Recieved XML for fetching. Attempting to fetch..."
      print data
      sendData = fetchTicker(data)
    except:
      # XML file is inappropriate
      # Bad XML file, tell yggrdasil it's bad
      print "Bad XML"
      sendData = 'Bad XML'

    # Attempt to send return data, if it fails wait for next input
    try:
      c.send(sendData)
    except:
      print "Connection Error!"
      c.close()
      print "Rebooting bifrost..."
      return 1 #error


while 1:
  main()
