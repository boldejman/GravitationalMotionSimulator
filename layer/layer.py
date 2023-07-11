from pygame import Rect
import pygame as pg


class Layer:
    def __init__(self, cellSize, imageFile):
        self.cellSize = cellSize
        self.texture = pg.image.load(imageFile)

    @property
    def cellWidth(self):
        return int(self.cellSize.x)

    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def renderTile(self, surface, position, tile, angle=None):
            # Location on screen
            spritePoint = position.elementwise() * self.cellSize

            # Texture
            texturePoint = tile.elementwise() * self.cellSize
            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), self.cellWidth, self.cellHeight)

            # Draw
            if angle is None:
                surface.blit(self.texture, spritePoint, textureRect)
            else:
                # Extract the tile in a surface
                textureTile = pg.Surface((self.cellWidth, self.cellHeight), pg.SRCALPHA)
                textureTile.blit(self.texture, (0, 0), textureRect)
                # Rotate the surface with the tile
                rotatedTile = pg.transform.rotate(textureTile, angle)
                # Compute the new coordinate on the screen, knowing that we rotate around the center of the tile
                spritePoint.x -= (rotatedTile.get_width() - textureTile.get_width()) // 2
                spritePoint.y -= (rotatedTile.get_height() - textureTile.get_height()) // 2
                # Render the rotatedTile
                surface.blit(rotatedTile, spritePoint)

    def render(self, surface):
        pass