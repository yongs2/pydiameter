#!/usr/bin/env python

##################################################################
# Copyright (c) 2012, Sergej Srepfler <sergej.srepfler@gmail.com>
# February 2012 - 
# Version 0.3.1, Last change on Nov 17, 2012
# This software is distributed under the terms of BSD license.    
##################################################################

# Diameter Test Simulator 
# simple TCP echo of diameter packets :-> REQ->RES only
# by changing Flag in header
# interrupt the program with Ctrl-C

import sys
import socket
import thread
import time
import string
import struct
import logging

# Readable time format
def now( ):
    return time.ctime(time.time( )) 

def DiameterECHO(connection,address):
    while True:                    
        #get input ,wait if no data
        #connection.setblocking(True)
        logging.warning("DiameterECHO.....")
        try:
            data=connection.recv(BUFFER_SIZE)
        except:
            break
        #suspect more data (try to get it all without stopping if no data)
        if len(data)==BUFFER_SIZE:
            while 1:
                #connection.setblocking(False)
                try:
                    data+=connection.recv(BUFFER_SIZE, socket.MSG_DONTWAIT)
                except:
                    #error means no more data
                    break
        #no data found exit loop (posible closed socket)
        if len(data)==0:
            break
        else:
            res=data[:4]+chr(ord(data[4])&127)+data[5:]
            logging.warning(("IN:",len(data),"OUT:",len(res)))
            connection.sendall(res)
    connection.close()
    
if __name__ == "__main__":
    # level for decoding are: DEBUG, INFO, WARNING, ERROR, CRITICAL
    # logging.basicConfig(filename='/path/to/your/log', level=logging.INFO)
    logging.basicConfig(level=logging.INFO)
    
    # Define server_host:port to use (empty string means localhost)
    HOST = ""
    PORT = 3868

    BUFFER_SIZE =1024       # Limit buffer size to detect complete message
    MAX_CLIENTS=5           # This is simulator - more makes no sense

    
    ####################################################################
    # Server: spawns a thread to handle each client connection
    # threads work on standard Windows systems, but process forks do not
    ####################################################################
    # I could not get ThreadingTCPserver to work 
   
    # Create the server, binding to HOST:PORT
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # fix "Address already in use" error upon restart
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))  
    server.listen(MAX_CLIENTS)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    while True:
        connection, address = server.accept( )
        dbg='Connected', address,'at', now( )
        logging.warning(dbg)
        thread.start_new(DiameterECHO, (connection,address))

    server.socket.close()
######################################################        
# History
# 0.3.1 - Nov 17, 2012 - initial version

