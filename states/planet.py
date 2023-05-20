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