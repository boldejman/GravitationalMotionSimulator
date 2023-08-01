import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))

objs = []
o = []


class Obj:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.dragging = False
        self.color = color
        objs.append(self)
        self.name = ''

    def __repr__(self):
        return(self.name)

    def clicked(self, m_pos):
        return self.rect.collidepoint(m_pos)

    def set_offset(self, m_pos):
        self.dragging = True
        m_x, m_y = m_pos
        self.offset_x = self.rect.x - m_x
        self.offset_y = self.rect.y - m_y

    def drag(self, m_pos):
        m_x, m_y = m_pos
        self.rect.x = m_x + self.offset_x
        self.rect.y = m_y + self.offset_y

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

square1 = Obj(200, 170, 100, 100, (255, 0, 0))
square1.name = 'red'
square2 = Obj(150, 300, 100, 100, (0, 255, 0))
square2.name = 'green'
square3 = Obj(220, 30, 100, 100, (0, 0, 255))
square3.name = 'blue'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for square in objs:
                    if square.clicked(event.pos):
                        print(square)
                        print(o)
                        o = objs[objs.index(square)+1:]
                        print(o)
                        if not any(s.clicked(event.pos) for s in o):
                            objs.remove(square)
                            objs.append(square)
                            square.set_offset(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for square in objs:
                    square.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            for square in objs:
                if square.dragging:
                    square.drag(event.pos)
    screen.fill((255, 255, 255))
    for square in objs:
        square.draw()
    pygame.display.update()