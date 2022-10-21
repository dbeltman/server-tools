# R510-Denoiser
### Homeassistant-compatible fan controller using mqtt for Dell R510,R710 and possibly other IDRAC6 devices
##### Bonus: Fan controller and other sensors automatically discovered by HomeAssistant if you have MQTT-discovery enabled in the mqtt integration.
# 
## SECURITY WARNING
For this project to work, you need to expose your /dev/ipmi0 device to this docker container which has not been tested at length. 

IPMI has a lot more functionality than just fan control (power off entire chassis and other fun stuff)

Please consider the security risks of this, and deploy accordingly.

Recently added remote IPMI support, but same principle stands

## Additional metrics
#### The following metrics are also available
- "Ambient" Inlet air temperature (degrees C)
- Power draw (W)
- Energy consumption (kWh)
- Fan speed (%), of course



## Setup :whale:

#### Kubernetes:
- Create a new secret containing your connection details (Not all options are required, see "Variables" below!)`kubectl create secret generic denoiser-secret --from-literal=MQTTHOST=changeme --from-literal=MQTTUSERNAME=changeme --from-literal=MQTTPASSWORD=changeme --from-literal=IPMIHOST=changeme --from-literal=IPMIUSERNAME=changeme --from-literal=IPMIPASSWORD=changeme --from-literal=DEVICENAME=Your-Friendly-Name`
- `kubectl apply -f -n yournamespace k8s/deployment.yaml`. Or use argoCD/flux and sealed-secrets, i'm not your mom
- Profit


#### Docker Run
- `docker run --rm --name R510-Denoiser --device /dev/ipmi0:/dev/ipmi0 -e MQTTHOST=localhost -e DEVICENAME=MyServer dockerdaan/r510-denoiser:latest`

#### Portainer
- Add new container with image `dockerdaan/r510-denoiser:latest`
- Add required Environment variables to the "Env" tab
- Add the following device mapping under the "Runtime & Resources" tab:  `/dev/ipmi0:/dev/ipmi0`

#### TODO Compose: (Swarm mode not supported because --device mapping)
- `docker-compose up -d` 

### Variables
#### Required
##### MQTT-Settings
- `MQTTHOST`: ip-addres or hostname of the MQTT server
#### Optional
##### IPMI (REQUIRED in kubernetes! todo: device passthrough k8s)
- `IPMIHOST`: Hostname/IP address of your IPMI interface (iDrac IP)
- `IPMIUSERNAME`: Username of your IPMI interface (iDrac username)
- `IPMIPASSWORD`: Password of your IPMI user (iDrac password)
##### MQTT-Settings
- `DEVICENAME` : Friendly name of the device, no spaces. Will default to "Poweredge-R510"
- `MQTTPORT`: port of the MQTT Server, defaults to 1883
- `MQTTCLIENTNAME`: Client name used to connect to the MQTT server, defaults to "r510-denoiser"
- `DISCOTOPIC`: discovery topic for homeassistant, only change this if you have a custom topic set in homeassistant
- `FANNAME`: Name of the fan, defaults to "`$DEVICENAME`-fan"
- `TEMPNAME`: Temperature sensor name, defaults to "`$DEVICENAME`-tempsensor"
- `POWERNAME`: Power usage sensor name, defaults to "`$DEVICENAME`-powersensor"
- `ENERGYNAME`: Energy consumption sensor name, defaults to "`$DEVICENAME`-energysensor"
- `FANCONTROLTOPIC`: Topic for controlling the fans, defaults to "`$DEVICENAME`/fansetpoint"
- `FANSTATETOPIC`: Topic for controlling the fans, defaults to "`$DEVICENAME`/fansetpoint"
- `TEMPSTATETOPIC`: Temperature state topic, defaults to "`$DEVICENAME`/ambienttemp"
- `POWERSTATETOPIC`: Power usage state topic, defaults to "`$DEVICENAME`/powerusage"
- `ENERGYSTATETOPIC`: Energy consumption state topic, defaults to "`$DEVICENAME`/energyusage"

### Usage
- If installation was done correctly, a new device should appear in the HomeAssistant mqtt-integration 
- This device contains the fan control entity along with the other sensors
- Manual Fan Control can be done via the mqtt-topic: "$FANNAME/fansetpoint". 
    - Accepted values: Whole numbers between 1-100 and "auto" for the default DELL fan-curve
