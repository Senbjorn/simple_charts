import matplotlib.pyplot as plt
import numpy as np
from simple_chart import *
import re
import os

DEFAULT=0

class Chart_builder():
	def __init__(self, chart, file_name = 'my_chart'):
		self.mode = 0
		self.chart = chart
		self.file_name = file_name
	
	def build(self):
		name = self.chart.get_name()
		ax, ay = self.chart.get_axes_names()
		curves = self.chart.get_curves()
		fig = plt.figure(figsize = (20, 12))
		plt.title(name)
		plt.xlabel(ax, fontsize=38, color='black')
		plt.ylabel(ay, fontsize=38, color='black')
		plt.grid(True)
		for c in curves:
			self.draw_curve(c)
		xmin, xmax = plt.xlim()
		a = (xmax - xmin) * 0.1
		ymin, ymax = plt.ylim()
		b = (ymax-ymin) * 0.1
		plt.xlim(xmin - a, xmax + a)
		plt.ylim(ymin - b, ymax + b)
		plt.legend(frameon = False, loc = 0, fontsize = 28)
		self.save_chart(name = self.file_name, fmt = 'png')
	
	def save_chart(self, name='', fmt='png'):
		pwd = os.getcwd()
		iPath = '.\pictures\{}'.format(fmt)
		if not os.path.exists(iPath):
			if not os.path.exists('.\pictures'):
				os.mkdir('.\pictures')
			os.mkdir(iPath)
		os.chdir(iPath)
		plt.savefig('{}.{}'.format(name, fmt), fmt=fmt)
		os.chdir(pwd)
		# plt.close()

	def draw_curve(self, curve):
		x, y = curve.get_data()
		xerr, yerr = curve.get_errors()
		line, cline, bline = plt.errorbar(x, y, xerr = xerr, yerr = yerr, label = curve.get_name(), antialiased = True)
		line.set_linestyle('')
		line.set_marker('')
		if curve.is_marked():
			line.set_marker('o')
		if curve.is_curve():
			line.set_linestyle('-')
		if curve.is_linear():
			xmin, xmax = min(x), max(x)
			a = (xmax - xmin)
			k = 0.1
			p = np.polyfit(x, y, deg = 1)
			t = np.arange(xmin - a * k, xmax + a * k, a / 100)
			s = ("{0:0f}x"+ ('+' if p[1] >= 0 else '') +"{1:0f}").format(*p)
			plt.plot(t, p[1] + p[0] * t, label = curve.get_name() + " $\ (линейная\ аппроксимация\ " + s + ")$", antialiased = True)
		if xerr is None:
				cline = None
				bline = None



if __name__ == '__main__':
	s = Simple_chart('dot.txt')
	c = Chart_builder(s, 'dot')
	c.build()
