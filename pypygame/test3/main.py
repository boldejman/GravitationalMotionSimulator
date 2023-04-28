import matplotlib.pyplot as plt
import numpy as np
import pygame


# class State:
#     def __init__(self):
#         self.x = 0
#         self.y = 0
#         self.v = 0
#         self.u = 0
#
#     def update(self, x_k, y_k):
#         self.x = x_k
#         self.y = y_k
#
#
# class UserInterface:
#     def __init__(self):
#         pass
#
#     def processInput(self):

def rightSide(x, y, v, u, m=1, k=1):
    F1 = [-k*x/(x**2+y**2)**1.5, -k*y/(x**2+y**2)**1.5]
    F2 = [-k*(x-1)/((x-1)**2+y**2)**1.5, -k*y/((x-1)**2+y**2)**1.5]
    derv = (F1[0]+F2[0])/m
    deru = (F1[1]+F2[1])/m
    derx = v
    dery = u
    return [derx, dery, derv, deru]


def RungeKutta(x0, y0, v0, u0, t0, t, h=0.0001):
    # number of iterating process
    n = int((t-t0)/h)

    # define y_k as y(x_k), where y(x) is function that we are looking for
    x_k = x0
    y_k = y0
    v_k = v0
    u_k = u0
    x_values = [x0*100]
    y_values = [y0*100]

    for i in range(1, n+1):
        k1 = [h * elem for elem in rightSide(x_k, y_k, v_k, u_k)]
        k2 = [h * elem for elem in rightSide(x_k + h*k1[0]/2, y_k + h*k1[1]/2, v_k + h*k1[2]/2, u_k + h*k1[3]/2)]
        k3 = [h * elem for elem in rightSide(x_k + h*k2[0]/2, y_k + h*k2[1]/2, v_k + h*k2[2]/2, u_k + h*k2[3]/2)]
        k4 = [h * elem for elem in rightSide(x_k + h*k3[0], y_k + h*k3[1], v_k + h*k3[2], u_k + h*k3[3])]

        x_k += (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        y_k += (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        v_k += (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6
        u_k += (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]) / 6
        x_values.append(x_k*100)
        y_values.append(y_k*100)

    return x_values, y_values


x0 = 1
y0 = 0.4
v0 = 1
u0 = -0.5

x, y = RungeKutta(x0, y0, v0, u0, 0, 20)


plt.plot(x, y)
plt.show()


