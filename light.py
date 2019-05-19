# _*_ coding:utf-8 _*_

import httplib
import time
import socket

host="light"
port=9000

cmd=["ESPGLED1","ESPKLED1",
     "ESPGLED2","ESPKLED2",
     "ESPGLED3","ESPKLED3"]

cmd_light=["KLIGHT","GLIGHT"]
STATUS="黑着"

def get():
    global STATUS
    return STATUS

def on():
    global STATUS

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, port))
        s.sendall(cmd_light[0])
    except socket.error as msg:
        s.close()
        return msg
    STATUS="亮着呢"
    s.close()
    return "打开了"


def off():
    global STATUS
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, port))
        s.sendall(cmd_light[1])
    except socket.error as msg:
        s.close()
        return msg
    STATUS="黑着"
    s.close()
    return "关了"
#
# while True:
# #    print off()
#     time.sleep(2)
#     print on()
#     time.sleep(3)
#
# print "end"
# '''host="192.168.1.13"
# port=80
# conn = httplib.HTTPConnection("192.168.1.13", 80)
# def check():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.settimeout(1)
#     try:
#         s.connect((host, port))
#     except socket.error as msg:
#         s.close()
#         return False
#     s.close()
#     return True
#
# def get():
#     if not check():
#         return "Server not open."
#     try:
#         conn.request("GET", url="/")
#         return conn.getresponse().read()
#     except httplib.HTTPException as e:
#         return e
#
# def on():
#     if not check():
#         return "Server not open."
#     try:
#         conn.request("GET", url="/on")
#         return conn.getresponse().read()
#     except httplib.HTTPException as e:
#         return e
#
# def off():
#     if not check():
#         return "Server not open."
#     try:
#         conn.request("GET", url="/off")
#         return conn.getresponse().read()
#     except httplib.HTTPException as e:
#         return e
#'''