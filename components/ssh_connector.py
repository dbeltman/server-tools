import paramiko

key = paramiko.RSAKey.from_private_key_file("static/poweredge.key")


def set_auto():
	conn = paramiko.SSHClient()
	conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print("connecting")
	conn.connect(hostname="poweredge", username="dbtman", pkey=key)
	print("connected")
	command = "sudo bash ~/fanctl.sh auto"
	print("Executing {}".format(command))
	stdin, stdout, stderr = conn.exec_command(command)
	output = stdout.read()
	print(stdout.read())
	print("Errors")
	print(stderr.read())
	errors = stderr.read()

	conn.close()
	return output


def set_manual(value):
	conn = paramiko.SSHClient()
	conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print("connecting")
	conn.connect(hostname="poweredge", username="dbtman", pkey=key)
	print("connected")
	commands = "sudo bash ~/R510-Denoiser/scripts/dellfanctl.sh manual && sudo bash ~/R510-Denoiser/scripts/dellfanctl.sh set " + str(value)
	print("Executing {}".format(commands))
	stdin, stdout, stderr = conn.exec_command(commands)
	output = stdout.read()
	print(stdout.read())
	print("Errors")
	print(stderr.read())
	errors = stderr.read()

	conn.close()
	return output


def get_status():
	conn = paramiko.SSHClient()
	conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print("connecting")
	conn.connect(hostname="poweredge", username="dbtman", pkey=key)
	print("connected")
	commands = "sudo bash ~/R510-Denoiser/scripts/dellfanctl.sh status"
	print("Executing {}".format(commands))
	stdin, stdout, stderr = conn.exec_command(commands)
	output = stdout.read()
	print(stdout.read())
	print("Errors")
	print(stderr.read())
	errors = stderr.read()
	cleanoutput = []
	for line in output.splitlines():
		line = line.strip()
		if not line: continue
		cleanoutput.append(line.decode('UTF-8'))
	conn.close()
	return cleanoutput
