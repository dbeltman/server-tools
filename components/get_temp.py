import components.ssh_connector as sshconnect


def get_ambient_temp():
	temperature = float(sshconnect.get_status()[2].replace('Ambient Temp', '').strip())

	return temperature
