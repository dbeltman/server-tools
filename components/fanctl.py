import components.ssh_connector as sshconnect


def set_fan_auto():
	# # process = Popen(['sudo', '/bin/bash', '/home/dbtman/fanctl.sh', 'auto'], stdout=PIPE, stderr=PIPE)
	# process = Popen(['ssh', 'poweredge-r510', '~/R510-Denoiser/scripts/dellfanctl.sh', 'auto'], stdout=PIPE, stderr=PIPE)
	# stdout, stderr = process.communicate()
	# print(str(stdout))
	stdout = sshconnect.set_auto()
	return stdout


def set_fan_manual(value):
	# set_manual = Popen(['ssh', 'poweredge-r510', '~/R510-Denoiser/scripts/dellfanctl.sh', 'manual'], stdout=PIPE, stderr=PIPE)
	# manual_stdout, manual_stderr = set_manual.communicate()
	# set_value = Popen(['ssh', 'poweredge-r510', '~/R510-Denoiser/scripts/dellfanctl.sh', 'set', str(value)], stdout=PIPE, stderr=PIPE)
	# value_stdout, value_stderr = set_value.communicate()
	# stdout = manual_stdout + value_stdout
	# stderr = manual_stderr + value_stderr
	stdout = sshconnect.set_manual(value)
	return stdout


def get_detailed_status():
	# process = Popen(['ssh', 'poweredge-r510', '~/R510-Denoiser/scripts/dellfanctl.sh', 'status'], stdout=PIPE, stderr=PIPE)
	# stdout, stderr = process.communicate()
	stdout = str(sshconnect.get_status())
	print(stdout)
	return stdout
