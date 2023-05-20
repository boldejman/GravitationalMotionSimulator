class Mode:
    def __init__(self):
        self.__observers = []

    def notifySimulationRequested(self):
        for observer in self.__observers:
            observer.simulationMode()

    def notifyQuiRequested(self):
        for observer in self.__observers:
            observer.quitRequseted()
