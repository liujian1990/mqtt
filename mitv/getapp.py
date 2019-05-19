# -*- coding: utf-8 -*-

import socket
import struct
import time
import random
import json

#竟然是http协议
host=socket.gethostbyname('MiTV4A-3483fcd5a1e53c6b.local')

url="http://" + host +":6095/general?action=getVolum"
port=9093
### app名称 appname
bzhan="com.bilibili.tv"
tv="com.dianshijia.newlive"
###
'''def sigint_handler(signum, frame):
  global s
  if s:
    s.close()
signal.signal(signal.SIGINT, sigint_handler)
'''
###
final={"vercode":1,"clientId":1008156}
first_cmd=[
0x55, 0x20, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x10,#bit4  dianshi  all
0x00, 0x00, 0x01, 0x07, 0x27, 0x10, 0x04, 0x02,#0f    0e       07
0x00, 0x00, 0x00, 0xdb, 0x00, 0x00, 0x00, 0x00,#e3    e2       db
0x00, 0x00, 0x00, 0x20]

first_cmd1=[
0x55, 0x20, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x10,#bit4  dianshi  all
0x00, 0x00, 0x01, 0x08, 0x27, 0x10, 0x04, 0x02,#0f    0e       07
0x00, 0x00, 0x00, 0xdc, 0x00, 0x00, 0x00, 0x00,#e3    e2       db
0x00, 0x00, 0x00, 0x20]

first_cmd_dianshi=[
0x55, 0x20, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x10,#bit4  dianshi  all
0x00, 0x00, 0x01, 0x0e, 0x27, 0x10, 0x04, 0x02,#0f    0e       07  08 06 11 10
0x00, 0x00, 0x00, 0xe2, 0x00, 0x00, 0x00, 0x00,#e3    e2       db  dc da e5 e4
0x00, 0x00, 0x00, 0x20]

cmdx=[
0x55, 0x20, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x10,
0x00, 0x00, 0x01, 0x09, 0x27, 0x10, 0x04, 0x02,
0x00, 0x00, 0x00, 0xdd, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x20]
data0 = struct.pack("%dB" % (len(first_cmd)), *first_cmd)
data01 = struct.pack("%dB" % (len(first_cmd1)), *first_cmd1)

data_tv = struct.pack("%dB" % (len(first_cmd_dianshi)), *first_cmd_dianshi)

def genrandm():
    randnum=str(random.random())
    missnum=17-len(randnum)
    randmiss=str(random.randint(1*10**missnum,(10**(missnum+1)-1)))
    return randnum+randmiss

def getapp(appname):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)

    timeup=str(int(round(time.time() * 1000)))+":"+genrandm()

    seltv= {
        "request":True,
        "requestId":timeup,
        "action":0,
        "control":{
            "type":0,
            "method":{
                "methodCallID":0,
                "methodName":"openApp",
                "methodCall":{
                "args":[appname,""],
                "useDataChannelReturn":True
                }
            }
        }
    }
    databody=json.dumps(seltv)+json.dumps(final)
    print databody
    if appname == tv:
        data=data_tv+databody.replace(' ','')
    else:
        data=data0+databody.replace(' ','')
    try:
        s.connect((host, port))
        s.sendall(data)
        print "Send"
        print s.recvfrom(1024)
        s.close()
    except socket.timeout as msg:
        print "getapp",msg
        s.sendall(data01+databody.replace(' ',''))
        print "recv",s.recvfrom(1024)
        s.close()
    except socket.error as msg:
        s.close()
        print port, ":", msg
    except Exception as e:
        s.close()


