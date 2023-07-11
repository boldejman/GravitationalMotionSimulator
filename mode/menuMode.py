import pygame as pg
import pygame_textinput
from .mode import Mode
from states import States
from simulation import Simulation
from .velocityCircle import VelCircle


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

        self.states = States()
        self.simulation = Simulation()
        self.simDone = False
        self.states.addObserver(self.simulation)
        self.currentMode = 'setting'

        self.font = pg.font.SysFont(pg.font.get_fonts()[10], 15)
        self.x = 180
        self.y = 20

        self.planets = []
        self.planetDispositionCheck = False
        self.planetImage = pg.image.load('figures/planet.png')

        self.ship = None
        self.shipDispositionCheck = False
        self.shipVelocityCheck = False
        self.shipCoord = (0, 0)
        self.shipImage = pg.image.load('figures/rocket3.png')
        self.velCoef = 10

        self.notifyingWindow = {
            "position": Button((860, 420), (860 + self.x, 420 + self.y*2)),
            "text": '',
        }

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
            },
            {
                "title": "launch simulation",
                "position": Button((860, 20 + 10 * self.y), (860 + self.x, 20 + 11 * self.y)),
                "action": lambda: self.launchSimulator(),
                "gotPressed": False
            }
        ]

        self.accuracyInput = pygame_textinput.TextInputVisualizer()
        self.shipMassInput = pygame_textinput.TextInputVisualizer()
        self.planetMassInput = pygame_textinput.TextInputVisualizer()

        pg.key.set_repeat(200, 25)
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
                "action": lambda: self.shipMass,
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
        self.background = pg.image.load("figures/background_space.png")

        self.mouse = pg.mouse.get_pos()
        self.currentTextInput = -1
        self.running = True
        self.velocityCircle = VelCircle((960, 600), 120)

        self.playingSpeed = 100
        self.positions = []

    @staticmethod
    def separateText(text):
        splittedText = text.split()
        fLine = ''
        sLine = ''
        i = 0
        lineLen = 0
        while i < len(splittedText) and lineLen + len(splittedText[i]) < 15:
            fLine += ' ' + splittedText[i]
            lineLen += len(splittedText[i])
            i += 1
        if i < len(splittedText):
            while i != len(splittedText):
                sLine += ' ' + splittedText[i]
                i += 1
        return fLine, sLine

    def launchSimulator(self):
        if self.simulationCanBeStarted():
            for planet in self.planets:
                self.states.notifyPlanetSet(planet[0], planet[1])

            self.states.notifyShipSet(self.ship[0], self.ship[1], self.ship[2])
            self.notifyingWindow['text'] = 'Please wait.'
            self.runSimulating()
            # self.simulation.rungeKutta()
            self.currentMode = 'simulating'

    def simulationCanBeStarted(self):
        if not self.planets:
            self.notifyingWindow['text'] = 'Please set at least one planet'
            return False

        if not self.ship:
            self.notifyingWindow['text'] = 'Please set a ship'
            return False

        return True

    def runSimulating(self):
         self.positions = self.simulation.getPositions()
         self.simDone = True

    def getShipPos(self):
        self.playingSpeed += 100
        return self.positions[self.playingSpeed - 100]

    def addPlanet(self):
        if self.menuTextInput[0]['textInput'].value == '':
            self.notifyingWindow['text'] = 'Please, enter the mass of planet.'
        else:
            self.notifyingWindow['text'] = 'Choose the position.'
            self.planetDispositionCheck = True

    def setAccuracy(self):
        pass

    def shipMass(self):
        pass

    def addShip(self):
        if self.menuTextInput[1]['textInput'].value == '':
            self.notifyingWindow['text'] = 'Please, enter the mass of ship.'
        else:
            self.notifyingWindow['text'] = 'Choose the position.'
            self.shipDispositionCheck = True

    def setPlanetMass(self):
        pass

    def update(self):
        self.mouse = pg.mouse.get_pos()

    def processInput(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.notifyQuiRequested()
                break

            if event.type == pg.MOUSEBUTTONUP:
                for item in self.menuButtons:
                    if self.mouse in item["position"]:
                        item["action"]()

                for index, item in enumerate(self.menuTextInput):
                    if self.mouse in item["position"]:
                        self.currentTextInput = index

                if self.planetDispositionCheck and 0 < self.mouse[0] < 840:
                    self.planets.append((self.mouse, int(self.menuTextInput[0]['textInput'].value)))
                    # self.states.notifyPlanetSet(self.mouse, int(self.menuTextInput[0]['textInput'].value))
                    self.planetDispositionCheck = False
                    self.notifyingWindow['text'] = ''

                if self.shipDispositionCheck and 0 < self.mouse[0] < 840:
                    # self.states.notifyShipSet(self.mouse, self.menuTextInput[1]['textInput'].value)
                    self.shipDispositionCheck = False
                    self.shipVelocityCheck = True
                    self.shipCoord = self.mouse
                    self.notifyingWindow['text'] = 'Enter the velocity in the circle.'

                if self.shipVelocityCheck and (int(self.mouse[0]-self.velocityCircle.center[0])**2 +
                                               int(self.mouse[1]-self.velocityCircle.center[1])**2)**0.5 <= \
                        self.velocityCircle.radius:

                    # self.states.notifyShipSet(self.shipCoord, int(self.menuTextInput[1]['textInput'].value),
                    #                           (int(self.mouse[0]-self.velocityCircle.center[0]),
                    #                            int(self.mouse[1]-self.velocityCircle.center[1])))
                    self.ship = (self.shipCoord, int(self.menuTextInput[1]['textInput'].value),
                                                    (int(self.mouse[0]-self.velocityCircle.center[0])/self.velCoef,
                                                     int(self.mouse[1]-self.velocityCircle.center[1])/self.velCoef))

                    self.shipVelocityCheck = False
                    self.notifyingWindow['text'] = ''

            for index, item in enumerate(self.menuTextInput):
                if self.currentTextInput == index and event.type == pg.KEYDOWN:
                    if event.key == pg.K_0 or event.key == pg.K_1 or \
                       event.key == pg.K_2 or event.key == pg.K_3 or \
                       event.key == pg.K_4 or event.key == pg.K_5 or \
                       event.key == pg.K_6 or event.key == pg.K_7 or \
                       event.key == pg.K_8 or event.key == pg.K_9:
                        if item["numberCount"] < 10:
                            item["textInput"].update(events)
                            item["numberCount"] += 1
                    if event.key == 8:     # = pg.K_DELETE
                        if item["numberCount"] > 0:
                            item["numberCount"] -= 1
                        item["textInput"].update(events)

    def render(self, screen):
        pg.draw.rect(screen, (210, 210, 210), (0, 0, 840, 720))
        pg.draw.rect(screen, (113, 121, 126), (840, 0, 240, 720))
        pg.draw.circle(screen, (255, 255, 255), (960, 600), 120)
        pg.draw.rect(screen, (190, 190, 190), (self.notifyingWindow["position"].leftUp[0],
                                               self.notifyingWindow["position"].leftUp[1], self.x, self.y * 2))
        screen.blit(self.background, (0, 0))

        if self.separateText(self.notifyingWindow['text']) != ('', ''):
            (fLine, sLine) = self.separateText(self.notifyingWindow['text'])
            surface2 = None
            surface1 = self.font.render(fLine.strip(), True, (0, 0, 0))
            if sLine.strip() != '':
                surface2 = self.font.render(sLine.strip(), True, (0, 0, 0))
            screen.blit(surface1, self.notifyingWindow["position"].leftUp)
            if surface2:
                screen.blit(surface2, (self.notifyingWindow["position"].leftUp[0],
                                       self.notifyingWindow["position"].leftUp[1] + self.y))

        for item in self.menuButtons:
            pg.draw.rect(screen, (190, 190, 190), (item["position"].leftUp[0],
                                                   item["position"].leftUp[1], self.x, self.y))
            surface = self.font.render(item["title"], True, (0, 0, 0))
            screen.blit(surface, item["position"].leftUp)

        for item in self.menuTextInput:
            pg.draw.rect(screen, (190, 190, 190), (item["position"].leftUp[0],
                                                   item["position"].leftUp[1], self.x, self.y))
            surface = self.font.render(item["textInput"].value, True, (0, 0, 0))
            screen.blit(surface, item["position"].leftUp)

        if self.planetDispositionCheck:
            screen.blit(self.planetImage, (self.mouse[0]-50, self.mouse[1]-50))

        for planet in self.planets:
            screen.blit(self.planetImage, (planet[0][0]-50, planet[0][1]-50))

        if self.shipDispositionCheck and self.currentMode == 'setting':
            screen.blit(self.shipImage, (self.mouse[0]-25, self.mouse[1]-24))

        if (self.ship or self.shipVelocityCheck) and self.currentMode == 'setting':
            screen.blit(self.shipImage, (self.shipCoord[0]-25, self.shipCoord[1]-24))

        if self.currentMode == 'simulating':
            screen.blit(self.shipImage, (self.getShipPos()[0]-25, self.getShipPos()[1]-24))


