import pygame as pg
# from simulation import Simulation
from mode import ModeObserver, MenuMode, SimulationMode


class UserInterface(ModeObserver):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1080, 720))

        self.menu = MenuMode()
        self.simulation = None
        self.currentMode = 'Setting'
        self.running = True

    def simulationMode(self):
        self.currentMode = 'Simulation'
        self.simulation = SimulationMode()

    def quitRequested(self):
        self.running = False

    def run(self):
        while self.running:
            self.menu.update()
            self.menu.processInput()

            if self.currentMode == 'Simulation':
                self.simulation.render()

UI = UserInterface()
UI.run()