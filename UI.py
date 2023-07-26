import pygame as pg
import constants
from mode import Menu, SimulationManager
from simulation import Simulation


class UserInterface:
    # Class, that realising all logic of the app.
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((constants.SCREEN_X, constants.SCREEN_Y))
        self.clock = pg.time.Clock()
        self.mouse = None
        self.events = None
        self.running = True

        # every 'planet' is tuple ('coordinates', 'mass')
        self.planets = []
        self.planetDispositionCheck = False  # it needs to dispose the planet
        self.planetImage = pg.image.load('figures/planet.png')

        # ship is tuple ('coordinates', 'mass', 'velocity')
        self.ship = None
        self.shipDispositionCheck = False
        self.shipVelocityCheck = False
        self.shipCoord = (0, 0)
        self.shipImage = pg.image.load('figures/rocket3.png')
        self.velCoef = 5

        self.background = pg.image.load("figures/background_space.png")

        self.menu = Menu(self)
        self.simulation = Simulation()
        self.simulationManager = SimulationManager(self.simulation, self)
        self.currentMode = 'setting'

    def run(self):
        while self.running:
            self.update()
            self.menu.update()
            self.simulationManager.update()
            self.processInput()
            self.menu.processInput()
            self.screen.blit(self.background, (0, 0))
            self.simulationManager.render(self.screen)
            self.menu.render(self.screen)
            self.running = self.menu.running

            pg.display.update()
            self.clock.tick(60)

    def update(self):
        self.mouse = pg.mouse.get_pos()
        self.events = pg.event.get()

    def processInput(self):
        for event in self.events:
            if event.type == pg.MOUSEBUTTONUP:
                # dispose and save the planet
                if self.planetDispositionCheck and 0 < self.mouse[0] < constants.PLAYING_SCREEN_X:
                    self.planets.append((self.mouse, float(self.menu.menuTextInput[0].value)))
                    self.planetDispositionCheck = False
                    self.menu.notifyingWindow.text = ['']

                # set the velocity of the ship and saving it
                if self.shipVelocityCheck and 0 < self.mouse[0] < constants.PLAYING_SCREEN_X and \
                        0 < self.mouse[1] < constants.PLAYING_SCREEN_Y:
                    self.ship = (self.shipCoord, float(self.menu.menuTextInput[1].value),
                                 (float(self.mouse[0] - self.shipCoord[0]) / self.velCoef,
                                  float(self.mouse[1] - self.shipCoord[1]) / self.velCoef))

                    self.shipVelocityCheck = False
                    self.menu.notifyingWindow.text = ['']

                # dispose the ship
                if self.shipDispositionCheck and 0 < self.mouse[0] < constants.PLAYING_SCREEN_X:
                    self.shipDispositionCheck = False
                    self.shipVelocityCheck = True
                    self.shipCoord = self.mouse
                    self.menu.notifyingWindow.text = ['Enter the velocity of', 'the ship.']

    def checkPlanet(self):
        # checks if is possible to add the planet
        if self.currentMode != 'simulating' and self.currentMode != 'stop':
            if self.currentMode != 'setting':
                self.currentMode = 'setting'

            if self.menu.planetMassInput.value == '':
                self.menu.notifyingWindow.text = ['Please, enter', 'the mass of the', 'planet.']
            else:
                self.menu.notifyingWindow.text = ['Choose the position.']
                self.planetDispositionCheck = True
                self.shipDispositionCheck = False
                self.shipVelocityCheck = False

    def checkShip(self):
        # checks if is possible to add the ship
        if self.currentMode != 'simulating' and self.currentMode != 'stop':
            if self.currentMode != 'setting':
                self.currentMode = 'setting'

            if self.menu.shipMassInput.value == '':
                self.menu.notifyingWindow.text = ['Please, enter the', 'mass of the', 'ship.']
            else:
                self.ship = None
                self.menu.notifyingWindow.text = ['Choose the position.']
                self.shipDispositionCheck = True
                self.planetDispositionCheck = False

    def launchSimulator(self):
        # launches the simulation
        if self.simulationCanBeStarted():

            for planet in self.planets:
                self.simulationManager.simulation.planetSet(planet[0], planet[1])

            self.simulationManager.simulation.shipSet(self.ship[0], self.ship[1], self.ship[2])

            # if the simulation was run, but some parameters were changed, then calculations will be re-calculated.
            if self.simulationManager.simulation.accuracy != float(self.menu.menuTextInput[2].value):
                self.simulationManager.simulation.accuracySet(float(self.menu.menuTextInput[2].value))
                self.currentMode = 'setting'
                self.simulationManager.positions = []

            if self.simulationManager.simulation.tmax != float(self.menu.menuTextInput[3].value):
                self.simulationManager.simulation.tMaxSet(float(self.menu.menuTextInput[3].value))
                self.currentMode = 'setting'
                self.simulationManager.positions = []

            # if accuracy and tMax aren't conform, then...
            if self.simulationManager.runSimulating():
                self.simulationManager.trace = []
                self.currentMode = 'simulating'
                self.menu.notifyingWindow.text = ['Simulating...']
            else:
                self.menu.notifyingWindow.text = ['Please, set another', 'accuracy or tMax', 'parameters.']

    def simulationCanBeStarted(self):
        if not self.planets:
            self.menu.notifyingWindow.text = ['Please, set at least', 'one planet.']
            return False

        if not self.ship:
            self.menu.notifyingWindow.text = ['Please, set the ship.']
            return False

        return True

    def reset(self):
        self.currentMode = 'setting'
        self.simulation = Simulation()
        self.simulationManager = SimulationManager(self.simulation, self)

        self.ship = None
        self.shipDispositionCheck = False
        self.shipVelocityCheck = False
        self.shipCoord = (0, 0)

        self.planets = []
        self.planetDispositionCheck = False

        self.menu.notifyingWindow.text = ''

    def stopPlaying(self):
        if self.currentMode == 'simulating' and self.menu.menuButtons[3].title == 'stop playing':
            self.currentMode = 'stop'
            self.menu.menuButtons[3].title = 'continue'
        elif self.currentMode == 'stop' and self.menu.menuButtons[3].title == 'continue':
            self.currentMode = 'simulating'
            self.menu.menuButtons[3].title = 'stop playing'

    def quit(self):
        self.running = False

    def setSimulationMode(self):
        self.simulationManager = SimulationManager(self.simulation, self)
