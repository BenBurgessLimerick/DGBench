
import rospy
import numpy
import os

from std_srvs.srv import Empty, EmptyResponse
from dynamic_workspace_controller.srv import WorkspaceTrajectory, WorkspaceTrajectoryResponse


import sys
sys.path.append("../src/")

import g_code
from controller_interface import ControllerInterface
from dummy_controller import DummyController

import trajectory_helpers


class DynamicWorkspaceNode(object):
	def __init__(self, serial_port="/dev/ttyACM0"):
		# set up controller and home

		if os.path.exists(serial_port):
			self.comms = ControllerInterface(serial_port)
		else:
			print("Serial port {} does not exist! Using dummy controller".format(serial_port))
			self.comms = DummyController()

		self.comms.send_g_code_block(g_code.HEADER_HOME_CENTER)

		self.run_traj_service = rospy.Service("run_workspace_trajectory", WorkspaceTrajectory, self.run_workspace_trajectory)
		self.reset_service = rospy.Service("reset_workspace", Empty, self.reset_workspace)

		self.commands_to_send = []

		self.workspace_size = 140  # Workspace can travel plus or minus this in x and y

	def run_workspace_trajectory(self, req):
		speed = req.speed * 60  # Convert mm/s to mm/min
		trajectory_name = req.trajectory_name
		trajectory_number = req.trajectory_number

		print("Running trajectory {} {} at speed {} mm/s ({} mm/min)".format(trajectory_name, trajectory_number, req.speed, speed))

		traj = trajectory_helpers.load_trajectory(trajectory_name, trajectory_number)

		gcode = g_code.convert_trajectory_to_g_code(traj, speed)

		self.commands_to_send = gcode.split("\n")
		print()

		return WorkspaceTrajectoryResponse()

	def reset_workspace(self, req):
		print("Resetting workspace: {}".format(g_code.POS_TO_CENTER))
		self.commands_to_send = [g_code.POS_TO_CENTER]
		return EmptyResponse()
	
	def run_command_loop(self):
		while not rospy.is_shutdown():
			n_commands = len(self.commands_to_send)
			if n_commands > 0:
				
				self.comms.send_g_code_cmd(self.commands_to_send[0])

				if n_commands != len(self.commands_to_send) and \
						len(self.commands_to_send) == 1 and \
						(self.commands_to_send[0] in [g_code.POS_TO_ZERO, g_code.POS_TO_CENTER]):
					# It has been reset.
					# Send the reset code and then clear it as normal
					self.comms.send_g_code_cmd(self.commands_to_send[0])
				self.commands_to_send = self.commands_to_send[1:]
			else:
				rospy.sleep(0.1)


if __name__ == "__main__":
	rospy.init_node("dynamic_workspace")
	d = DynamicWorkspaceNode()
	d.run_command_loop()