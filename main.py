from flask import Flask, request

import components.fanctl
import components.ssh_connector as sshconnect

app = Flask(__name__)


@app.route('/')
def hello_world():
	return 'Hello World!'


@app.route('/<command>')
def process_command(command):
	if command == 'auto':
		output = components.fanctl.set_fan_auto()

	elif command == 'manual':
		if 10 <= int(request.args['fanspeed']) <= 100:
			# output = 'Setting fan speed to ' + str(request.args['fanspeed'])
			output = components.fanctl.set_fan_manual(int(request.args['fanspeed']))
		else:
			return 'not an integer, or invalid value!'

	elif command == 'status':
		output = sshconnect.get_auto_status()
		if 'No such file or directory' in str(output):
			status = '0'
		else:
			status = '1'
		return status

	else:
		output = 'Command not recognised'
	return output


if __name__ == '__main__':
	app.run()
