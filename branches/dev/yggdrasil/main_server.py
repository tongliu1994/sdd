import socket
import time

#for the proof of concept test to send to bifrost
testXML = '<?xml version="1.0"?><data><ticker symbol="FB" market="DJI"><field>s</field><field>n</field><field>o</field><field>l1</field><field>p</field></ticker><ticker symbol="IBM" market="DJI"><field>n</field><field>s</field><field>l1</field><field>o</field><field>p</field></ticker><ticker symbol="GOOG" market="IXIC"><field>n</field><field>l1</field><field>s</field><field>o</field><field>p</field></ticker><ticker symbol="^XAU" market="DJI"><field>n</field><field>s</field><field>l1</field><field>o</field><field>p</field></ticker></data>'

#blank ip=localhost, 1337 is default port, will change in later revision to use yggdrasil.conf
serverIP = ''
serverPort = 1337

#ip and port for bifrost (default)
feedHandlerIP = '192.168.1.75'
feedHandlerPort = 1338

#ip and port for database (deafault)
databasePluginIP = '127.0.0.1'
databasePluginPort = 1339

#create a client socket
BUFFER_SIZE = 1024
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
feedHandlerFound=0

#for the handshake
prompt = "I am yggdrasil"

#attempt to connect to bifrost
while feedHandlerFound==0:
    try:
        c.connect((feedHandlerIP,feedHandlerPort))
        feedHandlerFound=1
    except:
        print "Looking for Bifrost..."
    time.sleep(5)

#now we're connected, send handshake
c.send(prompt)
#receive response
data = c.recv(BUFFER_SIZE)
print "response: " + data
#verify it's bifrost
if(data == "I am bifrost"):
    print ("sending connection information for bifrost")
    #tell bifrost the available port
    c.send(str(serverPort))

#boot up yggdrasil server application
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((serverIP,serverPort))
s.listen(1)
#close down client connection to bifrost, indicating we are ready for bifrost to connect to us now
c.close()
conn, addr = s.accept()
#accept client connection from bifrost
print 'Connection from:',addr
while 1:
    #send bifrost our test xml
    conn.send(testXML)
    #receive data back from bifrost
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    #print data for debug purposes
    print "received data:", data
    time.sleep(5)
#quit on close
conn.close()
