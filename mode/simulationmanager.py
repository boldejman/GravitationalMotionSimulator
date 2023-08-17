import pygame as pg
import constants

from math import atan2, pi


class SimulationManager:
    def __init__(self, simulation, UI):
        self.ui = UI
        self.simulation = simulation
        self.positions = None
        self.playingProgress = 0

        self.ship = self.ui.ship
        self.planets = []
        self.dotTraceImage = pg.image.load('figures/trace_dot.png')
        self.trace = []
        self.mouse = None

        self.currentUnit = None

    def runSimulating(self):
        # checks if acc. and tMax are comform
        if self.ui.currentMode == 'setting':
            self.positions = self.simulation.getPositions()
            if len(self.positions) > 200:
                return True
            else:
                return False
        return True

    def getShipPos(self):
        if len(self.positions) > self.playingProgress + 100 * int(1 / self.simulation.accuracy / 10000)and \
                (self.ui.currentMode == 'simulating' or self.ui.currentMode == 'stop'):
            # calculates angle of the ship
            angle = -atan2(
                (self.positions[self.playingProgress + 100 * int(1 / self.simulation.accuracy / 10000)][1] - self.positions[self.playingProgress][1]),
                (self.positions[self.playingProgress + 100 * int(1 / self.simulation.accuracy / 10000)][0] - self.positions[self.playingProgress][0])) \
                * 180 / pi - 45

            if self.ui.currentMode == 'simulating':
                self.playingProgress += 100 * int(1 / self.simulation.accuracy / 10000)

            return self.positions[self.playingProgress - 100 * int(1 / self.simulation.accuracy / 10000)], angle

        else:
            self.ui.currentMode = 'done'
            self.ui.menu.notifyingWindow.text = ['Simulating done.']  # don know how to avoid this X(
            angle = -atan2(
                (self.positions[self.playingProgress - 100 * int(1 / self.simulation.accuracy / 10000)][1] - self.positions[self.playingProgress - 200 * int(1 / self.simulation.accuracy / 10000)][1]),
                (self.positions[self.playingProgress - 100 * int(1 / self.simulation.accuracy / 10000)][0] - self.positions[self.playingProgress - 200 * int(1 / self.simulation.accuracy / 10000)][0])) \
                * 180 / pi - 45
            self.playingProgress = 0
            return self.positions[-1], angle

    def update(self):
        self.mouse = self.ui.mouse
        self.ship = self.ui.ship
        self.planets = self.ui.planets
        self.currentUnit = self.ui.currentUnit

    def render(self, screen):
        if self.ui.currentMode == 'setting':

            if self.ui.planetDispositionCheck:
                self.currentUnit.render(screen, self.mouse)

            elif self.ui.shipDispositionCheck:
                self.currentUnit.render(screen, self.mouse, 0)

            elif self.ui.shipVelocityCheck:
                angle = 0
                if 0 < self.mouse[0] < constants.PLAYING_SCREEN_X and 0 < self.mouse[1] < constants.PLAYING_SCREEN_Y:
                    angle = -atan2(self.mouse[1] - self.currentUnit.y,
                                   self.mouse[0] - self.currentUnit.x) * 180 / pi - 45
                self.currentUnit.render(screen, (self.currentUnit.x, self.currentUnit.y), angle)

            if self.ui.units:
                for unit in self.ui.units:
                    if unit != self.ship:
                        unit.render(screen, (unit.x, unit.y))
                    else:
                        angle = -atan2(self.ship.vel[1], self.ship.vel[0]) * 180 / pi - 45
                        self.ship.render(screen, (self.ship.x, self.ship.y), angle)

        elif self.ui.currentMode == 'simulating' or self.ui.currentMode == 'stop' or self.ui.currentMode == 'done':
            pos, angle = self.getShipPos()
            self.trace.append(pos)
            for position in self.trace:
                screen.blit(self.dotTraceImage, (position[0], position[1]))
            self.ship.render(screen, pos, angle)

            for planet in self.planets:
                planet.render(screen, (planet.x, planet.y))
