import pygame as pg
from .mode import Mode
from layer import BackgroundLayer, TraceLayer
from states import States

class SimulationMode(Mode):
    def __init__(self):
        super().__init__()
        self.state = States()
        self.cellSize = pg.Vector2(64, 64)

        self.layers = [
            # BackgroundLayer(self.cellSize, "figures/background_space.png", self.state,self.state.background, 0),
            TraceLayer(self.cellSize, "figures/dot.png", self.state, self.state.trace)

        ]