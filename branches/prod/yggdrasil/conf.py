#########################################################
#                                                       #
#   Chirs Weir                                          #
#   Tondiggidy Simonutti                                #
#   T0ng Liu                                            #
#   Codigail Doyle                                      #
#                                                       #
#   RPI Software Design and Documentation Fall 2014     #
#                                                       #
#   conf.py                                             #
#                                                       #
#########################################################


#config file
#make sure you set the IP's to your IP
#if you don't it will break.
#Don't use ports that don't work

class conf:
    identity = "yggdrasil"
    selfPort = 1337

    bifrostName = "bifrost"
    bifrostIP = "192.168.1.136"
    bifrostPort = 1437

    dbName = "fragg"
    dbIP = "192.168.1.136"
    dbPort = 1339

    odinName = "odin"
    odinIP = "192.168.1.136"
    odinPort = 1537

    #odinName = "Ratatoskr"
    #odinIP = "192.168.1.99"
    #odinPort = 1010
