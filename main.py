import pygame as pg
# from simulation import Simulation
from mode import ModeObserver, MenuMode, SimulationMode


class UserInterface(ModeObserver):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1080, 720))

        self.menu = MenuMode()
        self.menu.addObserver(self)

        self.mode = None

        self.currentMode = 'Setting'
        self.running = True
        self.clock = pg.time.Clock()

    def simulationModeRequested(self):
        self.currentMode = 'Simulation'
        self.mode = SimulationMode()

    def quitRequested(self):
        self.running = False

    def run(self):
        while self.running:
            self.menu.update()
            self.menu.processInput()
            self.menu.render(self.screen)

            if self.currentMode == 'Simulation':
                self.mode.render(self.screen)

            pg.display.update()
            self.clock.tick(60)


UI = UserInterface()
UI.run()
