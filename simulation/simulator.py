import numpy as np
import matplotlib.pyplot as plt

from states import Ship, Planet
from states import StateObserver


class Simulation(StateObserver):
    def __init__(self):
        self.ship = Ship()
        # self.ship.shipPar["coord"] = [1, 0.4]
        # self.ship.shipPar["vel"] = [1, -0.5]
        # self.ship.shipPar["mass"] = 1
        #
        # self.planet1 = Planet()
        # self.planet1.planPar["coord"] = [0, 0]
        # self.planet1.planPar["mass"] = 1
        #
        # self.planet2 = Planet()
        # self.planet2.planPar["coord"] = [1, 0]
        # self.planet2.planPar["mass"] = 1

        self.tmax = 20

        self.planets = []
        self.gravConst = 1
        self.accuracy = 0.0001
        self.cnt = 0

    def shipSet(self, shipPos, shipMass, shipVel):
        self.ship.shipPar['coord'] = shipPos
        self.ship.shipPar['mass'] = shipMass
        self.ship.shipPar['vel'] = shipVel
        print(self.ship)

    def planetSet(self, planetPos, planetMass):
        self.planets.append(Planet(planetPos, planetMass))
        print(self.planets)

    def rightSide(self, x, y, v, u):
        f = [0, 0]
        coord = [x, y]
        vel = [v, u]
        r = [0, 0]
        n = [0, 0]

        for planet in self.planets:
            r[0] = planet.planPar["coord"][0] - coord[0]
            r[1] = planet.planPar["coord"][1] - coord[1]

            rLength = (r[0]**2 + r[1]**2)**0.5

            n[0] = r[0]/rLength
            n[1] = r[1]/rLength

            f[0] += self.gravConst * self.ship.shipPar["mass"] * planet.planPar["mass"] * n[0] / (rLength**2)
            f[1] += self.gravConst * self.ship.shipPar["mass"] * planet.planPar["mass"] * n[1] / (rLength ** 2)

        derv = f[0] / self.ship.shipPar["mass"]
        deru = f[1] / self.ship.shipPar["mass"]
        derx = vel[0]
        dery = vel[1]

        return [derx, dery, derv, deru]

    def rungeKutta(self):
        h = self.accuracy
        n = int(self.tmax/h)

        x_k, y_k = self.ship.shipPar["coord"]
        v_k, u_k = self.ship.shipPar["vel"]
        shipCoords = []

        for i in range(n+1):

            k1 = [h * elem for elem in self.rightSide(x_k, y_k, v_k, u_k)]
            k2 = [h * elem for elem in
                  self.rightSide(x_k + h * k1[0] / 2, y_k + h * k1[1] / 2, v_k + h * k1[2] / 2, u_k + h * k1[3] / 2)]
            k3 = [h * elem for elem in
                  self.rightSide(x_k + h * k2[0] / 2, y_k + h * k2[1] / 2, v_k + h * k2[2] / 2, u_k + h * k2[3] / 2)]
            k4 = [h * elem for elem in self.rightSide(x_k + h * k3[0], y_k + h * k3[1], v_k + h * k3[2], u_k + h * k3[3])]

            x_k += (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
            y_k += (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
            v_k += (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6
            u_k += (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]) / 6
            shipCoords.append((x_k, y_k))

            self.cnt += 1
            if self.cnt % 100 == 0:
                print(x_k, y_k)

        return shipCoords

    def getPositions(self):
        return self.rungeKutta()



# sim = Simulation()
# c = sim.rungeKutta()
# c = np.array(c)
#
# plt.plot(c[:, 0], c[:, 1])
# plt.show()

# a = np.array((3, 4))
# print(a/(a.dot(a))**0.5)
