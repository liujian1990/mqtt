# _*_ coding:utf-8 _*_
import paho.mqtt.client as mqtt
import light
import PlayMusic
import mitv.micmd as cmd
import mitv.mitv as mi
import paho.mqtt.publish as publish
import mitv.getapp as app
HOST= "ifunhome.top"

mitv=None

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("my/funhome")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print "消息", msg.payload

    global mitv
    if not mitv:
        publish.single(topic="my/funhome", payload="home:" + "tv none", hostname=HOST)
        return

    direct=str(msg.payload)
    response="好的!"
    if direct == "fange":
        PlayMusic.run()
    elif direct == "huange":
        PlayMusic.change()
    elif direct == "chage":
        response=PlayMusic.readlist()

    elif direct == "guange":
        PlayMusic.shutdown()

    elif direct == "guandeng":
        light.off()
    elif direct == "kaideng":
        light.on()

    elif direct == "ontv":
        mitv.sendhandle([cmd.shutdown])
    elif direct == "offtv":
        mitv.sendhandle([cmd.mainpage])
        mitv.sendhandle(mi.shutupcmds)
    elif direct == "addvoice":
        mitv.sendhandle([cmd.voice_add])
    elif direct == "reducevoice":
        mitv.sendhandle([cmd.voice_reduce])
    elif direct == "openbzhan":
        print "B站"
        app.getapp(app.bzhan)
        mitv.sendhandle(mi.bzhancmds)
    elif direct == "changetv":
        mitv.sendhandle([cmd.down_move])
    elif direct == "watchtv":
        print "watchTV"
        app.getapp(app.tv)


    elif direct == "getstatus":
        response="Light:"+str(light.get())

    else:
        print "消息", msg.payload

        return

    print response
    publish.single(topic="my/funhome", payload="home:"+response, hostname=HOST)


    #print(msg.topic+" "+str(msg.payload))
def main():
    global mitv
    print "Start"
    # 实例化电视控制
    mitv = mi.mitv()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOST, 1883, 60) #你的ip

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    print "Start loop."
    client.loop_forever()

if __name__ == '__main__':
    main()
 #    print "0"
 #    mitv = mi.mitv()
 #    print "1"
 #    app.getapp(app.bzhan)
 #    mitv.sendhandle(mi.bzhancmds)