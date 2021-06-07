import json
import os
import paho.mqtt.publish as mqtt_publish
mqtt_host = os.getenv('MQTTHOST', 'MQTT-Server')
mqtt_port = os.getenv('MQTTPORT', 1883)

fan_name = os.getenv('FANNAME', 'R510Fan')
temp_sensor_name = os.getenv('TEMPNAME', fan_name + '-tempsensor')

mqtt_control_topic = os.getenv('CONTROLTOPIC', '' + fan_name + '/fansetpoint')
mqtt_fanspeed_topic = os.getenv('STATETOPIC', '' + fan_name + '/fanspeed')
mqtt_client_name = os.getenv('MQTTCLIENTNAME', 'r510-denoiser')
mqtt_ambient_temp_topic = os.getenv(
    'TEMPSTATETOPIC', '' + fan_name + '/ambienttemp')
fan_config_topic = os.getenv('MQTTDISCOVERYTOPIC',
                             'homeassistant/fan/' + fan_name + '/config')
temp_config_topic = os.getenv('MQTTDISCOVERYTOPIC',
                              'homeassistant/sensor/' + temp_sensor_name + '/config')


def publish(topic, payload):
    print("Publishing " +str(payload) + " @" + str(topic))
    mqtt_publish.single(topic, payload,
                    hostname=mqtt_host,
                    client_id=mqtt_client_name,
                    port=mqtt_port,
                    retain=True)


fan_config_template = {
    "name": fan_name,
    "unique_id": fan_name.lower(),
    "device": {
        "manufacturer": "Dell",
        "model": "R510",
        "name": fan_name,
        "identifiers": [
            fan_name.lower()
        ],
        "sw_version": "2.0"
    },
    "command_topic": mqtt_control_topic,
    "percentage_state_topic": mqtt_fanspeed_topic,
    "pct_cmd_t": mqtt_control_topic,
    "payload_on": "auto",
    "payload_off": "1"
}
temp_config_template = {
    "name": temp_sensor_name,
    "unique_id": temp_sensor_name.lower(),
    "device": {
        "manufacturer": "Dell",
        "model": "R510",
        "name": temp_sensor_name,
        "identifiers": [
            temp_sensor_name.lower()
        ],
        "sw_version": "2.0"
    },
    "state_topic": mqtt_ambient_temp_topic,
    "unit_of_measurement": "°C"
}
# publish fan discovery
publish(fan_config_topic, json.dumps(fan_config_template))
# json_template = json.dumps(fan_config_template)
# mqtt_publish.single(fan_config_topic, json_template,
#                     hostname=mqtt_host,
#                     client_id=mqtt_client_name,
#                     port=mqtt_port,
#                     retain=True)
# publish tempsensor discovery
publish(temp_config_topic, json.dumps(temp_config_template))
# mqtt_publish.single(temp_config_topic, json.dumps(temp_config_template),
#                     hostname=mqtt_host,
#                     client_id=mqtt_client_name,
#                     port=mqtt_port,
#                     retain=True)
