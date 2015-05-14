#########################################################
#                                                       #
#   Chris Weir                                          #
#   Tondiggidy Simonutti                                #
#   T0ng Liu                                            #
#   Codigail Doyle                                      #
#                                                       #
#   RPI Software Design and Documentation Fall 2014     #
#                                                       #
#   Yggdrasil.py                                        #
#   run with ~$ python Yggdrasil.py                     #
#                                                       #
#########################################################

import socket
import time
import os
import signal
import sys
import stat
from conf import conf

#catch ctrl-c so that we can make sure children die on exit
#zombies bad
def signal_handler(signal, frame):
    print "Caught ctrl-c, killing children..."
    print "Goodbye ",os.getpid()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#class def
class Yggdrasil:
    def __init__(self):
        self.mname = conf.identity #get the identity string from the configuration file
        self.myggdrasilIp = '' #this is blank for default
        self.myggdrasilPort = conf.selfPort #check conf file for port to use
        self.mpluginInfo = [] #list to store the plugin information

    #configures server for plugins     
    def setUpPlugins(self):
        #ip and port for bifrost (default)
        feedHandlerInfo = ('bifrost',conf.bifrostIP, conf.bifrostPort, socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.mpluginInfo.append(feedHandlerInfo)
        print "Config data for: ",self.mpluginInfo[0]
        #here is how you would add other plugins (below)
        #odinInfo = ('odin',conf.odinIP, conf.odinPort, socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        #self.mpluginInfo.append(odinInfo) #etc etc\
        #print "Config data for: ",self.mpluginInfo[1]

    def method(data): #if Yggdrasil were to run as a plugin itself, it would need a "method"
        #since Yggdrasil isn't running as a method, this doesn't do anthing
        return "This plugin's method has not been implemented yet"

    def handShake(self):
        return None
        #Yggdrasil doesn't need a separate handshake def either, since it's not running as plugin

    def start(self):
        #get plugins ready to go (gets all of them ready)
        self.setUpPlugins()

        BUFFER_SIZE = 1024
        for plugin in self.mpluginInfo:
            rc=os.fork()
            if rc==0:
                pluginFound=0

                #for the handshake
                prompt = "I am " + self.mname

                #attempt to connect to plugin
                while pluginFound==0:
                    try:
                        plugin[3].connect((plugin[1],plugin[2]))
                        pluginFound=1
                    except:
                        print "Looking for", plugin[0], "..."
                        time.sleep(5)

                #now we're connected, send handshake
                plugin[3].send(prompt)
                #receive response
                data = plugin[3].recv(BUFFER_SIZE)
                print "response: " + data
                #verify it's bifrost
                if(data == "I am ", plugin[0]):
                    print "sending connection information for", plugin[0]
                    #tell bifrost the available port
                    plugin[3].send(str(plugin[2]+1))
                else:
                    # Connection is not Yggdrasil, loop around and check next connection
                    print "Not", plugin[0]
                    recData = "I DON'T KNOW YOU!"
                    conn.send(recData)

                #boot up yggdrasil server application
                print "ip=",self.myggdrasilIp," port=",plugin[2]+1
                plugin[4].bind((self.myggdrasilIp, plugin[2]+1))
                plugin[4].listen(1)
                #close down client connection to bifrost, indicating we are ready for bifrost to connect to us now
                plugin[3].close()

                conn, addr = plugin[4].accept()
                #accept client connection from bifrost
                print 'Connection from:',addr
                while 1:
                    #send bifrost our test xml
                    #testXML = '<?xml version="1.0"?><data><ticker symbol="FB" market="DJI"><field>s</field><field>n</field><field>o</field><field>l1</field><field>p</field></ticker><ticker symbol="IBM" market="DJI"><field>n</field><field>s</field><field>l1</field><field>o</field><field>p</field></ticker><ticker symbol="GOOG" market="IXIC"><field>n</field><field>l1</field><field>s</field><field>o</field><field>p</field></ticker><ticker symbol="^XAU" market="DJI"><field>n</field><field>s</field><field>l1</field><field>o</field><field>p</field></ticker></data>'
                    if plugin[0]=="bifrost":
                        xmlfile = open("odin")
                        xmldat = xmlfile.read()
                        print "sending bifrost XML"
                        #testXML = '<?xml version="1.0"?><data><ticker symbol="FB" market="DJI"><field>s</field><field>n</field><field>o</field><field>l1</field><field>p</field></ticker><ticker symbol="IBM" market="DJI"><field>n</field><field>s</field><field>l1</field><field>o</field><field>p</field></ticker><ticker symbol="GOOG" market="IXIC"><field>n</field><field>l1</field><field>s</field><field>o</field><field>p</field></ticker><ticker symbol="^XAU" market="DJI"><field>n</field><field>s</field><field>l1</field><field>o</field><field>p</field></ticker></data>'
                        conn.send(xmldat)
                    if plugin[0]=="odin":
                        xmlfile = open("bifrost")
                        xmldat = xmlfile.read()
                        try:
                            conn.send(xmldat)
                        except:
                            print "odin has left"

                    #receive data back from bifrost
                    print "receving data"
                    data = conn.recv(BUFFER_SIZE)
                    f = open(plugin[0],'w')
                    f.write(data)
                    f.close()
                    #if not data: break
                    #print data for debug purposes
                    #print "received data from ",plugin[0],":", data
                    print "got data: ",data
                    time.sleep(5)
                #quit on close
                conn.close()
            else:
                print "Oh man, gotta use protection next time. Now I have a child named ",rc
        while 1:
            #print "I'm a babysitter. I kill the children when I leave. Probably get terrible reviews on craigslist..."
            time.sleep(1)
            #inputPipe = open("pipe","r",0)
            #print "parent got ",inputPipe.read()

# start Yggdrasil
if __name__ == '__main__':
    a = Yggdrasil()
    a.start()
