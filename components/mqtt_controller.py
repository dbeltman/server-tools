import json
import os
import paho.mqtt.publish as mqtt_publish
mqtt_host = os.getenv('MQTTHOST', 'MQTT-Server')
mqtt_port = os.getenv('MQTTPORT', 1883)

device_name = os.getenv('DEVICENAME', 'Poweredge-R510')
fan_name = os.getenv('FANNAME', '' + device_name + '-fan')  
temp_sensor_name = os.getenv('TEMPNAME', device_name + '-tempsensor')
power_sensor_name = os.getenv('POWERNAME', device_name + '-powersensor')
energy_sensor_name = os.getenv('ENERGYNAME', device_name + '-energysensor')

mqtt_control_topic = os.getenv('CONTROLTOPIC', '' + device_name + '/fansetpoint')
mqtt_fanspeed_topic = os.getenv('STATETOPIC', '' + device_name + '/fanspeed')
mqtt_power_topic = os.getenv('POWERSTATETOPIC', '' + power_sensor_name + '/powerusage')
mqtt_energy_topic = os.getenv('ENERGYSTATETOPIC', '' + power_sensor_name + '/energyusage')

mqtt_client_name = os.getenv('MQTTCLIENTNAME', 'r510-denoiser')
mqtt_ambient_temp_topic = os.getenv('TEMPSTATETOPIC', '' + device_name + '/ambienttemp')
fan_config_topic = os.getenv('MQTTDISCOVERYTOPIC',
                             'homeassistant/fan/' + device_name + '/config')
temp_config_topic = os.getenv('MQTTDISCOVERYTOPIC',
                              'homeassistant/sensor/' + temp_sensor_name + '/config')
power_config_topic = os.getenv('MQTTDISCOVERYTOPIC',
                              'homeassistant/sensor/' + power_sensor_name + '/config')
energy_config_topic = os.getenv('MQTTDISCOVERYTOPIC',
                              'homeassistant/sensor/' + energy_sensor_name + '/config')                              

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
        "name": device_name,
        "identifiers": [
            device_name.lower()
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
        "name": device_name,
        "identifiers": [
            device_name.lower()
        ],
        "sw_version": "2.0"
    },
    "state_topic": mqtt_ambient_temp_topic,
    "unit_of_measurement": "°C"
}
power_config_template = {
    "name": power_sensor_name,
    "unique_id": power_sensor_name.lower(),
    "device_class": "power",
    "device": {
        "manufacturer": "Dell",
        "model": "R510",
        "name": device_name,
        "identifiers": [
            device_name.lower()
        ],
        "sw_version": "2.0"
    },
    "state_topic": mqtt_power_topic,
    "unit_of_measurement": "W"
}
energy_config_template = {
    "name": energy_sensor_name,
    "unique_id": energy_sensor_name.lower(),
    "device_class": "energy",
    "state_class": "total_increasing",
    "device": {
        "manufacturer": "Dell",
        "model": "R510",
        "name": device_name,
        "identifiers": [
            device_name.lower()
        ],
        "sw_version": "2.0"
    },
    "state_topic": mqtt_energy_topic,
    "unit_of_measurement": "kWh"
}
# publish fan discovery
publish(fan_config_topic, json.dumps(fan_config_template))
publish(power_config_topic, json.dumps(power_config_template))
publish(energy_config_topic, json.dumps(energy_config_template))

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
