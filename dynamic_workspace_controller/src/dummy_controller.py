

class DummyController(object):
	def __init__(self, port="COM5"):
		print("Finished controller initialisation")

	def send_g_code_cmd(self, cmd):
		# print("Sending {}".format(cmd))
		pass
	
	def send_g_code_block(self, gcode):
		pass