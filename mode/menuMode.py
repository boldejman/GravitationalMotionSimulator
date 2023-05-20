import pygame as pg
import pygame_textinput
from .mode import Mode

class Button:
    def __init__(self, lu, rd):
        self.leftUp = lu
        self.rightDown = rd

    def __contains__(self, mouse):
        return self.leftUp[0] <= mouse[0] <= self.rightDown[0] and \
               self.leftUp[1] <= mouse[1] <= self.rightDown[1]


class MenuMode(Mode):
    def __init__(self):
        super().__init__()

        self.font = pg.font.SysFont(pg.font.get_fonts()[10], 15)
        self.x = 120
        self.y = 20
        self.menuButtons = [
            {
                "title": "add planet",
                "position": Button((860, 20), (860 + self.x, 20 + self.y)),
                "action": lambda: self.addPlanet(),
                "gotPressed": False
            },
            {
                "title": "add ship",
                "position": Button((860, 20+4*self.y), (860 + self.x, 20 + 5*self.y)),
                "action": lambda: self.addShip(),
                "gotPressed": False
            }
        ]

        self.accuracyInput = pygame_textinput.TextInputVisualizer()
        self.shipMassInput = pygame_textinput.TextInputVisualizer()
        self.planetMassInput = pygame_textinput.TextInputVisualizer()
        self.menuTextInput = [
            {
                "name": "planet mass",
                "position": Button((860, 20+2*self.y), (860 + self.x, 20 + 3*self.y)),
                "action": lambda: self.setPlanetMass(),
                "textInput": self.planetMassInput,
                "numberCount": 0
            },
            {
                "name": "ship mass",
                "position": Button((860, 20+6*self.y), (860 + self.x, 20 + 7*self.y)),
                "action": lambda: self.addShip(),
                "textInput": self.shipMassInput,
                "numberCount": 0
            },
            {
                "name": "set accuracy",
                "position": Button((860, 20 + 8*self.y), (860 + self.x, 20 + 9*self.y)),
                "action": lambda: self.setAccuracy(),
                "textInput": self.accuracyInput,
                "numberCount": 0
            }
        ]
        self.mouse = pg.mouse.get_pos()
        self.currentTextInput = -1
        self.running = True

    def setAccuracy(self):
        print(1)

    def shipMass(self):
        print(2)

    def addPlanet(self):
        print(3)

    def addShip(self):
        print(4)

    def setPlanetMass(self):
        print(5)

    def update(self):
        self.mouse = pg.mouse.get_pos()

    def processInput(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.notifyQuiRequested()

            if event.type == pg.MOUSEBUTTONUP:
                for item in self.menuButtons:
                    if self.mouse in item["position"]:
                        item["action"]()
                for index, item in enumerate(self.menuTextInput):
                    if self.mouse in item["position"]:
                        self.currentTextInput = index

            for index, item in enumerate(self.menuTextInput):
                if self.currentTextInput == index and event.type == pg.KEYDOWN:
                    # print(event.key)
                    if event.key == pg.K_0 or event.key == pg.K_1 or \
                       event.key == pg.K_2 or event.key == pg.K_3 or \
                       event.key == pg.K_4 or event.key == pg.K_5 or \
                       event.key == pg.K_6 or event.key == pg.K_7 or \
                       event.key == pg.K_8 or event.key == pg.K_9:
                        if item["numberCount"] < 10:
                            item["textInput"].update(events)
                            item["numberCount"] += 1
                        print(item["numberCount"])
                    if event.key == 8:     # = pg.K_DELETE
                        if item["numberCount"] > 0:
                            item["numberCount"] -= 1
                        item["textInput"].update(events)

    def render(self, screen):
        pg.draw.rect(screen, (210, 210, 210), (0, 0, 840, 720))
        pg.draw.rect(screen, (113, 121, 126), (840, 0, 240, 720))
        pg.draw.circle(screen, (255, 255, 255), (960, 600), 120)

        for item in self.menuButtons:
            pg.draw.rect(screen, (190, 190, 190), (item["position"].leftUp[0], item["position"].leftUp[1], self.x, self.y))
            surface = self.font.render(item["title"], True, (0, 0, 0))
            screen.blit(surface, item["position"].leftUp)

        for item in self.menuTextInput:
            pg.draw.rect(screen, (190, 190, 190), (item["position"].leftUp[0], item["position"].leftUp[1], self.x, self.y))
            surface = self.font.render(item["textInput"].value, True, (0, 0, 0))
            screen.blit(surface, item["position"].leftUp)


# pg.init()
# screen = pg.display.set_mode((1080, 720))
# running = True
# clock = pg.time.Clock()
# mode = Menu()
# while running:
#
#     mode.update()
#     mode.render(screen)
#     mode.processInput()
#     pg.display.update()
#     clock.tick(60)
#
# pg.display.quit()
