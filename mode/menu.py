import pygame as pg
import constants
from pygame_textinput import TextInputVisualizer
from units import Ship, Planet


class Menu:
    def __init__(self, UI):
        self.ui = UI
        self.running = True

        # Window for notifying user about processes and issues
        self.notifyingWindow = NotifyingWindow((constants.MENU_SCREEN_X + 20, 20 + 18 * constants.y))

        self.menuButtons = [
            Button((constants.MENU_SCREEN_X + 20, 20),
                   'add planet', self.ui.checkPlanet),
            Button((constants.MENU_SCREEN_X + 20, 20 + 4 * constants.y),
                   'add ship', self.ui.checkShip),
            Button((constants.MENU_SCREEN_X + 20, 20 + 12 * constants.y),
                   'play simulation', self.ui.launchSimulator),
            Button((constants.MENU_SCREEN_X + 20, 20 + 14 * constants.y),
                   'stop playing', self.ui.stopPlaying),
            Button((constants.MENU_SCREEN_X + 20, 20 + 16 * constants.y),
                   'reset', self.ui.reset)
        ]

        self.planetMassInput = TextInputPlate((constants.MENU_SCREEN_X + 20, 20 + 2 * constants.y),
                                            'planet mass', False)

        self.shipMassInput = TextInputPlate((constants.MENU_SCREEN_X + 20, 20 + 6 * constants.y),
                                            'ship mass', False)

        self.accuracyInput = TextInputPlate((constants.MENU_SCREEN_X + 20, 20 + 8 * constants.y),
                                            'set accuracy', True)
        self.accuracyInput.value = '0.0001'

        self.tMax = TextInputPlate((constants.MENU_SCREEN_X + 20, 20 + 10 * constants.y),
                                            'set tMax(def. 15)', True)
        self.tMax.value = '15'

        self.menuTextInput = [
            self.planetMassInput,
            self.shipMassInput,
            self.accuracyInput,
            self.tMax
        ]

        pg.key.set_repeat(200, 25)

        self.mouse = None
        self.font = pg.font.SysFont(pg.font.get_fonts()[10], 15)
        self.events = None
        self.currentTextInput = -1

        self.planetMassIsChosen = False
        self.shipMassIsChosen = False

    def update(self):
        self.mouse = self.ui.mouse
        for index, textInput in enumerate(self.menuTextInput):
            if self.currentTextInput != index:
                textInput.isCurrent = False
        self.events = self.ui.events
        for item in self.menuTextInput:
            if not item.isCurrent:
                item.cursor_visible = False
            else:
                item.cursor_visible = True

        if self.ui.currentUnit:
            # print(self.ui.currentUnit)
            if isinstance(self.ui.currentUnit, Ship):
                self.shipMassIsChosen = True
                self.planetMassIsChosen = False
                # self.ui.currentUnit.setMass(float(self.shipMassInput.value))
                # self.shipMassInput.isCurrent = True
            elif isinstance(self.ui.currentUnit, Planet):
                self.planetMassIsChosen = True
                self.shipMassIsChosen = False
                # self.ui.currentUnit.setMass(float(self.planetMassInput.value))
                # self.planetMassInput.isCurrent = True
                # print('aaa')

    def processInput(self):
        for event in self.events:
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.MOUSEBUTTONUP:
                for item in self.menuButtons:
                    if self.mouse in item:
                        item.action()

                somethingWasChosen = False
                for index, item in enumerate(self.menuTextInput):
                    if self.mouse in item:
                        self.currentTextInput = index
                        item.isCurrent = True
                        somethingWasChosen = True

                if not somethingWasChosen:
                    for item in self.menuTextInput:
                        item.isCurrent = False
                        self.shipMassIsChosen = False
                        self.planetMassIsChosen = False

            if event.type == pg.KEYDOWN:
                for index, item in enumerate(self.menuTextInput):
                    if self.currentTextInput == index and item.isCurrent:
                        if event.key == pg.K_0 or event.key == pg.K_1 or \
                                event.key == pg.K_2 or event.key == pg.K_3 or \
                                event.key == pg.K_4 or event.key == pg.K_5 or \
                                event.key == pg.K_6 or event.key == pg.K_7 or \
                                event.key == pg.K_8 or event.key == pg.K_9 or \
                                event.key == pg.K_PERIOD:
                            if item.digitCounter < 10:
                                item.update(self.events)
                                item.digitCounter += 1

                            # if self.ui.currentUnit:
                            #     if isinstance(self.ui.currentUnit, Ship) and item is self.shipMassInput:
                            #         self.ui.currentUnit.setMass(float(self.shipMassInput.value))
                            #     elif isinstance(self.ui.currentUnit, Planet) and item is self.planetMassInput:
                            #         print(self.planetMassInput.value)
                            #         self.ui.currentUnit.setMass(float(self.planetMassInput.value))

                        elif event.key == pg.K_BACKSPACE:
                            if item.digitCounter > 0:
                                item.digitCounter -= 1
                            # item.cursor_visible = False
                            item.update(self.events)
                        elif event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                            # item.cursor_visible = False
                            item.update(self.events)
                        else:
                            pass

                        if self.planetMassIsChosen and item == self.planetMassInput and self.ui.currentUnit:
                            self.ui.currentUnit.setMass(float(item.value))

                        if self.shipMassIsChosen and item == self.shipMassInput and self.ui.currentUnit:
                            self.ui.currentUnit.setMass(float(item.value))

                # print(self.planetMassInput.value)

    def render(self, screen):
        pg.draw.rect(screen, (113, 121, 126), (constants.MENU_SCREEN_X, 0, 240, constants.MENU_SCREEN_Y))
        surface1 = self.font.render('Semester Project for MFF', True, (0, 0, 0))
        screen.blit(surface1, (constants.MENU_SCREEN_X + 10, constants.MENU_SCREEN_Y - 40))
        surface2 = self.font.render('Nail Sultanbekov', True, (0, 0, 0))
        screen.blit(surface2, (constants.MENU_SCREEN_X + 10, constants.MENU_SCREEN_Y - 20))

        for button in self.menuButtons:
            button.render(screen)

        self.notifyingWindow.render(screen)

        if self.planetMassIsChosen and isinstance(self.ui.currentUnit, Planet):
            self.planetMassInput.value = str(self.ui.currentUnit.mass)

        if self.shipMassIsChosen and isinstance(self.ui.currentUnit, Ship):
            self.shipMassInput.value = str(self.ui.currentUnit.mass)

        for textInput in self.menuTextInput:
            textInput.render(screen)


class Button:
    # Class for handle and render buttons
    def __init__(self, lu, title, action):
        self.leftUp = lu
        self.title = title
        self.action = action
        self.font = pg.font.SysFont(pg.font.get_fonts()[10], 15)

    def __contains__(self, mouse):
        return self.leftUp[0] <= mouse[0] <= self.leftUp[0] + constants.x and \
               self.leftUp[1] <= mouse[1] <= self.leftUp[1] + constants.y

    def render(self, screen):
        pg.draw.rect(screen, (190, 190, 190), (self.leftUp[0],
                                               self.leftUp[1], constants.x, constants.y))

        surface = self.font.render(self.title, True, (0, 0, 0))
        screen.blit(surface, self.leftUp)


class NotifyingWindow:
    # Class for process and render notifying window
    def __init__(self, lu):
        self.leftUp = lu
        self.text = []
        self.font = pg.font.SysFont(pg.font.get_fonts()[10], 15)

    def render(self, screen):
        pg.draw.rect(screen, (190, 190, 190), (self.leftUp[0],
                                               self.leftUp[1], constants.x, constants.y * 3))
        for index, line in enumerate(self.text):
            surface = self.font.render(line, True, (0, 0, 0))
            screen.blit(surface, (self.leftUp[0], self.leftUp[1] + index*constants.y))


class TextInputPlate(TextInputVisualizer):
    # Class for handle and render text input plate. It is inherited from TextInputVisualizer, that give me the easy way
    # to manipulate and rendering text.
    def __init__(self, lu, name, hasDef):
        super().__init__()
        self.hasDefaultValue = hasDef
        self.name = name
        self.leftUp = lu
        self.digitCounter = 0
        self.textFont = pg.font.SysFont(pg.font.get_fonts()[10], 15)
        self.font_object = pg.font.SysFont(pg.font.get_fonts()[10], 15)
        self.isCurrent = False
        self.cursor_visible = False

    def __contains__(self, mouse):
        return self.leftUp[0] <= mouse[0] <= self.leftUp[0] + constants.x and \
               self.leftUp[1] <= mouse[1] <= self.leftUp[1] + constants.y

    def render(self, screen):
        pg.draw.rect(screen, (190, 190, 190), (self.leftUp[0],
                                               self.leftUp[1], constants.x, constants.y))
        if self.isCurrent:
            screen.blit(self.surface, self.leftUp)
        else:
            if not self.hasDefaultValue and self.value != '':
                screen.blit(self.surface, self.leftUp)
            else:
                screen.blit(self.textFont.render(self.name, True, (0, 0, 0)), self.leftUp)


