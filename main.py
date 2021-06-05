import paho.mqtt.client as mqtt
import os
# from components import SSH_controller
import paho.mqtt.publish as mqtt_publish
import json
from numpy import interp

mqtt_host = os.getenv('MQTTHOST', '192.168.1.101')
mqtt_port = os.getenv('MQTTPORT', 1883)
fan_name = os.getenv('FANNAME', 'R510Fan')
mqtt_control_topic = os.getenv('CONTROLTOPIC', '' + fan_name + '/fansetpoint')
mqtt_state_topic = os.getenv('STATETOPIC', '' + fan_name + '/fanspeed')
mqtt_client_name = os.getenv('MQTTCLIENTNAME', 'r510-denoiser')
config_topic = os.getenv('MQTTDISCOVERYTOPIC', 'homeassistant/fan/' + fan_name + '/config')
# config_template = {
#     "name": fan_name,
#     "command_topic": mqtt_control_topic,
#     "percentage_state_topic": mqtt_state_topic,
#     "percentage_command_topic": mqtt_control_topic,
#     "qos": 0,
#     "payload_on": "auto",
#     "payload_off": "1",
# }#
config_template = {
  "name": fan_name,
  "unique_id": fan_name.lower(),
  "device": {
    "manufacturer": "Dell",
    "model": "R510",
    "name": fan_name,
    "identifiers": [
      fan_name.lower()
    ],
    "sw_version": "todo"
  },
  "command_topic": mqtt_control_topic,
  "percentage_state_topic": mqtt_state_topic,
  "pct_cmd_t": mqtt_control_topic,
  "payload_on": "auto",
  "payload_off": "1"
}
json_template = json.dumps(config_template)
mqtt_publish.single(config_topic, json_template,
                    hostname=mqtt_host,
                    client_id=mqtt_client_name,
                    port=mqtt_port,
                    retain=True)


def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt

    client.subscribe(
        mqtt_control_topic)  # Subscribe to the control topic , receive any messages published on it


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    command = msg.payload.decode('utf-8')
    if command == 'CHECKINSTALL':
        print('Doing nothing for now')
    print("Message received-> " + msg.topic + ": " + str(msg.payload.decode('utf-8')))  # Print a received msg
    payload = msg.payload.decode('utf-8')

    if str(payload) == 'auto':
        print('setting to auto')
        os.system("bash /app/dellfanctl.sh auto")
    elif 0 < int(payload) <= 100:
        payload = int(payload)
        ##SAFEGUARD For accidental noise discharges
        safepayload=interp(int(payload), [0,100], [0,60]).round()
        print("setting to " + str(safepayload) + "original payload was:" + str(payload))
        os.system("bash /app/dellfanctl.sh manual")
        os.system("bash /app/dellfanctl.sh set " + str(int(safepayload)))
    else:
        print("Received invalid command, What Do?")


client = mqtt.Client(mqtt_client_name)  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.connect(mqtt_host, 1883, 60)
client.loop_forever()  # Start networking daemon
