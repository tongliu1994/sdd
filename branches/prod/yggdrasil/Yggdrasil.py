#########################################################
#                                                       #
#   Chirs Weir                                          #
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

#for catching ctrl-c and ensuring children exit
def signal_handler(signal, frame):
    print "Caught ctrl-c, killing children..."
    print "Goodbye",os.getpid()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#main class
class Yggdrasil:
    def __init__(self):
        self.mname = conf.identity #identity string from conf.py
        self.myggdrasilIp = '' #default IP (your own)
        self.myggdrasilPort = conf.selfPort #server port from conf.py
        self.mpluginInfo = [] #array for storing plugin info

    #sets up plugins
    def setUpPlugins(self):
        #ip and port for bifrost (default)
        feedHandlerInfo = ('bifrost',conf.bifrostIP, conf.bifrostPort, socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.mpluginInfo.append(feedHandlerInfo) #adds to plugin info (new plugin added to list)
        #print "Config data for: ",self.mpluginInfo[0] #debug
        #below is how you would add another plugin if odin worked the same way
        #odinInfo = ('odin',conf.odinIP, conf.odinPort, socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        #self.mpluginInfo.append(odinInfo) #etc etc\
        #print "Config data for: ",self.mpluginInfo[1]

    #these two methods are provided for compatibility with the plugin class
    def method(data): #yggdrasil provides the same methods as a plugin class, but doesn't need this one
        return "This plugin's method has not been implemented yet"

    def handShake(self): #yggdrasil initiates the handshake, so this method isn't needed either
        return None

    def start(self): #start server
        self.setUpPlugins() #get plugin configs

        BUFFER_SIZE = 102400 #buffer for xmldata
        for plugin in self.mpluginInfo: #for every plugin we have...
            rc=os.fork() #create a new thread
            if rc==0: #if child
                pluginFound=0 #look for plugin at the specified IP (in the config)

                #for the handshake
                prompt = "I am " + self.mname #ident to send to plugin

                #attempt to connect to plugin
                while pluginFound==0:
                    try:
                        plugin[3].connect((plugin[1],plugin[2]))
                        pluginFound=1
                    except:
                        #if we can't connect, try again
                        print "Looking for", plugin[0], "..."
                        time.sleep(5) #don't spam people

                #now we're connected, send handshake
                plugin[3].send(prompt)
                #receive response
                data = plugin[3].recv(BUFFER_SIZE)
                print "response: " + data
                #verify it's the right plugin
                if(data == "I am ", plugin[0]):
                    print "sending connection information for", plugin[0]
                    #tell the plugin the available port
                    plugin[3].send(str(plugin[2]+1))
                else:
                    # Connection is undefined, loop around and check next connection
                    print "Not", plugin[0]
                    recData = "I DON'T KNOW YOU!"
                    conn.send(recData)

                #boot up yggdrasil server application
                print "ip=",self.myggdrasilIp," port=",plugin[2]+1
                plugin[4].bind((self.myggdrasilIp, plugin[2]+1))
                plugin[4].listen(1)
                #close down client connection to the plugin, indicating we are ready for it to connect to us now
                plugin[3].close()

                conn, addr = plugin[4].accept()
                #accept client connection from plugin
                print 'Connection from:',addr
                while 1:
                    #send plugin the xml
                    if plugin[0]=="bifrost": #since plugins are handled differently, we take care of that here
                        xmlfile = open("odin") #open the xml dumped from odin
                        xmldat = xmlfile.read()
                        print "sending bifrost XML: ",xmldat,"ENDDATA"
                        conn.send(xmldat)
                    if plugin[0]=="odin": #support for a possible odin plugin
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
                    f.write(data) #dump data to odin (or whatever plugins are listening)
                    f.close()
                    #if not data: break
                    #print data for debug purposes
                    #print "received data from ",plugin[0],":", data
                    print "got data: ",data
                    time.sleep(5) #avoid spam!
                #quit on close
                conn.close()
            else:
                print "Spawing child process with pid ",rc
        while 1:
            #print "I'm a babysitter. I kill the children when I leave. Probably get terrible reviews on craigslist..."
            time.sleep(1)
            #this is the parent process, it watches the children and catches ctrl-c to kill them

# main start
if __name__ == '__main__':
    a = Yggdrasil()
    a.start()
