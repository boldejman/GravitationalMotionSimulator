from math import atan


class VelCircle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def velPar(self, mouse):
        a = mouse[0] - self.center[0]
        b = mouse[1] - self.center[1]
        return (a**2 + b**2)**0.5, atan(b/a)

    def renderCircle(self):
        pass

