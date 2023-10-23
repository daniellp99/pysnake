from apple import Apple
from settings import (
    CELL_SIZE,
    COLS,
    DARK_GREEN,
    LIGHT_GREEN,
    ROWS,
    SHADOW_OPACITY,
    SHADOW_SIZE,
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
        self.game_active = False

    def draw_bg(self):
        self.display_surface.fill(LIGHT_GREEN)
        for rect in self.bg_rectangles:
            pygame.draw.rect(self.display_surface, DARK_GREEN, rect)

    def draw_shadows(self):
        shadow_surf = pygame.Surface(self.display_surface.get_size())
        shadow_surf.fill((0, 255, 0))
        shadow_surf.set_colorkey((0, 255, 0))

        # surfaces
        shadow_surf.blit(
            self.apple.scaled_surface, self.apple.scaled_rect.topleft + SHADOW_SIZE
        )
        for surf, rect in self.snake.draw_data:
            shadow_surf.blit(surf, rect.topleft + SHADOW_SIZE)

        mask = pygame.mask.from_surface(shadow_surf)
        mask.invert()
        shadow_surf = mask.to_surface()
        shadow_surf.set_colorkey((255, 255, 255))
        shadow_surf.set_alpha(SHADOW_OPACITY)

        self.display_surface.blit(shadow_surf, (0, 0))

    def input(self):
        keys = pygame.key.get_pressed()
        mapping_direction = {
            pygame.K_RIGHT: pygame.Vector2(1, 0)
            if self.snake.direction.x != -1
            else self.snake.direction,
            pygame.K_LEFT: pygame.Vector2(-1, 0)
            if self.snake.direction.x != 1
            else self.snake.direction,
            pygame.K_UP: pygame.Vector2(0, -1)
            if self.snake.direction.y != 1
            else self.snake.direction,
            pygame.K_DOWN: pygame.Vector2(0, 1)
            if self.snake.direction.y != -1
            else self.snake.direction,
        }
        for key, direction in mapping_direction.items():
            if keys[key]:
                self.snake.direction = direction

    def collision(self):
        # eat apple
        if self.snake.body[0] == self.apple.pos:
            self.snake.has_eaten = True
            self.apple.set_pos()
        # game over
        if (
            self.snake.body[0] in self.snake.body[1:]
            or not 0 <= self.snake.body[0].x < COLS
            or not 0 <= self.snake.body[0].y < ROWS
        ):
            self.snake.reset()
            self.game_active = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == self.update_event and self.game_active:
                    self.snake.move()

                if event.type == pygame.KEYDOWN and not self.game_active:
                    self.game_active = True

            # move
            self.input()
            self.collision()
            # drawing
            self.draw_bg()
            self.draw_shadows()
            self.snake.draw()
            self.apple.draw()
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
