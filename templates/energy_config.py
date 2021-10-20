import os

device_name = os.getenv('DEVICENAME', 'Poweredge-R510')
energy_sensor_name = os.getenv('ENERGYNAME', device_name + '-energysensor')
mqtt_energy_topic = os.getenv('ENERGYSTATETOPIC', '' + energy_sensor_name + '/energyusage')

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