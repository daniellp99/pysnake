from math import sin
from random import choice
from settings import join

from settings import (
    CELL_SIZE,
    COLS,
    ROWS,
    pygame,
)
from snake import Snake


class Apple:
    def __init__(self, snake: Snake) -> None:
        self.pos = pygame.Vector2()
        self.display_surface = pygame.display.get_surface()
        self.snake = snake
        self.set_pos()
        self.surface_image = pygame.image.load(
            join("graphics", "apple.png")
        ).convert_alpha()

    def set_pos(self):
        available_pos = [
            pygame.Vector2(x, y)
            for x in range(COLS)
            for y in range(ROWS)
            if pygame.Vector2(x, y) not in self.snake.body
        ]
        self.pos = choice(available_pos)

    def draw(self):
        scale = 1 + sin(pygame.time.get_ticks() / 500) / 3
        self.scaled_surface = pygame.transform.smoothscale_by(self.surface_image, scale)
        self.scaled_rect = self.scaled_surface.get_rect(
            center=(
                self.pos.x * CELL_SIZE + CELL_SIZE / 2,
                self.pos.y * CELL_SIZE + CELL_SIZE / 2,
            )
        )
        self.display_surface.blit(self.scaled_surface, self.scaled_rect)
