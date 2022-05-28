import os

device_name = os.getenv('DEVICENAME', 'Poweredge-R510')
button_name = os.getenv('CHASSISPOWERNAME', device_name + '-powerbutton')
mqtt_button_topic = os.getenv('CHASSISPOWERTOPIC', '' + button_name + '/commands')

chassispower_config_template = {
    "name": button_name,
    "unique_id": button_name.lower(),
    "device": {
        "manufacturer": "Dell",
        "model": "R510",
        "name": device_name,
        "identifiers": [
            device_name.lower()
        ],
        "sw_version": "2.0"
    },
    "state_topic": mqtt_button_topic,
    "entity_category": "config",
    "payload_press": "poweron"
}