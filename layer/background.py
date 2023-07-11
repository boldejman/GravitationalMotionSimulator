from .layer import Layer
import pygame as pg


class BackgroundLayer(Layer):
    def __init__(self, cellSize, imageFile, state, array, surfaceFlags=pg.SRCALPHA):
        super().__init__(cellSize, imageFile)
        self.state = state
        self.array = array
        self.surface = None
        self.surfaceFlags = surfaceFlags

    def render(self, surface):
        if self.surface is None:
            self.surface = pg.Surface(surface.get_size(), flags=self.surfaceFlags)
            self.renderTile(self.surface, pg.Vector2(0, 0), self.array)

        surface.blit(self.surface, (0, 0))
