import serial
import time


class ControllerInterface(object):
	def __init__(self, port="COM5"):
		self.serial = serial.Serial(port, 115200, timeout=1)
		time.sleep(1)
		while 1:
			recv = self.serial.readline()
			if recv:
				print("Received {}".format(recv))
			else:
				break
		print("Finished controller initialisation")

	def send_g_code_cmd(self, cmd):
		self.serial.write(bytes(cmd +"\n", "utf-8"))
		received = self.serial.readline()
	
	def send_g_code_block(self, gcode):
		for cmd in gcode.split("\n"):
			self.send_g_code_cmd(cmd)


