class Simulation:
    def __init__(self):
        self.ship = None
        self.tmax = 15
        # self.cnt = 0
        self.planets = []
        self.gravConst = 1
        self.accuracy = 0.0001

    def shipSet(self, ship):
        self.ship = ship

    def planetSet(self, planets):
        self.planets = planets

    def accuracySet(self, accuracy):
        self.accuracy = accuracy

    def tMaxSet(self, tMax):
        self.tmax = tMax

    # Calculate right side for differential equation
    def rightSide(self, x, y, v, u):
        f = [0, 0]
        coord = [x, y]
        vel = [v, u]
        r = [0, 0]
        n = [0, 0]

        for planet in self.planets:
            r[0] = planet.coord[0] - coord[0]
            r[1] = planet.coord[1] - coord[1] 
            rLength = (r[0]**2 + r[1]**2)**0.5

            n[0] = r[0]/rLength
            n[1] = r[1]/rLength

            f[0] += self.gravConst * self.ship.mass * planet.mass * n[0] / (rLength ** 2)
            f[1] += self.gravConst * self.ship.mass * planet.mass * n[1] / (rLength ** 2)

        derv = f[0] / self.ship.mass
        deru = f[1] / self.ship.mass
        derx = vel[0]
        dery = vel[1]

        return [derx, dery, derv, deru]

    # Numerical Method
    def rungeKutta(self):
        h = self.accuracy
        n = int(self.tmax/h)

        x_k, y_k = self.ship.coord
        v_k, u_k = self.ship.vel
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

            if not -500 < x_k < 1340 or not -500 < y_k < 1220:
                return shipCoords
        return shipCoords

    def getPositions(self):
        return self.rungeKutta()
