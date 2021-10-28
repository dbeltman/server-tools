import os

device_name = os.getenv('DEVICENAME', 'Poweredge-R510')
power_sensor_name = os.getenv('POWERNAME', device_name + '-powersensor')
mqtt_power_topic = os.getenv('POWERSTATETOPIC', '' + power_sensor_name + '/powerusage')

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