import numpy as np
import re

class Simple_curve():
	def __init__(self, name, line, curve, errors, x, y, xe = None, ye = None):
		self.name = name
		self.line = line
		self.curve = curve
		self.errors = errors
		self.x = x
		self.y = y
		self.xe = xe
		self.ye = ye

	def get_name(self):
		return self.name

	def get_data(self):
		return (self.x, self.y)

	def get_errors(self):
		return (self.xe, self.ye)

	def is_linear(self):
		return self.line

	def is_curve(self):
		return self.curve

class Simple_chart():
	def __init__(self, file):
		self.name, self.ax, self.ay, self.curves = self.read(file)

	def read(self, file):
		file = open(file, 'r')
		data_str = file.read()
		file.close()
		regexp = re.compile("""^#chart:\nname=(.+)\nax=(.+)\nay=(.+)\ncurves=(\d+)\n#data:\n""")
		sre_1 = regexp.search(data_str)
		assert sre_1
		group_1 = sre_1.groups()
		name, ax, ay, curves = group_1
		curves = int(curves)
		index = sre_1.end()
		c_array = []
		for i in range(curves):
			tf = lambda s: True if s == 'True' else False
			regexp = re.compile("""^dname=(.+)\nline=(True|False)\ncurve=(True|False)\nerrors=(True|False)\nnpoints=(\d+)\n""")
			sre = regexp.search(data_str[index:])
			assert sre
			index += sre.end()
			dname, line, curve, errors, npoints = sre.groups()
			line = tf(line)
			curve = tf(curve)
			errors = tf(errors)
			npoints = int(npoints)
			regdata = re.compile("^#\(x\,\sy\)\n" + "(-?\d+(?:[\.\,]\d+)?)(?:[\s\t]|\,[\s\t]?|;[\s\t]?)(-?\d+(?:[\.\,]\d+)?)\n" * npoints)
			sredata = regdata.search(data_str[index:])
			assert sredata
			index += sredata.end()
			xy = sredata.groups()
			x = np.array([float(xy[i]) for i in range(0, len(xy), 2)])
			y = np.array([float(xy[i]) for i in range(1, len(xy), 2)])
			if errors:
				regerr = re.compile("^#\(delta_x\,\sdelta_y\)\n" + "(-?\d+(?:[\.\,]\d+)?)(?:[\s\t]|\,[\s\t]?|;[\s\t]?)(-?\d+(?:[\.\,]\d+)?)\n" * npoints)
				sreerr = regerr.search(data_str[index:])
				assert sreerr
				index += sreerr.end()
				xye = sreerr.groups()
				xe = np.array([float(xye[i]) for i in range(0, len(xye), 2)])
				ye = np.array([float(xye[i]) for i in range(1, len(xye), 2)])
				c_array.append(Simple_curve(dname, line, curve, errors, x, y, xe, ye))
			else:
				c_array.append(Simple_curve(dname, line, curve, errors, x, y))
		return (name, ax, ay, c_array)

	def get_name(self):
		return self.name

	def get_curves(self):
		return self.curves

	def get_axes_names(self):
		return (self.ax, self.ay)