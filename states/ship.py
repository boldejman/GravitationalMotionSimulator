from .stateObserver import StateObserver


class Ship(StateObserver):
    def __init__(self):
        self.shipPar = {
            "coord": (0, 0),
            "vel": (0, 0),
            "mass": 0
        }

    def __repr__(self):
        return str(self.shipPar)
