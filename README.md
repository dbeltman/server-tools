# R510-Denoiser
### MQTT-Enabled fan controller for Dell R510/Other IDRAC6 devices
### Bonus: Automatically discovered by HomeAssistant if you have MQTT-discovery enabled on the mqtt-server.
# 
## SECURITY WARNING
For this project to work, you need to expose your /dev/ipmi0 device to this docker container which has not been tested at length. 

IPMI has a lot more functionality than just fan control (power off entire chassis and other fun stuff)

Please consider the security risks of this, and deploy accordingly.


## Variables:
#### Required:
- `FANNAME` : Friendly name of the fan, dont use spaces because i dont normalise input sue me
- `MQTTHOST`: ip-addres or hostname of the MQTT server
#### Optional:
- `MQTTPORT`: port of the MQTT Server, defaults to 1883
- `MQTTCLIENTNAME`: Client name used to connect to the MQTT server, defaults to "r510-denoiser"
- //TODO: add authentication stuff

### Docker Installation :whale::
#### TODO Compose: (Swarm mode not supported because --device mapping)
- `docker-compose up -d` 

#### Portainer
- Add new container with image `dockerdaan/r510-denoiser:latest`
- Add required Environment variables to the "Env" tab
- Add the following device mapping under the "Runtime & Resources" tab:  `/dev/ipmi0:/dev/ipmi0`

### Usage
- If installation was done correctly, a fan should appear in the HomeAssistant mqtt-integration
- Manual Control can be done via the mqtt-topic: "$FANNAME/fansetpoint". 
    - Accepted values: Whole numbers between 1-100 and "auto" for the default DELL fan-curve
