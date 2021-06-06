import os
from components import mqtt_controller
from numpy import interp
from threading import Thread
from time import sleep
import paho.mqtt.client as mqtt

def get_ipmi_stats():
    while True:
        ipmistats = os.popen("bash /app/dellfanctl.sh simplestats").read()
        # print(str(ipmistats))
        ipmistatlist = ipmistats.split("\n")
        ipmifanspeed = round(int(ipmistatlist[1]) / 11000 * 100)
        ipmitemp = int(ipmistatlist[0])
        print("Fan speed: " + str(ipmifanspeed) +
              "% | Ambient Temperature: " + str(ipmitemp))
        print("Publishing Fanspeed")              
        mqtt_controller.publish(mqtt_controller.mqtt_fanspeed_topic, ipmifanspeed)
        print("Publishing Ambient temperature")                           
        mqtt_controller.publish(mqtt_controller.mqtt_ambient_temp_topic, ipmitemp)
        sleep(60)


# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    # Print result of connection attempt
    print("Connected with result code {0}".format(str(rc)))

    client.subscribe(
        mqtt_controller.mqtt_control_topic)  # Subscribe to the control topic , receive any messages published on it


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    command = msg.payload.decode('utf-8')
    if command == 'CHECKINSTALL':
        print('Doing nothing for now')
    print("Message received-> " + msg.topic + ": " +
          str(msg.payload.decode('utf-8')))  # Print a received msg
    payload = msg.payload.decode('utf-8')

    if str(payload) == 'auto':
        print('setting to auto')
        os.system("bash /app/dellfanctl.sh auto")
    elif 0 < int(payload) <= 100:
        payload = int(payload)
        # SAFEGUARD For accidental noise discharges
        safepayload = interp(int(payload), [0, 100], [0, 60]).round()
        print("setting to " + str(safepayload) +
              "original payload was:" + str(payload))
        os.system("bash /app/dellfanctl.sh manual")
        os.system("bash /app/dellfanctl.sh set " + str(int(safepayload)))
    else:
        print("Received invalid command, What Do?")


t = Thread(target=get_ipmi_stats)
t.start()
# Create instance of client with client ID “digi_mqtt_test”
client = mqtt.Client(mqtt_controller.mqtt_client_name)
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.connect(mqtt_controller.mqtt_host, 1883, 60)
client.loop_forever()  # Start networking daemon
