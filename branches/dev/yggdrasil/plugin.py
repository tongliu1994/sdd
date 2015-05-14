import socket
import time

class GenericPlugin:
    def __init__(self):
        self.mip = ''   #ip of plugin
        self.mport = 1537   #port the plugin will run on
        self.mname = 'odin'  #plugin name
        self.msock = None   #socket used within class
        self.myggdrasilIp = ''  #yggdrasil's ip
        self.myggdrasilPort = ''    #yggdrasil's port

    # Generic method. This does the main functionality of the plugin using
    #   the data sent from Yggdrasil and return the data to be sent back
    # This should be implemented on a per plugin basis
    def method(self, data):
        print "This plugin's method has not been implemented yet"
        return '<?xml version="1.0"?><data><ticker symbol="CY" market="DJI"><field>s</field><field>n</field><field>o</field><field>l1</field><field>p</field></ticker><ticker symbol="IBM" market="DJI"><field>n</field><field>s</field><field>l1</field><field>o</field><field>p</field></ticker><ticker symbol="GOOG" market="IXIC"><field>n</field><field>l1</field><field>s</field><field>o</field><field>p</field></ticker><ticker symbol="^XAU" market="DJI"><field>n</field><field>s</field><field>l1</field><field>o</field><field>p</field></ticker></data>'

    # recieves data from yggdrasil and runs the plugin method on it
    #   then takes output from the method and sends it to Yggdrasil
    def contactYggdrasil(self):
        BUFFER_SIZE = 1024
        ret = -1
        # Receive input from yggdrasil
        print "Waiting to recieve XML request from Yggdrasil..."
        data = self.msock.recv(BUFFER_SIZE)
        # If Yggdrasil sends an XML schema, attempt Plugin method
        try:
            print "Recieved XML for fetching. Attempting method"
            print data
            sendData = self.method(data)
            ret = 1
        except:
            # XML file is inappropriate
            # Bad XML file, tell yggrdasil it's bad
            print "Bad XML"
            sendData = 'Bad XML'
            ret = 0
        # Attempt to send return data, if it fails wait for next input
        try:
            self.msock.send(sendData)
        except:
            print "Connection Error!"
            ret = -1
        return ret

    # Handshake used to connect to Yggdrasil properly
    def handShake(self):
        BUFFER_SIZE = 1024
        tempSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected=0
        while not connected:
            try:
                tempSock.bind((self.mip,self.mport))
                connected=1
            except:
                print "Waiting for socket to unbind..."
                time.sleep(5)
        tempSock.listen(1)

        # Once a connection is established accept it and begin sending data
        print "Finding Yggdrasil..."
        conn, self.mip = tempSock.accept()
        print 'Connection from:', self.mip

        flag = True
        while flag:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            print "received data:", data
            # Checks if the handshaking recieved the correct passcode
            if(data == "I am yggdrasil"):
                print "Yggdrasil found! Waiting for Yggdrasil server startup..."
                # Sends the correct passcode back, and recieve the IP and port of Yggdrasil
                sendData = "I am " + self.mname
                print sendData
                conn.send(sendData)
                recvData = conn.recv(BUFFER_SIZE)
                print self.mip[0], recvData
                self.myggdrasilIp = self.mip[0]
                self.myggdrasilPort = recvData
                flag = False
            else:
                # Connection is not Yggdrasil, loop around and check next connection
                print "Not Yggdrasil."
                recData = "I DON'T KNOW YOU!"
                conn.send(recData)


        conn.close()

    # Starts the plugin
    def start(self):
        print "Starting", self.mname

        self.handShake()

        print "Setting up as a client..."
        self.msock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "ip=",self.myggdrasilIp," port=",self.myggdrasilPort
        self.msock.connect((self.myggdrasilIp, int(self.myggdrasilPort)))
        print "Set up as a client..."

        flag = 1
        while flag == 1:
            flag = self.contactYggdrasil()

# DEBUG
if __name__ == '__main__':
    a = GenericPlugin()
    a.start()
