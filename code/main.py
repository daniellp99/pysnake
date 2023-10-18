from apple import Apple
from settings import (
    CELL_SIZE,
    COLS,
    DARK_GREEN,
    LIGHT_GREEN,
    ROWS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    exit,
    pygame,
)
from snake import Snake


class Main:
    def __init__(self) -> None:
        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PySnake")
        # game objects
        self.bg_rectangles = [
            pygame.Rect(
                (col + int(row % 2 == 0)) * CELL_SIZE,  # left
                row * CELL_SIZE,  # top
                CELL_SIZE,  # width
                CELL_SIZE,  # height
            )
            for col in range(0, COLS, 2)
            for row in range(ROWS)
        ]
        self.snake = Snake()
        self.apple = Apple(self.snake)

        # timer
        self.update_event = pygame.event.custom_type()
        pygame.time.set_timer(self.update_event, 200)

    def draw_bg(self):
        self.display_surface.fill(LIGHT_GREEN)
        for rect in self.bg_rectangles:
            pygame.draw.rect(self.display_surface, DARK_GREEN, rect)

    def input(self):
        keys = pygame.key.get_pressed()
        mapping_direction = {
            pygame.K_RIGHT: pygame.Vector2(1, 0),
            pygame.K_LEFT: pygame.Vector2(-1, 0),
            pygame.K_UP: pygame.Vector2(0, -1),
            pygame.K_DOWN: pygame.Vector2(0, 1),
        }
        for key, direction in mapping_direction.items():
            if keys[key]:
                self.snake.direction = direction

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == self.update_event:
                    self.snake.move()
            # move
            self.input()
            # drawing
            self.draw_bg()
            self.snake.draw()
            self.apple.draw()
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
