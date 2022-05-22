from components import mqtt_controller,ipmi_controller
from threading import Thread
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))

    client.subscribe(
        mqtt_controller.mqtt_control_topic)

def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + ": " +
          str(msg.payload.decode('utf-8')))
    payload = msg.payload.decode('utf-8')
    if isinstance(payload, int):
        print ("payload is int")
    elif isinstance(payload, str):
        print ("payload is str")
    else:
        print ("payload unknown type")
        
    if str(payload) == "auto":
        ipmi_controller.set_fanmode(payload)
    elif 0 < int(payload) <= 100:
        ipmi_controller.set_fanspeed(payload)

print("Connecting to" + mqtt_controller.mqtt_host + " Using usr/pw: " + mqtt_controller.mqtt_username + "/" + mqtt_controller.mqtt_password)

getstats = Thread(target=ipmi_controller.scrape_ipmi)
getstats.start()

client = mqtt.Client(mqtt_controller.mqtt_client_name)
client.on_connect = on_connect 
client.on_message = on_message  
client.username_pw_set(mqtt_controller.mqtt_username, mqtt_controller.mqtt_password)
client.connect(mqtt_controller.mqtt_host, mqtt_controller.mqtt_port, 60)
client.loop_forever()  # Start networking daemon
