
import os
from matplotlib import pyplot as plt
import numpy

import sys
sys.path.append("../src/")

import trajectory_shapes
import trajectory_helpers



def plot_trajectory(traj, name="", save_name="trajectory"):
	plt.style.use(['science', "grid"])
	plt.figure(figsize=(4,4))
	ax = plt.axes()
	ax.set_aspect(1)

	plt.xlim([-150, 150])
	plt.ylim([-150, 150])
	plt.plot(traj[:, 0], traj[:, 1], "k-")

	plt.xlabel("$x$ (mm)")
	plt.ylabel("$y$ (mm)")
	plt.title("Workspace Trajectory {}".format(name))
	plt.tight_layout()
	plt.savefig(save_name)

def save_trajectory(traj, name):
	numpy.savetxt(name, traj, delimiter=",", fmt="%f")


if __name__ == "__main__":
	n_to_generate = 20
	start_seed = 1

	workspace_size = 140 # mm
	n_direction_changes = 30
	dist_between_changes = 50
	corner_radius = 10

	folder_name = "../trajectories/RadiusedRandomWalk"

	if not os.path.exists(folder_name):
		print("Creating folder {}".format(folder_name))
		os.mkdir(folder_name)

	image_folder_name = os.path.join(folder_name, "images")
	if not os.path.exists(image_folder_name):
		print("Creating image folder {}".format(image_folder_name))
		os.mkdir(image_folder_name)


	for i in range(n_to_generate):
		seed = i + start_seed
		traj = trajectory_shapes.RadiusedRandomWalk(
			workspace_size,
			n_direction_changes,
			dist_between_changes, 
			corner_radius,
			seed
		).generate()

		traj = trajectory_helpers.interpolate_trajectory(traj)

		save_name = os.path.join(folder_name, "trajectory_{}.csv".format(seed))
		save_trajectory(traj,save_name)

		image_save_name = os.path.join(image_folder_name, "trajectory_{}".format(seed))
		plot_trajectory(
			traj,
			seed,
			image_save_name
		)

