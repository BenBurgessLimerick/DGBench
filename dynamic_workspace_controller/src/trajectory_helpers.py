import numpy
import os
import matplotlib.pyplot as plt

def interpolate_trajectory(traj, max_distance = 1):
	new_traj = traj[0, :].reshape(-1, 2)
	for i in range(1, traj.shape[0]):
		dist_to_previous = numpy.linalg.norm(new_traj[-1, :] - traj[i, :])

		if dist_to_previous > max_distance:
			n_required = int(numpy.ceil(dist_to_previous / max_distance))
			vals = numpy.tile(numpy.linspace(0, 1, n_required + 1)[1:].reshape(-1,1), 2)
			new_traj = numpy.vstack([new_traj, (new_traj[-1, :] * (1-vals) + traj[i, :] * vals)])
			
		else:
			# insert current point
			new_traj = numpy.vstack([new_traj, traj[i, :]])

	return new_traj

def load_trajectory(name, number):
	filename = os.path.join(
		"../trajectories",
		name, 
		"trajectory_{}.csv".format(number)
	)
	traj = numpy.loadtxt(filename, dtype=numpy.float32, delimiter=",")
	print("Loaded {} from {}".format(traj.shape, filename))
	return traj

def plot_trajectory(traj):
	plt.style.use(['science', "grid"])
	plt.figure(figsize=(4,4))
	ax = plt.axes()
	ax.set_aspect(1)

	plt.xlim([-150, 150])
	plt.ylim([-150, 150])
	plt.plot(traj[:, 0], traj[:, 1], "k-")

	plt.xlabel("$x$ (mm)")
	plt.ylabel("$y$ (mm)")
	plt.title("Workspace Trajectory")
	plt.tight_layout()
	plt.show()