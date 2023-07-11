from pygame.math import Vector2


class States:
    def __init__(self):
        self.units = []
        self.trace = []
        self.background = [[Vector2(5, 1)]*16]*10
        self.__observers = []

    def addObserver(self, observer):
        self.__observers.append(observer)

    def notifyPlanetSet(self, planetPos, planetMass):
        for observer in self.__observers:
            observer.planetSet(planetPos, planetMass)

    def notifyShipSet(self, shipPos, shipMass, shipVel):
        for observer in self.__observers:
            observer.shipSet(shipPos, shipMass, shipVel)
