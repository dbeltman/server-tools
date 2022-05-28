import os
from numpy import interp
from components import mqtt_controller
from time import sleep

ipmi_host = os.getenv('IPMIHOST')
ipmi_username = os.getenv('IPMIUSERNAME')
ipmi_password = os.getenv('IPMIPASSWORD')

if ipmi_host and ipmi_username and ipmi_password:
    print("Remote IPMI interface detected")
    ipmi_base_command = "ipmitool -H " + ipmi_host + " -U " + ipmi_username + " -P " + ipmi_password
    ipmi_oem_base_command = "ipmi-oem -h " + ipmi_host + " -u " + ipmi_username + " -p " + ipmi_password 
else:
    ipmi_base_command = "ipmitool"
    ipmi_oem_base_command = "ipmi-oem"

def get_stat_value(stat):
    value=stat.split("|")[1].strip()
    return value

def power_on():
    action = os.popen(ipmi_base_command + " chassis power on").read()
    return action

def scrape_ipmi():
    while True:
        statlist = os.popen(ipmi_base_command + " sensor").read()
        for stat in statlist.split("\n"):
            if "Ambient" in stat:
                if "degrees C" in stat:
                    ambient_temp=get_stat_value(stat)
                    mqtt_controller.publish(mqtt_controller.mqtt_ambient_temp_topic, ambient_temp)
                    print ("Ambient temp: " + str(ambient_temp) + " degrees C")
            elif "FAN MOD 1A" in stat:
                #Todo: make this more generic
                if get_stat_value(stat) != "na":
                    fanpercent=round((float(get_stat_value(stat)) / 11000 * 100))
                else: 
                    fanpercent=0
                mqtt_controller.publish(mqtt_controller.mqtt_fanspeed_topic, fanpercent)
                print (str(fanpercent) + "%")
            elif "System Level" in stat:
                if get_stat_value(stat) != "na":
                    wattage=get_stat_value(stat)
                else: 
                    wattage=0
                mqtt_controller.publish(mqtt_controller.mqtt_power_topic, wattage)
                print (wattage)
        powerconsumption = os.popen(ipmi_oem_base_command + " dell get-power-consumption-data | grep kWh | awk '{ print $4}'").read()
        mqtt_controller.publish(mqtt_controller.mqtt_energy_topic, float(powerconsumption))

        print (str(powerconsumption)+ " kWh") 
        sleep(30)

def set_fanmode(mode):
    if mode == 'auto':
        print('setting to auto')
        os.system(ipmi_base_command + " raw 0x30 0x30 0x01 0x01")
    else:
        print("Received invalid command, What Do?")

def set_fanspeed(payload):
    payload = int(payload)
    # SAFEGUARD For accidental noise discharges
    safepayload = int(interp(int(payload), [0, 100], [0, 60]).round())
    if len(hex(safepayload)) < 4:
        hexpayload = hex(safepayload)[:2] + "0" + hex(safepayload)[2:]
    else:
        hexpayload = hex(safepayload)
    print("setting to " + str(safepayload) +
            "original payload was:" + str(payload))
    os.system(ipmi_base_command + " raw 0x30 0x30 0x01 0x00")
    os.system(ipmi_base_command + " raw 0x30 0x30 0x02 0xff " + hexpayload)