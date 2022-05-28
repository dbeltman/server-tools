import os

device_name = os.getenv('DEVICENAME', 'Poweredge-R510')
button_name = os.getenv('CHASSISPOWERNAME', device_name + '-powerbutton')
mqtt_button_topic = os.getenv('CHASSISPOWERTOPIC', '' + button_name + '/commands')
mqtt_button_availability_topic = os.getenv('CHASSISPOWERAVTTOPIC', '' + button_name + '/availability')

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
    "command_topic": mqtt_button_topic,
    "availability": {
        "topic": mqtt_button_availability_topic
    },
    "device_class": "restart",
    "payload_press": "poweron"
}