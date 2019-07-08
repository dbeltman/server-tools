from flask import Flask, request
import components.fanctl
app = Flask(__name__)


@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/<command>')
def process_command(command):
	if command == 'auto':
		components.fanctl.set_fan_auto()
	else:
		'Commmand not recognised'
	return 'ok'


if __name__ == '__main__':
	app.run()
