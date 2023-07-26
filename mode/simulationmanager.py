import pygame as pg

import constants
from math import atan2, pi


class SimulationManager:
    def __init__(self, simulation, UI):
        self.ui = UI
        self.simulation = simulation
        self.positions = None
        self.playingProgress = 0

        self.planets = self.ui.planets
        self.ship = self.ui.ship
        self.dotTraceImage = pg.image.load('figures/trace_dot.png')
        self.trace = []
        self.mouse = None

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
        if len(self.positions) > self.playingProgress + 100 and self.ui.currentMode == 'simulating':
            # calculates angle of the ship
            angle = -atan2(
                (self.positions[self.playingProgress + 100][1] - self.positions[self.playingProgress][1]),
                (self.positions[self.playingProgress + 100][0] - self.positions[self.playingProgress][0])) \
                * 180 / pi - 45
            self.playingProgress += 100

            return self.positions[self.playingProgress - 100], angle
        elif self.ui.currentMode == 'stop':
            angle = -atan2(
                (self.positions[self.playingProgress + 100][1] - self.positions[self.playingProgress][1]),
                (self.positions[self.playingProgress + 100][0] - self.positions[self.playingProgress][0])) \
                * 180 / pi - 45
            return self.positions[self.playingProgress - 100], angle
        else:
            self.ui.currentMode = 'done'
            self.ui.menu.notifyingWindow.text = ['Simulating done.']  # don know how to avoid this X(
            angle = -atan2(
                (self.positions[self.playingProgress-100][1] - self.positions[self.playingProgress-200][1]),
                (self.positions[self.playingProgress-100][0] - self.positions[self.playingProgress-200][0])) \
                * 180 / pi - 45
            self.playingProgress = 0
            return self.positions[-1], angle

    def update(self):
        self.mouse = self.ui.mouse
        self.ship = self.ui.ship
        self.planets = self.ui.planets

    def render(self, screen):
        if self.ui.planetDispositionCheck:
            screen.blit(self.ui.planetImage, (self.ui.mouse[0] - 50, self.ui.mouse[1] - 50))

        if self.ui.shipDispositionCheck and self.ui.currentMode == 'setting':
            screen.blit(self.ui.shipImage, (self.ui.mouse[0] - 25, self.ui.mouse[1] - 24))

        if (self.ship or self.ui.shipVelocityCheck) and self.ui.currentMode == 'setting':
            w, h = self.ui.shipImage.get_size()
            angle = 0
            if self.ui.shipVelocityCheck and 0 < self.mouse[0] < constants.PLAYING_SCREEN_X and \
                        0 < self.mouse[1] < constants.PLAYING_SCREEN_Y:
                angle = -atan2(self.mouse[1] - self.ui.shipCoord[1],
                               self.mouse[0] - self.ui.shipCoord[0]) * 180 / pi - 45
            elif self.ship:
                angle = -atan2(self.ship[2][1], self.ship[2][0]) * 180 / pi - 45
            blitRotate(screen, self.ui.shipImage, (self.ui.shipCoord[0], self.ui.shipCoord[1]),
                       (w / 2, h / 2), angle, 1)

        if self.ui.currentMode == 'simulating' or self.ui.currentMode == 'stop' or self.ui.currentMode == 'done':
            pos, angle = self.getShipPos()
            w, h = self.ui.shipImage.get_size()
            self.trace.append(pos)
            for position in self.trace:
                screen.blit(self.dotTraceImage, (position[0], position[1]))
            blitRotate(screen, self.ui.shipImage, (pos[0], pos[1]), (w / 2, h / 2), angle, 1)

        for planet in self.planets:
            screen.blit(self.ui.planetImage, (planet[0][0] - 50, planet[0][1] - 50))


# Stack overflow function to rotating ship sprite
def blitRotate(surf, image, pos, originPos, angle, zoom):
    # calculate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pg.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pg.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    move = (-originPos[0] + min_box[0] - pivot_move[0], -originPos[1] - max_box[1] + pivot_move[1])
    origin = (pos[0] + zoom * move[0], pos[1] + zoom * move[1])

    # get a rotated image
    rotozoom_image = pg.transform.rotozoom(image, angle, zoom)

    # rotate and blit the image
    surf.blit(rotozoom_image, origin)

    # draw rectangle around the image
