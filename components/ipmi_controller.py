import os
from numpy import interp
from components import mqtt_controller
from time import sleep
import statistics

def get_stat_value(stat):
    value=stat.split("|")[1].strip()
    return value

def get_ipmi_stats():
    while True:
        ipmistats = os.popen("bash /app/dellfanctl.sh simplestats").read()
        ipmistatlist = ipmistats.split("\n")
        ipmifanspeed = round(int(ipmistatlist[1]) / 11000 * 100)
        ipmitemp = int(ipmistatlist[0])
        print("Fan speed: " + str(ipmifanspeed) +
              "% | Ambient Temperature: " + str(ipmitemp))
        print("Publishing Fanspeed!")              
        mqtt_controller.publish(mqtt_controller.mqtt_fanspeed_topic, ipmifanspeed)
        print("Publishing Ambient temperature")                           
        mqtt_controller.publish(mqtt_controller.mqtt_ambient_temp_topic, ipmitemp)
        sleep(60)

def scrape_ipmi():
    while True:
        statlist = os.popen("bash /app/dellfanctl.sh statlist").read()
        rpmlist=[]
        for stat in statlist.split("\n"):
            if "Ambient" in stat:
                if "degrees C" in stat:
                    ambient_temp=get_stat_value(stat)
                    mqtt_controller.publish(mqtt_controller.mqtt_ambient_temp_topic, ambient_temp)
                    print ("Ambient temp: " + str(ambient_temp) + " degrees C")
            elif "FAN MOD 1A" in stat:
                #Todo: make this more generic
                fanpercent=round((float(get_stat_value(stat)) / 11000 * 100))
                mqtt_controller.publish(mqtt_controller.mqtt_fanspeed_topic, fanpercent)
                print (str(fanpercent) + "%")
            elif "System Level" in stat:
                wattage=get_stat_value(stat)
                mqtt_controller.publish(mqtt_controller.mqtt_power_topic, wattage)
                print (wattage)
        powerconsumption = os.popen("bash /app/dellfanctl.sh powerconsumption").read()
        mqtt_controller.publish(mqtt_controller.mqtt_energy_topic, float(powerconsumption))

        print (str(powerconsumption)+ " kWh") 
        sleep(30)

def set_fanmode(mode):
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