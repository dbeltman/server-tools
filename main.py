from flask import Flask, request
import components.fanctl

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
		output = components.fanctl.get_fan_status()

	else:
		output = 'Commmand not recognised'
	return output


if __name__ == '__main__':
	app.run()
