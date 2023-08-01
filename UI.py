import pygame as pg
import constants
from mode import Menu, SimulationManager
from simulation import Simulation
from units import Ship, Planet


class UserInterface:
    # Class, that realising all logic of the app.
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((constants.SCREEN_X, constants.SCREEN_Y))
        self.clock = pg.time.Clock()
        self.mouse = None
        self.events = None
        self.running = True
        self.cnt = 0

        self.planets = []
        self.planetDispositionCheck = False  # it needs to dispose the planet

        self.ship = None
        self.shipDispositionCheck = False
        self.shipVelocityCheck = False
        self.velCoef = 5

        self.background = pg.image.load('figures/background_space.png')

        self.menu = Menu(self)
        self.simulation = Simulation()
        self.simulationManager = SimulationManager(self.simulation, self)
        self.currentMode = 'setting'

        self.currentUnit = None

        self.units = []

    def run(self):
        while self.running:
            self.update()
            self.menu.update()
            self.processInput()
            self.menu.processInput()
            self.screen.blit(self.background, (0, 0))
            self.simulationManager.update()
            self.simulationManager.render(self.screen)
            self.menu.render(self.screen)
            self.running = self.menu.running

            pg.display.update()
            self.clock.tick(60)

    def update(self):
        self.mouse = pg.mouse.get_pos()
        self.events = pg.event.get()
        # print(self.currentUnit)
        # for unit in self.units:
        #     print(unit.mass)

    def processInput(self):
        for event in self.events:

            if event.type == pg.MOUSEBUTTONDOWN:
                # dispose and save the planet
                if self.planetDispositionCheck and 0 < self.mouse[0] < constants.PLAYING_SCREEN_X and \
                        0 < self.mouse[1] < constants.PLAYING_SCREEN_Y:
                    self.currentUnit.x, self.currentUnit.y = self.mouse
                    self.cnt += 1
                    self.currentUnit.name = self.cnt
                    self.planets.append(self.currentUnit)

                    self.units.append(self.currentUnit)
                    self.planetDispositionCheck = False
                    self.currentUnit = None
                    self.menu.notifyingWindow.text = ['']

                # set the velocity of the ship and saving it
                elif self.shipVelocityCheck and 0 < self.mouse[0] < constants.PLAYING_SCREEN_X and \
                        0 < self.mouse[1] < constants.PLAYING_SCREEN_Y:
                    self.ship = self.currentUnit
                    self.ship.vel = (float(self.mouse[0] - self.ship.x) / self.velCoef,
                                     float(self.mouse[1] - self.ship.y) / self.velCoef)
                    self.units.append(self.ship)
                    self.shipVelocityCheck = False
                    self.currentUnit = None
                    self.menu.notifyingWindow.text = ['']

                # dispose the ship
                elif self.shipDispositionCheck and 0 < self.mouse[0] < constants.PLAYING_SCREEN_X:
                    self.currentUnit.x, self.currentUnit.y = self.mouse
                    self.shipDispositionCheck = False
                    self.shipVelocityCheck = True

                    self.menu.notifyingWindow.text = ['Enter the velocity of', 'the ship.']

                elif event.button == 1:
                    for unit in self.units:
                        if self.mouse in unit:
                            overlapUnits = self.units[self.units.index(unit) + 1:]
                            if not any(self.mouse in overlapUnit for overlapUnit in overlapUnits):
                                self.units.remove(unit)
                                self.units.append(unit)
                                unit.set_offset(self.mouse)
                                self.currentUnit = unit

                self.currentMode = 'setting'

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.currentUnit and not self.shipVelocityCheck and self.currentMode != 'simulating' and \
                            self.currentMode != 'stop':
                        self.currentUnit.dragging = False
                        self.currentUnit.dragged = True
                        # self.currentUnit = None
                        if any(self.mouse in unit for unit in self.units) or \
                                self.mouse in self.menu.shipMassInput or self.mouse in self.menu.planetMassInput:
                            pass
                        else:
                            self.currentUnit = None

            elif event.type == pg.MOUSEMOTION and self.currentMode != 'simulating' and self.currentMode != 'stop':
                if self.currentUnit and not self.shipVelocityCheck and self.currentUnit.dragging:
                    self.currentUnit.drag(self.mouse)

    def checkPlanet(self):
        # checks if is possible to add the planet
        if self.currentMode != 'simulating' and self.currentMode != 'stop':
            self.currentMode = 'setting'

            if self.menu.planetMassInput.value == '':
                self.menu.notifyingWindow.text = ['Please, enter', 'the mass of the', 'planet.']
            else:
                self.currentUnit = Planet()
                self.currentUnit.mass = float(self.menu.planetMassInput.value)
                self.menu.notifyingWindow.text = ['Choose the position.']
                self.planetDispositionCheck = True
                self.shipDispositionCheck = False
                self.shipVelocityCheck = False

    def checkShip(self):
        # checks if is possible to add the ship
        if self.currentMode != 'simulating' and self.currentMode != 'stop':
            self.currentMode = 'setting'

            if self.menu.shipMassInput.value == '':
                self.menu.notifyingWindow.text = ['Please, enter the', 'mass of the', 'ship.']
            else:
                self.currentUnit = Ship()
                self.ship = None
                for unit in self.units:
                    if isinstance(unit, Ship):
                        self.units.remove(unit)
                self.ship = self.currentUnit
                self.currentUnit.mass = float(self.menu.shipMassInput.value)
                self.menu.notifyingWindow.text = ['Choose the position.']
                self.shipDispositionCheck = True
                self.planetDispositionCheck = False

    def launchSimulator(self):
        # launches the simulation
        if self.simulationCanBeStarted():
            if any(unit.dragged for unit in self.units):
                for planet in self.planets:
                    planet.coord = [planet.x, planet.y]
                self.simulationManager.simulation.planetSet(self.planets)
                self.ship.coord = [self.ship.x, self.ship.y]
                self.simulationManager.simulation.shipSet(self.ship)
                self.currentMode = 'setting'
        for unit in self.units:
            unit.dragged = False

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

        elif not self.ship:
            self.menu.notifyingWindow.text = ['Please, set the ship.']
            return False

        elif self.menu.accuracyInput.value == '':
            self.menu.notifyingWindow.text = ['Please, set the ship.']
            return False

        elif self.menu.tMax.value == '':
            self.menu.notifyingWindow.text = ['Please, set the ship.']
            return False

        else:
            return True

    def reset(self):
        self.currentMode = 'setting'
        self.simulation = Simulation()
        self.simulationManager = SimulationManager(self.simulation, self)

        self.units.clear()

        # self.ship = None
        self.shipDispositionCheck = False
        self.shipVelocityCheck = False
        #
        self.planets.clear()
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
