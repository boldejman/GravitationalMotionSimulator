# rudiment, that can be useful then...

# import pygame as pg
#
#
# class VelCircle:
#     def __init__(self, center, radius):
#         self.center = center
#         self.radius = radius
#
#     def __contains__(self, mouse):
#         if (int(mouse[0] - self.center[0]) ** 2 + int(mouse[1] - self.center[1]) ** 2) ** 0.5 <= self.radius:
#             return True
#         else:
#             return False
#
#     def render(self, screen):
#         pg.draw.circle(screen, (255, 255, 255), (960, 600), 120)
#
