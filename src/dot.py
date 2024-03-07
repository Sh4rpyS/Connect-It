import pygame, game, grid, editor

class Dot:
    dots = []

    def __init__(self, x: float, y: float, color: tuple) -> None:
        self.x = x
        self.y = y
        self.color = color

        if not self.color in grid.Tile.lines:
            grid.Tile.lines[self.color] = []

        self.size = (550 / game.level_size)
        self.radius = self.size / 3

        # Create the collider for the DOT object
        coll_x = self.x
        coll_y = self.y
        collider = pygame.Surface((self.size, self.size))
        self.collider_obj = game.screen.blit(collider, (coll_x, coll_y))

        # Change the X and Y to center the circle
        self.x += 550/game.level_size/2
        self.y += 550/game.level_size/2

        Dot.dots.append(self)
    
    def draw(self) -> None:
        self.object = pygame.draw.circle(game.screen, self.color, (self.x, self.y), self.radius)

class EditorDot:
    dots = []

    def __init__(self, x: float, y: float, color: tuple, editor_size: int) -> None:
        self.update_dot(x, y, color, editor_size)

        EditorDot.dots.append(self)

    def update_dot(self, x: float, y: float, color: tuple, editor_size: int) -> None:
        self.original_x = x
        self.original_y = y
        self.x = 25 + self.original_x * (550/editor_size)
        self.y = 125 + self.original_y * (550/editor_size)
        self.color = color

        self.size = (550 / editor_size)
        self.radius = self.size / 3

        self.coll_x = self.x
        self.coll_y = self.y
        self.collider = pygame.Surface((self.size-2, self.size-2))
        self.collider_obj = game.screen.blit(self.collider, (self.coll_x+1, self.coll_y+1))

        self.x += 550/editor_size/2
        self.y += 550/editor_size/2

    def draw(self) -> None:
        self.object = pygame.draw.circle(game.screen, self.color, (self.x, self.y), self.radius)

def Draw() -> None:
    for dot in Dot.dots:
        dot.draw()