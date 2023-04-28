import pygame as pg
import pygame_textinput


class Button:
    def __init__(self, lu, rd):
        self.leftUp = lu
        self.rightDown = rd

    def __contains__(self, mouse):
        return self.leftUp[0] <= mouse[0] <= self.rightDown[0] and \
               self.leftUp[1] <= mouse[1] <= self.rightDown[1]


class Menu:
    def __init__(self):
        self.font = pg.font.SysFont(pg.font.get_fonts()[10], 15)
        self.menuItems = [
            {
                "title": "add planet",
                "position": Button((0, 0), (10, 8)),
                "action": lambda: self.addPlanet()
            },
            {
                "name": "planet mass",
                "position": Button((0, 10), (10, 18)),
                "action": lambda: self.setPlanetMass()
            },
            {
                "title": "ship mass",
                "position": Button((0, 20), (10, 28)),
                "action": lambda: self.shipMass()
            },
            {
                "name": "add ship",
                "position": Button((0, 30), (10, 38)),
                "action": lambda: self.addShip()
            },
            {
                "title": "set accuracy",
                "position": Button((0, 40), (10, 48)),
                "action": lambda: self.setAccuracy()
            }
        ]
        self.mouse = pg.mouse.get_pos()
        self.accuracyInput = pygame_textinput.TextInputVisualizer()
        self.shipMassInput = pygame_textinput.TextInputVisualizer()
        self.planetMassInput = pygame_textinput.TextInputVisualizer()


    def setAccuracy(self):
        pass

    def shipMass(self):
        pass

    def addPlanet(self):
        pass

    def addShip(self):
        pass

    def setPlanetMass(self):
        pass

    def processInput(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                for item in self.menuItems:
                    if self.mouse in item["position"]:
                        item["action"]()

    def render(self):
        pass

