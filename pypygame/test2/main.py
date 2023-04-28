import pygame as pg
from pygame.locals import *


pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
v = pg.Vector2()
v.x = 1
v.y = 2
v.normalize_ip()
print(type(v))


def main():
   while True:
      for event in pg.event.get():
            if event.type == QUIT:
               pg.quit()
               return
            elif event.type == MOUSEBUTTONUP:
               print(mouse)
               # print(event.x, event.y)
               # print(event.flipped)
               # # can access properties with
               # proper notation(ex: event.y)
      mouse = pg.mouse.get_pos()
      clock.tick(60)

# Execute game:
main()