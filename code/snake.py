from settings import (
    CELL_SIZE,
    START_COL,
    START_LENGTH,
    START_ROW,
    pygame,
)


class Snake:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.body = [
            pygame.Vector2(START_COL - col, START_ROW) for col in range(START_LENGTH)
        ]
        self.direction = pygame.Vector2(1, 0)
        self.has_eaten = False

    def move(self):
        if not self.has_eaten:
            body_copy = self.body[:-1]
            new_head = body_copy[0] + self.direction
            body_copy.insert(0, new_head)
            self.body = body_copy[:]
        else:
            body_copy = self.body[:]
            new_head = body_copy[0] + self.direction
            body_copy.insert(0, new_head)
            self.body = body_copy[:]
            self.has_eaten = False

    def draw(self):
        for point in self.body:
            rect = pygame.Rect(
                point.x * CELL_SIZE,
                point.y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(self.display_surface, "red", rect)
