UNITS = "G21" # mm

# SET_TO_ZERO = "G92 X0 Y0"
HOME = "$H"
POS_TO_CENTER = "G0 X0 Y0"
POS_TO_ZERO = "G0 X-140 Y0"
CLEAR_ALARM = "$X"

ABSOLUTE = "G90"
INCREMENTAL = "G91"

RAPID_TRAVEL = "G00"
INTERPOLATED_TRAVEL = "G01"

HEADER_HOME = "\n".join([UNITS, ABSOLUTE, HOME, POS_TO_ZERO]) + "\n"

HEADER_HOME_CENTER = "\n".join([UNITS, ABSOLUTE, HOME, POS_TO_CENTER]) + "\n"
# HEADER_HOME_CENTER = "\n".join([UNITS, ABSOLUTE, HOME]) + "\n"

HEADER_SKIP_HOME = "\n".join([UNITS, ABSOLUTE, CLEAR_ALARM]) + "\n"

def convert_trajectory_to_g_code(traj, speed = 5000):
	# Max speed 15000 ish
	gcode = ""
	speed = speed # mm/min
	gcode += "{} X{:.5f} Y{:.5f}\n".format(RAPID_TRAVEL, traj[0][0], traj[0][1])
	for coord in traj:
		gcode += "{} F{:.5f} X{:.5f} Y{:.5f}\n".format(INTERPOLATED_TRAVEL, speed, coord[0], coord[1])
	return gcode