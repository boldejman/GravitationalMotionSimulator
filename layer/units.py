from .layer import Layer


class UnitsLayer(Layer):
    def __init__(self, cellSize, imageFile, state, unit):
        super().__init__(cellSize, imageFile)
        self.state = state
        self.unit = unit
