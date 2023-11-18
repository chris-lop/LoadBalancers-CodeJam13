import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("CodeJam")

def on_message(client, userdata, msg):
    # send truck events to truck function
    payload = json.loads(msg.payload.decode())
    print(payload)
    if(payload["type"] == "truck"):
        init_truck()
    #print(msg.topic+" "+str(msg.payload))

def init_truck():
    # initialize truck
    print("Truck initialized")

client = mqtt.Client(client_id="LoadBalancers01")
client.username_pw_set("CodeJamUser", "123CodeJam")
client.on_connect = on_connect
client.on_message = on_message

client.connect("fortuitous-welder.cloudmqtt.com", 1883, 60)
client.loop_forever()
