class Planet:
    def __init__(self, coord, mass):
        self.planPar = {
            "coord": coord,
            "mass": mass,
        }


class Ship:
    def __init__(self):
        self.shipPar = {
            "coord": (0, 0),
            "vel": (0, 0),
            "mass": 0
        }
