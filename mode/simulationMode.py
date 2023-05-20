import pygame as pg
from .mode import Mode
from layer import BackgroundLayer


class SimulationMode(Mode):
    def __init__(self):
        super().__init__()

        self.cellSize = pg.Vector2(64, 64)

        self.layers = [
            BackgroundLayer(self.cellSize,)
        ]