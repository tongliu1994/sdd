import MySQLdb as mdb
import xml.etree.ElementTree as ET
from lxml import etree
import csv
import urllib2
import socket
import time

#the connection to the mysql database
#connect is used:(location of db, username, password, the database name)
#con = mdb.connect('192.168.1.75', 'odin', 'odintest123', 'odindatabase');

testXml = '<?xml version="1.0" encoding="ASCII"?><data><ticker symbol="FB" market="DJI"><s>FB</s><n0>Facebook, Inc.</n0><o0>79.37</o0><l1>80.04</l1><p0>78.37</p0></ticker><ticker symbol="IBM" market="DJI"><n0>International Bus</n0><s0>IBM</s0><l1>162.18</l1><o0>162.11</o0><p0>161.79</p0></ticker><ticker symbol="GOOG" market="IXIC"><n0>Google Inc.</n0><l1>543.98</l1><s0>GOOG</s0><o0>539.32</o0><p0>532.71</p0></ticker><ticker symbol="^XAU" market="DJI"><n0>PHLX Gold/Silver </n0><s0>^XAU</s0><l1>76.25</l1><o0>75.656</o0><p0>75.927</p0></ticker></data>'


#DEBUG
AllTags = ('c8', 'g3', 'a0', 'b2', 'a5', 'a2', 'b0', 'b3', 'b6', 'b4', 'c1', 'c0', 'm7', 'm5', 'k4', 'j5', 'p2', 'k2', 'c6', 'c3', 'c4', 'h0', 'g0', 'm0', 'm2', 'w1', 'w4', 'r1', 'd0', 'y0', 'e0', 'j4', 'e7', 'e9', 'e8', 'q0', 'm3', 'f6', 'l2', 'g4', 'g1', 'g5', 'g6', 'v1', 'v7', 'd1', 'l1', 'k1', 'k3', 't1', 'l0', 'l3', 'j1', 'j3', 'i0', 'n0', 'n4', 't8', 'o0', 'i5', 'r5', 'r0', 'r2', 'm8', 'm6', 'k5', 'j6', 'p0', 'p6', 'r6', 'r7', 'p1', 'p5', 's6', 's1', 'j2', 's7', 'x0', 's0', 't7', 'd2', 't6', 'f0', 'm4', 'v0', 'k0', 'j0', 'w0')

#ResetData resets the database to be empty
def ResetData():
  with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS StockData")
    cur.execute("CREATE TABLE StockData(Id INT PRIMARY KEY AUTO_INCREMENT, time decimal(15,2), c8 VARCHAR(10), g3 VARCHAR(10), a0 VARCHAR(10), b2 VARCHAR(10), a5 VARCHAR(10), a2 VARCHAR(10), b0 VARCHAR(10), b3 VARCHAR(10), b6 VARCHAR(10), b4 VARCHAR(10), c1 VARCHAR(10), c0 VARCHAR(10), m7 VARCHAR(10), m5 VARCHAR(10), k4 VARCHAR(10), j5 VARCHAR(10), p2 VARCHAR(10), k2 VARCHAR(10), c6 VARCHAR(10), c3 VARCHAR(10), c4 VARCHAR(10), h0 VARCHAR(10), g0 VARCHAR(10), m0 VARCHAR(10), m2 VARCHAR(10), w1 VARCHAR(10), w4 VARCHAR(10), r1 VARCHAR(10), d0 VARCHAR(10), y0 VARCHAR(10), e0 VARCHAR(10), j4 VARCHAR(10), e7 VARCHAR(10), e9 VARCHAR(10), e8 VARCHAR(10), q0 VARCHAR(10), m3 VARCHAR(10), f6 VARCHAR(10), l2 VARCHAR(10), g4 VARCHAR(10), g1 VARCHAR(10), g5 VARCHAR(10), g6 VARCHAR(10), v1 VARCHAR(10), v7 VARCHAR(10), d1 VARCHAR(10), l1 VARCHAR(10), k1 VARCHAR(10), k3 VARCHAR(10), t1 VARCHAR(10), l0 VARCHAR(10), l3 VARCHAR(10), j1 VARCHAR(10), j3 VARCHAR(10), i0 VARCHAR(10), n0 VARCHAR(25), n4 VARCHAR(10), t8 VARCHAR(10), o0 VARCHAR(10), i5 VARCHAR(10), r5 VARCHAR(10), r0 VARCHAR(10), r2 VARCHAR(10), m8 VARCHAR(10), m6 VARCHAR(10), k5 VARCHAR(10), j6 VARCHAR(10), p0 VARCHAR(10), p6 VARCHAR(10), r6 VARCHAR(10), r7 VARCHAR(10), p1 VARCHAR(10), p5 VARCHAR(10), s6 VARCHAR(10), s1 VARCHAR(10), j2 VARCHAR(10), s7 VARCHAR(10), x0 VARCHAR(10), s0 VARCHAR(10), t7 VARCHAR(10), d2 VARCHAR(10), t6 VARCHAR(10), f0 VARCHAR(10), m4 VARCHAR(10), v0 VARCHAR(10), k0 VARCHAR(10), j0 VARCHAR(10), w0 VARCHAR(10))")

#ParseXml parses the xml file output.xml and adds the data in it to the databse
#   by calling AddRow for each ticker in the xml
# includes the current time in seconds
#TODO make this work with a connection to yggdrasil instead of using output.xml
def ParseXml():
  #current time in seconds
  t = str(time.time())

  #Creates the root node of the return XML file
  returnRoot = etree.Element('data')
  chunkRoot = etree.Element('data')

  #Parses the input XML file, and finds the root (in this case <data></data>)
  tree = ET.parse('output.xml')
  root = tree.getroot()

  # Loops through all children of the root node (in this case <ticker></ticker>)
  for child in root:
    #all fields to add to the database for a ticker, starting with time
    fields = [('time', t)]

    # symbol = child.get("symbol") # Gets symbol e.g FB
    # market = child.get("market") # Gets market e.g DJI

    # Loops through all fields of the ticker's node
    #   getting the name of the field and info to store from that field
    for field in child:
      if len(field.tag) == 1: #fields with a 0 can be written without that 0
                              #   this takes the case were the 0 in not written
        #adds the fields name and data
        fields.append((field.tag + '0', field.text))
      else:
        #adds the fields name and data
        fields.append((field.tag, field.text))

    #adds ticker to database
    AddTickerData(fields)

#ParseYggdrasilXml parses the xml file sent from yggdrasil and adds the data in
#   it to the databse by calling AddRow for each ticker in the xml
# includes the current time in seconds
#TODO make this work with a connection to yggdrasil instead of using output.xml
def ParseYggdrasilXml(_yggdrasilXml):
  #current time in seconds
  t = str(time.time())

  #Creates the root node of the return XML file
  returnRoot = etree.Element('data')

  #Parses the input XML file, and finds the root (in this case <data></data>)
  tree = ET.fromstring(_yggdrasilXml)
  # root = tree.getroot()
  # Loops through all children of the root node (in this case <ticker></ticker>)
  for child in tree:
    #all fields to add to the database for a ticker, starting with time
    fields = [('time', t)]
    symbol = child.get("symbol") # Gets symbol e.g FB
    #market = child.get("market") # Gets market e.g DJI
    print "symbol=",symbol
    # Loops through all fields of the ticker's node
    #   getting the name of the field and info to store from that field
    for field in child:
      if len(field.tag) == 1: #fields with a 0 can be written without that 0
                              #   this takes the case were the 0 in not written
        #adds the fields name and data
        fields.append((field.tag + '0', field.text))
      else:
        #adds the fields name and data
        fields.append((field.tag, field.text))

    #adds ticker to database
    print fields
    #AddTickerData(fields)


#AddRowData adds one ticker to the database where the info for the ticker is
#   stored in _fields as a list of tuples (field name, field data) e.g (n0, 1)
def AddTickerData(_fields):
  #first converts _fields into the command to use on the database
  ToExecute = "insert into StockData("
  flag = True
  for field in _fields:
    if flag:
      flag = False
    else:
      ToExecute += ", "
    ToExecute += field[0]

  ToExecute += ") values("

  flag = True
  for field in _fields:
    if flag:
      flag = False
    else:
      ToExecute += ", "
    ToExecute += "'" + field[1] + "'"

  ToExecute += ")"


  with con:
    cur = con.cursor()

    #uses the command to input the data into the database
    cur.execute(ToExecute)

#PrintData prints data from database
def PrintData():
  with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM StockData")

    rows = cur.fetchall()

    for row in rows:
        print row

#PrintDataDesc prints data from database with each field labeled
def PrintDataDesc():
  with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM StockData")

    rows = cur.fetchall()

    desc = cur.description
    #print "%s %3s %4s" % (desc[0][0], desc[1][0], desc[2][0])

    for row in rows:
      print ""
      for i in range(0, len(row)):
        if row[i] != None:
          print '', str(desc[i][0]) + ': ' + str(row[i])

#updates a line in the database currently not implemented properly but we might
#   not need to implement it
# def UpdateData():
#   with con:
#     cur = con.cursor()
#
#     cur.execute("UPDATE Writers SET Name = %s WHERE Id = %s",
#         ("Cody", "4"))
#
#     print "Number of rows updated:",  cur.rowcount





#DEBUG
#ResetData()
# ParseXml()
ParseYggdrasilXml(testXml)
# UpdateData()
#PrintDataDesc()
