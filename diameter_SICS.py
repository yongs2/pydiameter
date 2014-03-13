#!/usr/bin/env python
import datetime
import time

# Testing handling basic AVP types
from libDiameter import *

class SerSessionMsg:
    def __init__(self):
        self.SESSION_ID = 0
        self.HOST_NAME = "dia.SICS.com"
        self.REALM_NAME = "SICS.com"
        self.RECORD_TYPE = 1
        self.RECORD_NUMBER = 0
        self.ACCT_APPLICATION_ID = 1
        self.EVENT_TIMESTAMP = 0
        self.ACCT_SESSION_ID = "0"
        self.USER_NAME = u""
        self.NAS_ID = "nasid001"
        self.NAS_IP = "192.168.0.1"
        self.NAS_PORT = 3868
        self.MAC = ":ffff:ffff:ffff:ffff"
        self.TERMINATION_CAUSE = 0
        self.IN_VOLUME = 0
        self.OUT_VOLUME = 0
        self.ACCT_SESSION_TIME = 0
        self.FRAMED_IP_ADDRESS = "192.168.0.11"
        self.GIADDR = u"192.168.0.1@test.SICS.com"
        self.UACS_ACCOUTING = u"UACS_ACCOUTING"

    def CreateMsg(self):
        AVP=[]
        AVP.append(encodeAVP("Origin-Host", self.HOST_NAME ))
        AVP.append(encodeAVP("Origin-Realm", self.REALM_NAME))
        AVP.append(encodeAVP("Destination-Realm", self.REALM_NAME))
        AVP.append(encodeAVP("Accounting-Record-Type", self.RECORD_TYPE))
        AVP.append(encodeAVP("Accounting-Record-Number", self.RECORD_NUMBER))
        AVP.append(encodeAVP("Acct-Application-Id", self.ACCT_APPLICATION_ID))
        AVP.append(encodeAVP("User-Name", self.USER_NAME))
        AVP.append(encodeAVP("Event-Timestamp", time.time()))
        AVP.append(encodeAVP("Acct-Session-Id", self.ACCT_SESSION_ID))
        AVP.append(encodeAVP("NAS-Identifier", self.NAS_ID))
        AVP.append(encodeAVP("NAS-IP-Address", self.NAS_IP))
        AVP.append(encodeAVP("NAS-Port", self.NAS_PORT))
        AVP.append(encodeAVP("Termination-Cause", self.TERMINATION_CAUSE))
        AVP.append(encodeAVP("Accounting-Input-Octets", self.IN_VOLUME))
        AVP.append(encodeAVP("Accounting-Output-Octets", self.OUT_VOLUME))
        AVP.append(encodeAVP("Acct-Session-Time", self.ACCT_SESSION_TIME))
        AVP.append(encodeAVP("Calling-Station-Id", self.MAC))
        AVP.append(encodeAVP("Framed-IP-Address", self.FRAMED_IP_ADDRESS))
        AVP.append(encodeAVP("GIADDR", self.GIADDR))
        AVP.append(encodeAVP("UACS-Accounting", self.UACS_ACCOUTING))

        ACR=HDRItem()
        # Set command code
        ACR.cmd=dictCOMMANDname2code("Accounting")
        # Set Hop-by-Hop and End-to-End
        initializeHops(ACR)
        # Add AVPs to header and calculate remaining fields
        msg=createReq(ACR, AVP)
        # msg now contains ACR Request as hex string
        return msg

    def DecodeMsg(self, msg):
        H = HDRItem()
        stripHdr(H,msg)
        avps = splitMsgAVPs(H.msg)
        cmd = dictCOMMANDcode2name(H.flags,H.cmd)
        if cmd == ERROR:
            print 'Unknown command',H.cmd
        else:
            print cmd
        #print "Hop-by-Hop=",H.HopByHop,"End-to-End=",H.EndToEnd,"ApplicationId=",H.appId
        for avp in avps:
            if isinstance(avp,tuple):
                (Name,Value)=avp
            else:
                (Name,Value)=decodeAVP(avp)
            
            #print "decode, |%s|" % (Name)

            if Name == 'Origin-Host'                : self.HOST_NAME = Value
            if Name == "Origin-Realm"               : self.REALM_NAME = Value
            if Name == "Destination-Realm"          : self.REALM_NAM = Value
            if Name == "Accounting-Record-Type"     : self.RECORD_TYPE = Value
            if Name == "Accounting-Record-Number"   : self.RECORD_NUMBER = Value
            if Name == "Acct-Application-Id"        : self.ACCT_APPLICATION_ID = Value
            if Name == "User-Name"                  : self.USER_NAME = Value
            if Name == "Event-Timestamp"            : self.EVENT_TIMESTAMP = Value
            if Name == "Acct-Session-Id"            : self.ACCT_SESSION_ID= Value
            if Name == "NAS-Identifier"             : self.NAS_ID = Value
            if Name == "NAS-IP-Address"             : self.NAS_IP = Value
            if Name == "NAS-Port"                   : self.NAS_PORT = Value
            if Name == "Termination-Cause"          : self.TERMINATION_CAUSE = Value
            if Name == "Accounting-Input-Octets"    : self.IN_VOLUME = Value
            if Name == "Accounting-Output-Octets"   : self.OUT_VOLUME = Value
            if Name == "Acct-Session-Time"          : self.ACCT_SESSION_TIME = Value
            if Name == "Calling-Station-Id"         : self.MAC = Value
            if Name == "Framed-IP-Address"          : self.FRAMED_IP_ADDRESS = Value
            if Name == "GIADDR"                     : self.GIADDR = Value
            if Name == "UACS-Accounting"            : self.UACS_ACCOUTING = Value
            
        #print "="*30 + ", Done"

    def PrintMsg(self):
        print "|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|" % (
                self.SESSION_ID, self.HOST_NAME, 
                self.REALM_NAME, self.RECORD_TYPE.encode("hex"), 
                self.RECORD_NUMBER, self.USER_NAME.encode("utf-8"), 
                self.ACCT_SESSION_ID, self.EVENT_TIMESTAMP, 
                self.TERMINATION_CAUSE.encode("hex"), 
                self.IN_VOLUME, self.OUT_VOLUME, 
                self.ACCT_SESSION_TIME, self.MAC.encode("utf-8"), 
                self.GIADDR.encode("utf-8"))

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)
    LoadDictionary("dictDiameter.xml")
    MSG_SIZE=4096

    for RECORD_TYPE in ["Start Record", "Interim Record", "Interim Record", "Interim Record", "Stop Record"] :

        ACR = SerSessionMsg()
        ACR.USER_NAME = u'pi: \u03c0'

        ACR.RECORD_TYPE = RECORD_TYPE
        ACR.RECORD_NUMBER = ACR.RECORD_NUMBER + 1
        ACR.IN_VOLUME = 10
        ACR.OUT_VOLUME = 10
        ACR.ACCT_SESSION_TIME = 20

        print "ACR.CreateMsg.....(%s,%d)" % (ACR.RECORD_TYPE, ACR.RECORD_NUMBER)
        msg = ACR.CreateMsg()
        #print msg
        #print "="*30
        try:
            # Fire to test server for verification with wireshark
            # I use dummy-server.py
            HOST="localhost"
            PORT=3868
            # Connect to server
            Conn=Connect(HOST,PORT)
            # send data
            Conn.send(msg.decode("hex"))
            #print "+"*30
            ACR.DecodeMsg(msg)
            ACR.PrintMsg()
            print "="*50

            # Receive response
            received = Conn.recv(MSG_SIZE)

            ACA = SerSessionMsg()
            ACA.DecodeMsg(received.encode("hex"))
            ACA.PrintMsg()
            print "-"*50

            Conn.close()
        except:
            pass

        time.sleep (50.0 / 1000.0);

    print "Loop Done..............................."
