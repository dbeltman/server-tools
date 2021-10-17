from components import mqtt_controller,ipmi_controller
from threading import Thread
import paho.mqtt.client as mqtt

# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    # Print result of connection attempt
    print("Connected with result code {0}".format(str(rc)))

    client.subscribe(
        mqtt_controller.mqtt_control_topic)  # Subscribe to the control topic , receive any messages published on it

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + ": " +
          str(msg.payload.decode('utf-8')))  # Print a received msg
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


# getstats = Thread(target=ipmi_controller.get_ipmi_stats)
getstats = Thread(target=ipmi_controller.scrape_ipmi)
getstats.start()

client = mqtt.Client(mqtt_controller.mqtt_client_name)
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.connect(mqtt_controller.mqtt_host, 1883, 60)
client.loop_forever()  # Start networking daemon
