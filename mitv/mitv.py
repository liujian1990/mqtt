# -*- coding: utf-8 -*-

import socket
import struct
import binascii
import time
from micmd import *

cmd_counts=0x00
host=socket.gethostbyname('MiTV4A-3483fcd5a1e53c6b.local')
url="http://"+host+":6095/general?action=getVolum"
port=6091

shutupcmds=[mainpage,shutdown, right_move,right_move,ok]
bzhancmds=[right_move,down_move,ok,right_move,ok,ok]
class mitv():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(3)
        self.retry=0
        try:
            self.s.connect((host, port))
        except socket.error as msg:
            self.s.close()
            exit(-1)
        print "Port",port,"Connected!"
        self.first()

    def first(self):
        data0 = struct.pack("%dB" % (len(first_cmd)), *first_cmd)
        self.s.sendall(data0)
        print "Recv system info:",self.s.recv(1024)

    def sendhandle(slef,cmds):
        global cmd_counts
        for cmd in cmds:    #cmd[0][8]
            cmd_counts=cmd_counts+1
            cmd[0][7]=cmd_counts
            data0 = struct.pack("%dB" % (len(cmd[0])), *cmd[0])
            cmd_counts=cmd_counts+1
            cmd[1][7]=cmd_counts
            data1 = struct.pack("%dB" % (len(cmd[1])), *cmd[1])
            try:
                slef.s.sendall(data0)
     #       print "recv:",str(binascii.b2a_hex(slef.s.recv(1024)))
                slef.s.sendall(data1)
    #        print "recv:",str(binascii.b2a_hex(slef.s.recv(1024)))
            except socket.timeout :
                slef.s.connect(host,port)
                slef.sendhandle(cmds)
                slef.retry+=1
                if slef.retry==10:
                    return
            except Exception as e:
                print e
                return
'''
first()

cmds=[
    esc,esc,
    voice_add,voice_add,
    voice_add, voice_add,
    voice_reduce,voice_reduce,
    voice_reduce, voice_reduce,
    menu, mainpage,
    shutdown, right_move,right_move,ok,shutdown
    ]
sendhandle(cmds)
s.close()
'''

