import os

device_name = os.getenv('DEVICENAME', 'Poweredge-R510')
fan_name = os.getenv('FANNAME', '' + device_name + '-fan')  
mqtt_control_topic = os.getenv('FANCONTROLTOPIC', '' + device_name + '/fansetpoint')
mqtt_fanspeed_topic = os.getenv('FANSTATETOPIC', '' + device_name + '/fanspeed')

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