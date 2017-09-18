import simple_chart as sc
import chart_builder as cb
import numpy as np
import random as rd
import math

def random_ponint(R):
	x = rd.uniform(0, R)
	y = rd.uniform(0, (R ** 2 - x ** 2) ** 0.5)
	return (x, y)

def eq_points(R, n, m):
	dS = np.pi * R ** 2 / n
	dR = R / m
	points = []
	for r in np.arange(dR, R, dR):
		S1 = np.pi * (r ** 2 - (r - dR) ** 2)
		da = 2 * np.pi * dS / S1
		for a in np.arange(0, 2 * np.pi, da):
			points.append(((r - dR / 2) * np.cos(a), (r - dR / 2) * np.sin(a), dS))
	return points

R = 0.03 # радиус отверстия (см)
L = 0.0000005 # длина волны (см)
m = 0.01 # количество зон Френеля
z = R ** 2 / m / L # расстояние от точки наблюдения до отверстия
n = 10000 # количество слогаемых
q = 700
T = 200 * R
S = np.pi * R ** 2 # площадь дырки
tpoints = np.arange(0, T, T / q)
E = [[t, complex(0, 0)] for t in tpoints]
points = eq_points(R, n, 100) # взовращает x, y, dS
A = 1
k = 2 * np.pi / L
J = complex(0, 1)
print(z, R, S)
c = 0
for i in range(len(tpoints)):
	print('точка', i + 1)
	for p in points:
		x, y, dS = p
		t = E[i][0]
		ro = ((t - x) ** 2 + y ** 2 + z ** 2) ** 0.5
		phi = k * ro
		E[i][1] += A / L / J / ro * np.exp(J * phi) * dS
		if t == 0 and phi - k * z >= np.pi * c:
			c += 1
print(abs(E[0][1]) ** 2, c)
curve = sc.Simple_curve(
					name = """$Зависимость\ интенсивности\ I\ от\ смещения\ t.$
$Количество\ зон\ Френеля:\ """ + str(m) + """.$
$Радиус\ отверстия:\ """ + str(R) + """\ см.$
$Расстояние\ до\ точки\ наблюдения:\ """ + "{0:.2f}".format(z) + """\ см.$""",
					line = False,
					curve = True,
					errors = False,
					marker = False,
					x = np.array([E[i][0] for i in range(len(E))]),
					y = np.array([abs(E[i][1]) ** 2 for i in range(len(E))])
				)
chart = sc.Simple_chart(
					name = '$Дифракция\ Френеля$',
					ax = '$t$',
					ay = '$I(t)$',
					curves = [curve]
				)
bulider = cb.Chart_builder(chart, 'Frenel_' + str(m) + 'z')
bulider.build()
