import os
from numpy import interp
from components import mqtt_controller
from time import sleep

def get_ipmi_stats():
    while True:
        ipmistats = os.popen("bash /app/dellfanctl.sh simplestats").read()
        # print(str(ipmistats))
        ipmistatlist = ipmistats.split("\n")
        ipmifanspeed = round(int(ipmistatlist[1]) / 11000 * 100)
        ipmitemp = int(ipmistatlist[0])
        print("Fan speed: " + str(ipmifanspeed) +
              "% | Ambient Temperature: " + str(ipmitemp))
        print("Publishing Fanspeed")              
        mqtt_controller.publish(mqtt_controller.mqtt_fanspeed_topic, ipmifanspeed)
        print("Publishing Ambient temperature")                           
        mqtt_controller.publish(mqtt_controller.mqtt_ambient_temp_topic, ipmitemp)
        sleep(60)

def set_fanmod(mode):
    if mode == 'auto':
        print('setting to auto')
        os.system("bash /app/dellfanctl.sh auto")
    else:
        print("Received invalid command, What Do?")

def set_fanspeed(payload):
    payload = int(payload)
    # SAFEGUARD For accidental noise discharges
    safepayload = interp(int(payload), [0, 100], [0, 60]).round()
    print("setting to " + str(safepayload) +
            "original payload was:" + str(payload))
    os.system("bash /app/dellfanctl.sh manual")
    os.system("bash /app/dellfanctl.sh set " + str(int(safepayload)))