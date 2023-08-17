import pygame as pg


class Planet:
    def __init__(self):
        self.name = ''
        self.x = 0
        self.y = 0
        self.coord = [self.x, self.y]
        self.mass = 0
        # self.planPar = {
        #     "coord": 0,
        #     "mass": 0,
        # }
        self.dragging = False
        self.offset_x, self.offset_y = 0, 0

        self.planetImage = pg.image.load('figures/planet.png')
        self.size = self.planetImage.get_size()
        self.dragged = True

    def __repr__(self):
        return str(self.name)

    def __contains__(self, mouse):
        if self.x - self.size[0]/2 < mouse[0] < self.x + self.size[0]/2 \
                and self.y - self.size[0]/2 < mouse[1] < self.y + self.size[1]/2:
            return True
        return False

    def setMass(self, mass):
        self.mass = mass

    def set_offset(self, mouse):
        self.dragging = True
        m_x, m_y = mouse
        self.offset_x = self.x - m_x
        self.offset_y = self.y - m_y

    def drag(self, m_pos):
        m_x, m_y = m_pos
        self.x = m_x + self.offset_x  # + self.size[0]/2
        self.y = m_y + self.offset_y  # + self.size[1]/2

    def render(self, screen, pos, angle=0):
        originPos = (self.size[0]/2, self.size[1]/2)
        blitRotate(screen, self.planetImage, pos, originPos, angle, 1)


class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.coord = [self.x, self.y]
        self.mass = 0
        self.vel = (0, 0)
        # self.shipPar = {
        #     "coord": (0, 0),
        #     "vel": (0, 0),
        #     "mass": 0,
        # }

        self.dragging = False
        self.offset_x, self.offset_y = 0, 0

        self.shipImage = pg.image.load('figures/rocket3.png')
        self.size = self.shipImage.get_size()
        self.dragged = True

    def __contains__(self, mouse):
        if self.x - self.size[0]/2 < mouse[0] < self.x + self.size[0]/2 \
                and self.y - self.size[0]/2 < mouse[1] < self.y + self.size[1]/2:
            return True
        return False

    def setMass(self, mass):
        if isinstance(mass, float):
            self.mass = mass
        else:
            raise 'POSHEL NAHUJ'

    def set_offset(self, mouse):
        self.dragging = True
        m_x, m_y = mouse
        self.offset_x = self.x - m_x
        self.offset_y = self.y - m_y

    def drag(self, m_pos):
        m_x, m_y = m_pos
        self.x = m_x + self.offset_x
        self.y = m_y + self.offset_y

    def render(self, screen, pos, angle=0):
        originPos = (self.size[0] / 2, self.size[1] / 2)
        blitRotate(screen, self.shipImage, pos, originPos, angle, 1)


# Stack overflow function to rotating ship sprite
def blitRotate(surf, image, pos, originPos, angle, zoom):
    # calculate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pg.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pg.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    move = (-originPos[0] + min_box[0] - pivot_move[0], -originPos[1] - max_box[1] + pivot_move[1])
    origin = (pos[0] + zoom * move[0], pos[1] + zoom * move[1])

    # get a rotated image
    rotozoom_image = pg.transform.rotozoom(image, angle, zoom)

    # rotate and blit the image
    surf.blit(rotozoom_image, origin)

    # draw rectangle around the image