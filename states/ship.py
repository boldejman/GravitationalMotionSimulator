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