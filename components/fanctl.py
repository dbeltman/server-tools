from subprocess import Popen, PIPE

def set_fan_auto():
	process = Popen(['sudo bash', '/home/dbtman/fanctl.sh', 'auto'], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	print(stdout)
	return stdout