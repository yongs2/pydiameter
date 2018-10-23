#!/usr/bin/env python
# python version 2.7

import datetime
import time

# Testing handling basic AVP types
from libDiameter import *

class ShMsg:
    def __init__(self):
        self.SESSION_ID = "12;presence.open-ims.test;1;"
        self.HOST_NAME = "presence.open-ims.test"
        self.REALM_NAME = "open-ims.test"
        self.DESTINATION_REALM = "open-ims.test"
        self.DESTINATION_HOST = "hss.open-ims.test"
        self.AUTH_SESSION_STATE = 1
        self.USER_IDENTITY = "PUID"
        self.SERVICE_INDICATION = "MMTEL-Services"
        self.SEND_DATA_INDICATION = 1
        self.SERVER_NAME = "sip:HSS_SERVER_NAME"
        self.SUBS_REQ_TYPE = 0
        self.DATA_REFERENCE = 0
        self.EXPIRY_TIME = 0
        self.USER_NAME = "PRID"
        self.VENDOR_ID = 10415
        self.AUTH_APP_ID = 16777217

    def create_CER(self):
        ORIGIN_ID=1 #str(datetime.datetime.now().microsecond)
        # Let's build CER
        CER_avps=[]
        CER_avps.append(encodeAVP("Origin-Host", self.HOST_NAME))
        CER_avps.append(encodeAVP("Origin-Realm", self.REALM_NAME))
        CER_avps.append(encodeAVP("Vendor-Id", dictVENDORid2code('TGPP')))
        CER_avps.append(encodeAVP("Origin-State-Id", ORIGIN_ID))
        CER_avps.append(encodeAVP("Supported-Vendor-Id", dictVENDORid2code('TGPP')))
        CER_avps.append(encodeAVP("Acct-Application-Id", self.AUTH_APP_ID))
        # Create message header (empty)
        CER=HDRItem()
        # Set command code
        CER.cmd=dictCOMMANDname2code("Capabilities-Exchange")
        CER.appId = self.AUTH_APP_ID
        # Set Hop-by-Hop and End-to-End
        initializeHops(CER)
        # Add AVPs to header and calculate remaining fields
        msg=createReq(CER,CER_avps)
        # msg now contains CER Request as hex string
        return msg

    def create_DWR(self):
        ORIGIN_ID=1 #str(datetime.datetime.now().microsecond)
        DWR_avps=[]
        DWR_avps.append(encodeAVP('Origin-Host', self.HOST_NAME))
        DWR_avps.append(encodeAVP('Origin-Realm', self.REALM_NAME))
        DWR_avps.append(encodeAVP('Host-IP-Address', "192.168.0.230"))
        DWR_avps.append(encodeAVP("Vendor-Id", dictVENDORid2code('TGPP')))
        DWR_avps.append(encodeAVP('Product-Name', "presence.open-ims.test"))
        DWR_avps.append(encodeAVP("Origin-State-Id", ORIGIN_ID))
        DWR_avps.append(encodeAVP("Supported-Vendor-Id", dictVENDORid2code('TGPP')))
        DWR_avps.append(encodeAVP("Inband-Security-Id", 0))
        DWR_avps.append(encodeAVP("Acct-Application-Id", self.AUTH_APP_ID))
        DWR_avps.append(encodeAVP("Vendor-Specific-Application-Id",
                        [
                            encodeAVP("Vendor-Id", self.VENDOR_ID),
                            encodeAVP('Auth-Application-Id', self.AUTH_APP_ID)
                        ]))
        DWR=HDRItem()
        DWR.cmd=dictCOMMANDname2code('Device-Watchdog')
        DWR.appId = self.AUTH_APP_ID
        initializeHops(DWR)
        msg=createReq(DWR,DWR_avps)
        return msg

    def Create_SNR(self):
        AVP=[]
        ExpiryTime = datetime.datetime.now() + datetime.timedelta(hours=365)
        self.EXPIRY_TIME = time.mktime(ExpiryTime.timetuple())
        AVP.append(encodeAVP("Session-Id", self.SESSION_ID ))
        AVP.append(encodeAVP("Origin-Realm", self.REALM_NAME))
        AVP.append(encodeAVP("Origin-Host", self.HOST_NAME))
        AVP.append(encodeAVP("Destination-Realm", self.DESTINATION_REALM))
        AVP.append(encodeAVP("Destination-Host", self.DESTINATION_HOST))
        AVP.append(encodeAVP("Auth-Session-State", self.AUTH_SESSION_STATE))
        AVP.append(encodeAVP("Vendor-Specific-Application-Id",
                    [
                        encodeAVP("Vendor-Id", self.VENDOR_ID),
                        encodeAVP('Auth-Application-Id', self.AUTH_APP_ID)
                    ]))
        AVP.append(encodeAVP("User-Identity", 
                    [
                        encodeAVP('Public-Identity', self.USER_IDENTITY),
                    ]))
        AVP.append(encodeAVP("Service-Indication", self.SERVICE_INDICATION))
        AVP.append(encodeAVP("Send-Data-Indication", self.SEND_DATA_INDICATION))
        AVP.append(encodeAVP("Server-Name", self.SERVER_NAME))
        AVP.append(encodeAVP("Subs-Req-Type", self.SUBS_REQ_TYPE))
        AVP.append(encodeAVP("Data-Reference", self.DATA_REFERENCE))
        AVP.append(encodeAVP("Expiry-Time", self.EXPIRY_TIME))
        AVP.append(encodeAVP("3GPP-IMSI", self.USER_NAME))

        SNR=HDRItem()
        # Set command code
        SNR.cmd=dictCOMMANDname2code("Subscribe-Notifications")
        SNR.appId = self.AUTH_APP_ID

        # Set Hop-by-Hop and End-to-End
        initializeHops(SNR)
        # Add AVPs to header and calculate remaining fields
        msg=createReq(SNR, AVP)
        # msg now contains SNR Request as hex string
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
            if Name == "Session-Id"                 : self.SESSION_ID = Value
            
        #print "="*30 + ", Done"

    def PrintMsg(self):
        print "|%s|%s|%s|" % (
                self.SESSION_ID, self.HOST_NAME, self.REALM_NAME)

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)
    LoadDictionary("dictDiameter.xml")
    MSG_SIZE=4096

    for RECORD_TYPE in ["Start Record"] :

        shMsg = ShMsg()

        #print msg
        #print "="*30
        try:
            # Fire to test server for verification with wireshark
            # I use dummy-server.py
            HOST="192.168.0.210"
            PORT=3868
            # Connect to server
            Conn=Connect(HOST,PORT)

            print "CER.CreateMsg.....(%s)" % (shMsg.SESSION_ID)
            # send CER
            msg=shMsg.create_CER()
            Ret=Conn.send(msg.decode("hex"))
            print ">> Send (%d)" % (Ret)
            print "="*50
            # Receive response
            received = Conn.recv(MSG_SIZE)
            print ">> Recv (%d)" % (len(received))
            CEA = ShMsg()
            CEA.DecodeMsg(received.encode("hex"))
            CEA.PrintMsg()
            print "-"*50

            print "DWR.CreateMsg.....(%s)" % (shMsg.SESSION_ID)
            # send CER
            msg=shMsg.create_DWR()
            Ret=Conn.send(msg.decode("hex"))
            print ">> Send (%d)" % (Ret)
            print "="*50
            # Receive response
            received = Conn.recv(MSG_SIZE)
            print ">> Recv (%d)" % (len(received))
            DWA = ShMsg()
            DWA.DecodeMsg(received.encode("hex"))
            DWA.PrintMsg()
            print "-"*50

            print "SNR.CreateMsg.....(%s)" % (shMsg.SESSION_ID)
            msg = shMsg.Create_SNR()    
            # send SNR
            Ret=Conn.send(msg.decode("hex"))
            print ">> Send (%d)" % (Ret)
            shMsg.DecodeMsg(msg)
            shMsg.PrintMsg()
            print "="*50

            # Receive response
            received = Conn.recv(MSG_SIZE)
            print ">> Recv (%d)" % (len(received))
            SNA = ShMsg()
            SNA.DecodeMsg(received.encode("hex"))
            SNA.PrintMsg()
            print "-"*50

            Conn.close()
        except Exception as ex:
            print "Exception (%s)" % (ex)

        time.sleep (50.0 / 1000.0);

    print "Loop Done..............................."
