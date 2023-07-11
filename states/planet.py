from .stateObserver import StateObserver


class Planet(StateObserver):
    def __init__(self, coord, mass):
        self.planPar = {
            "coord": coord,
            "mass": mass,
        }

    def __repr__(self):
        return str(self.planPar)
