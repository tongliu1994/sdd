import socket

serverIP = ''
serverPort = 1337

feedHandlerIP = '192.168.1.75'
feedHandlerPort = 1338

BUFFER_SIZE = 1024
prompt = "I am yggdrasil"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((feedHandlerIP,feedHandlerPort))
s.send(prompt)
data = s.recv(BUFFER_SIZE)
print "response: " + data
if(data == "I am bifrost"):
    print ("sending connection information for bifrost")
    s.send(str(serverPort))
s.close()
