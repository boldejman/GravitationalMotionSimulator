class Mode:
    def __init__(self):
        self.__observers = []

    def addObserver(self, observer):
        self.__observers.append(observer)

    def notifySimulationRequested(self):
        for observer in self.__observers:
            observer.simulationModeRequested()

    def notifyQuiRequested(self):
        for observer in self.__observers:
            observer.quitRequested()

    def notifyPlanetSet(self, planetPos, planetMass):
        for observer in self.__observers:
            observer.setPlanet(planetPos, planetMass)

    def notifyShipSet(self, shipPos, shipMass, shipVel):
        for observer in self.__observers:
            observer.setShip(shipPos, shipMass, shipVel)
