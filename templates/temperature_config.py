import os

device_name = os.getenv('DEVICENAME', 'Poweredge-R510')
temp_sensor_name = os.getenv('TEMPNAME', device_name + '-tempsensor')
mqtt_ambient_temp_topic = os.getenv('TEMPSTATETOPIC', '' + device_name + '/ambienttemp')

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