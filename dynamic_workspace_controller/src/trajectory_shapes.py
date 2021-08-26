import numpy

"""
Calculate points for a radiused corner of given angle and radius starting from prev_point
where previous line segment is of direction prev_angle.
"""
def calculate_radiused_corner_points(angle, prev_angle, prev_point, radius, n_points=50):
	if angle > 0:
		# turning left
		center_angle = prev_angle + 90
	else:
		# turning right
		center_angle = prev_angle - 90
	
	# Calculate center point
	center_angle_rad = numpy.deg2rad(center_angle)
	center = prev_point + numpy.array([numpy.cos(center_angle_rad), numpy.sin(center_angle_rad)], dtype=numpy.float32) * radius

	# Calculate angles around center point
	inv_center_angle = center_angle + 180
	theta = numpy.deg2rad(numpy.linspace(inv_center_angle, inv_center_angle + angle, n_points))

	# Generate corner points
	new_corner_points = numpy.vstack([numpy.cos(theta), numpy.sin(theta)]).astype(numpy.float32).T * radius + center
	return new_corner_points
	
class RadiusedRandomWalk(object):
	def __init__(self, workspace_size=140, n_direction_changes=10, dist_between_changes=50, radius=10, seed=None):
		self.workspace_size = workspace_size
		self.n_direction_changes = int(n_direction_changes)
		self.dist_between_changes = dist_between_changes
		self.radius = radius

		if seed is not None:
			self.seed = int(seed)
		else:
			self.seed = seed
	
	def generate(self):
		points = numpy.zeros(2, dtype=numpy.float32).reshape(1, 2)
		dist = self.dist_between_changes
		prev_angle = None

		if self.seed is not None:
			numpy.random.seed(self.seed)

		for i in range(1, self.n_direction_changes):
			while 1:
				# Random angle between 45 and 315
				angle = (numpy.random.rand() * 270) + 45

				# Keep absolute value of angle < 180
				if angle > 180:
					angle -= 360

				new_corner_points = None
				corner_points_out_of_bounds = False
				if prev_angle is not None:
					# Construct radiused corner is this is a direction change
					new_corner_points = calculate_radiused_corner_points(angle, prev_angle, points[-1, :], self.radius)

					# Check the corner will be within workspace bounds
					corner_points_out_of_bounds = numpy.any(numpy.abs(new_corner_points) > self.workspace_size)

					angle += prev_angle

				# Calculate next point
				angle_rad = numpy.deg2rad(angle)
				new_point_offset = numpy.array([numpy.cos(angle_rad), numpy.sin(angle_rad)], dtype=numpy.float32) * dist
				
				if new_corner_points is None:
					new_point = points[-1, :] + new_point_offset
				else:
					new_point = new_corner_points[-1, :] + new_point_offset

				
				# Simulate 360 degree turns left and right to ensure that a new direction will be possible while staying in bounds
				next_corner_points_left = calculate_radiused_corner_points(360, angle, new_point, self.radius)
				next_corner_points_in_bounds_left = numpy.all(numpy.abs(next_corner_points_left) <= self.workspace_size)

				next_corner_points_right = calculate_radiused_corner_points(-360, angle, new_point, self.radius)
				next_corner_points_in_bounds_right = numpy.all(numpy.abs(next_corner_points_right) <= self.workspace_size)

				# If either direciton possible, it will be ok
				next_corner_points_in_bounds = next_corner_points_in_bounds_left or next_corner_points_in_bounds_right
				

				if numpy.all(numpy.abs(new_point) <= self.workspace_size) and not corner_points_out_of_bounds and next_corner_points_in_bounds:
					prev_angle = angle
					if new_corner_points is not None:
						points = numpy.vstack([points, new_corner_points])
						
					points = numpy.vstack([points, new_point])
					break 

		return numpy.vstack(points)



if __name__=="__main__":
	from matplotlib import pyplot as plt
	from trajectory_helpers import *
	
	START_SEED = 1

	plt.style.use(['science', "grid"])
	plt.figure(figsize=(4,4))
	ax = plt.axes()
	ax.set_aspect(1)

	styles = ["k-", "b:", "r--"]
	for i in range(3):
		shape = RadiusedRandomWalk(140, 16, 50, 10, i + START_SEED)
		traj = shape.generate()
		traj = interpolate_trajectory(traj)

		plt.xlim([-150, 150])
		plt.ylim([-150, 150])
		plt.plot(traj[:, 0], traj[:, 1], styles[i])

	plt.xlabel("$x$ (mm)")
	plt.ylabel("$y$ (mm)")
	plt.title("Workspace Trajectory")
	plt.tight_layout()

	# plt.savefig("../RadiusedRandomWalkTrajectories.svg", format="svg")
	plt.show()