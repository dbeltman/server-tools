from subprocess import Popen, PIPE


def set_fan_auto():
	# process = Popen(['sudo', '/bin/bash', '/home/dbtman/fanctl.sh', 'auto'], stdout=PIPE, stderr=PIPE)
	process = Popen(['sudo', '/bin/bash', '/home/dbtman/fanctl.sh', 'auto'], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	print(str(stdout))
	return str(stdout) + '\n' + str(stderr)


def set_fan_manual(value):
	set_manual = Popen(['sudo', '/bin/bash', '/home/dbtman/fanctl.sh', 'manual'], stdout=PIPE, stderr=PIPE)
	manual_stdout, manual_stderr = set_manual.communicate()
	set_value = Popen(['sudo', '/bin/bash', '/home/dbtman/fanctl.sh', 'set', str(value)], stdout=PIPE, stderr=PIPE)
	value_stdout, value_stderr = set_value.communicate()
	stdout = manual_stdout + value_stdout
	stderr = manual_stderr + value_stderr
	return stdout


def get_fan_status():
	process = Popen(['sudo', '/bin/bash', '/home/dbtman/fanctl.sh', 'status'], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	return stdout