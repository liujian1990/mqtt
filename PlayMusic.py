# -*- coding: utf-8 -*-
import webbrowser
import urllib2
import json
import cookielib
import os
import time
import threading
import httplib
URL01= "https://douban.fm/j/v2/playlist?channel=-10&kbps=192&client=s%3Amainsite%7Cy%3A3.0&app_name=radio_website&version=100&type=n"
URL02= "https://douban.fm/j/v2/playlist?channel=-10&kbps=128&client=s%3Amainsite%7Cy%3A3.0&app_name=radio_website&version=100&type=p&sid=1821905&pt=&pb=128&apikey="

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

sid_current = 0
url_current = ""
kpbs_current = 0
length_current = 0
name_current = ""
singer_current = ""
#控制播放
g_isplay = False

import platform

def requests_url(url):
    request = urllib2.Request(url)
    respon = opener.open(request)  # 初始页面
    return respon.read()

def load_current(content):
    global sid_current,url_current,kpbs_current,length_current,name_current,singer_current
    info = json.loads(content,encoding='utf-8',)
    print info
    print json.dumps(info,indent=1)

    sid_current = info['song'][0]['sid']
    url_current = info['song'][0]['url']
    kpbs_current = info['song'][0]['kbps']
    length_current = info['song'][0]['length']
    name_current = info['song'][0]['title']
    singer_current = info['song'][0]['singers'][0]['name']

def begin_song():
    global sd_current,url_current,kpbs_current
    load_current(requests_url(URL01))
    if url_current:
        webbrowser.open(url_current)


def close_webbrowser():
    if 'Windows' in platform.system():
        os.system('taskkill /F /IM chrome.exe')
    if 'Linux' in platform.system():
        os.system('killall chromium-browser')


def next_song():
    global sid_current,url_current,kpbs_current
    if url_current and sid_current and kpbs_current:
        close_webbrowser()
        URL02 = "https://douban.fm/j/v2/playlist?" \
                "channel=-10&kbps="+str(kpbs_current)+"&client=s%3Amainsite%7Cy%3A3.0&" \
                "app_name=radio_website&version=100&type=p&sid="+str(sid_current)+"&pt=&pb="+str(kpbs_current)+"&apikey="
        load_current(requests_url(URL02))
        if url_current:
            webbrowser.open(url_current)

def readlist():
    global g_isplay,name_current,singer_current
    if not g_isplay:
        return "没有放歌！"
    return "当前歌名："+name_current.encode("utf-8") +"\n演唱歌手："+singer_current.encode("utf-8")

#停止播放
def shutdown():
    global g_isplay,url_current
    url_current=""
    g_isplay = False
    close_webbrowser()

#换歌
def change():
    global length_current
    length_current = 0


def play():
    global length_current , g_isplay
    while length_current > 1:
        length_current -= 1
        time.sleep(1)
    print "Next Song!"
    if g_isplay:
        next_song()
        play()
    else:
        return

#放歌
def run():
    global url_current,g_isplay
    if not g_isplay and not url_current:
        g_isplay =True
        begin_song()
    pth = threading.Thread(target=play)
    pth.start()

