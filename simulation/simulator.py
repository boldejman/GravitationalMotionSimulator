import numpy as np
import matplotlib.pyplot as plt


class Ship:
    def __init__(self):
        self.shipPar = {
            "coord": np.array((0, 0)),
            "vel": np.array((0, 0)),
            "mass": 0
        }

    @property
    def shipCoord(self):
        return self.shipPar["coord"]

    @shipCoord.setter
    def shipCoord(self, coord):
        self.shipPar["coord"] = coord

    @property
    def shipVel(self):
        return self.shipPar["vel"]

    @shipVel.setter
    def shipVel(self, vel):
        self.shipPar["vel"] = vel

    @property
    def shipMass(self):
        return self.shipPar["mass"]

    @shipMass.setter
    def shipMass(self, mass):
        self.shipPar["mass"] = mass


class Planet:
    def __init__(self):
        self.planPar = {
            "mass": 0,
            "coord": np.array((0, 0))
        }

    @property
    def planetMass(self):
        return self.planPar["mass"]

    @planetMass.setter
    def planetMass(self, mass):
        self.planPar["mass"] = mass

    @property
    def planetCoord(self):
        return self.planPar["coord"]

    @planetCoord.setter
    def planetCoord(self, coord):
        self.planPar["coord"] = coord


class Simulation:
    def __init__(self):
        self.ship = Ship()
        self.ship.shipCoord = np.array((1, 0.4))
        self.ship.shipVel = np.array((1, -0.5))
        self.ship.shipMass = 1

        self.planet1 = Planet()
        self.planet1.planetCoord = np.array((0, 0))
        self.planet1.planetMass = 1

        self.planet2 = Planet()
        self.planet2.planetCoord = np.array((1, 0))
        self.planet2.planetMass = 1

        self.tmax = 20

        self.planets = [self.planet1, self.planet2]
        self.gravConst = 1
        self.accuracy = 0.001

    def rightSide(self, x, y, v, u):
        f = 0
        coord = np.array((x, y))
        vel = np.array((v, u))
        for planet in self.planets:
            r = planet.planetCoord - coord
            n = r/(r.dot(r))**0.5
            f += self.gravConst * self.ship.shipMass * planet.planetMass * n / r.dot(r)

        derv, deru = f / self.ship.shipMass
        derx, dery = vel
        return [derx, dery, derv, deru]

    def rungeKutta(self):
        h = self.accuracy
        n = int(self.tmax/h)

        x_k, y_k = self.ship.shipCoord
        v_k, u_k = self.ship.shipVel
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

        return shipCoords


# sim = Simulation()
# x = sim.rungeKutta()
# x = np.array(x)
#
# plt.plot(x[:,0], x[:,1])
# plt.show()

# a = np.array((3, 4))
# print(a/(a.dot(a))**0.5)
