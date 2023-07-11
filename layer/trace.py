from .layer import Layer


class TraceLayer(Layer):
    def __init__(self, cellSize, imageFile, state, trace):
        super().__init__(cellSize, imageFile)
        self.state = state
        self.trace = trace

    def render(self, surface):
        pass
