from os import walk
from typing import Dict, List, Tuple

from pygame import Rect
from settings import CELL_SIZE, START_COL, START_LENGTH, START_ROW, pygame, join


class Snake:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.body = [
            pygame.Vector2(START_COL - col, START_ROW) for col in range(START_LENGTH)
        ]
        self.direction = pygame.Vector2(1, 0)
        self.has_eaten = False
        # graphics
        self.surfaces = self.import_surfs()
        self.draw_data: List[Tuple[Dict, Rect]] = []
        self.head_surf = self.surfaces["head_right"]
        self.tail_surf = self.surfaces["tail_left"]
        self.update_body()

    def import_surfs(self):
        surf_dict = {}
        for folder_path, _, images_name in walk(join("graphics", "snake")):
            for image_name in images_name:
                full_path = join(folder_path, image_name)
                image_surface = pygame.image.load(full_path).convert_alpha()
                surf_dict[image_name.split(".")[0]] = image_surface
        return surf_dict

    def reset(self):
        self.body = [
            pygame.Vector2(START_COL - col, START_ROW) for col in range(START_LENGTH)
        ]
        self.direction = pygame.Vector2(1, 0)

        self.update_head()
        self.update_tail()
        self.update_body()

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

        self.update_head()
        self.update_tail()
        self.update_body()

    def update_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == pygame.Vector2(-1, 0):
            self.head_surf = self.surfaces["head_right"]
        elif head_relation == pygame.Vector2(1, 0):
            self.head_surf = self.surfaces["head_left"]
        elif head_relation == pygame.Vector2(0, -1):
            self.head_surf = self.surfaces["head_down"]
        elif head_relation == pygame.Vector2(0, 1):
            self.head_surf = self.surfaces["head_up"]

    def update_tail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == pygame.Vector2(-1, 0):
            self.tail_surf = self.surfaces["tail_right"]
        elif tail_relation == pygame.Vector2(1, 0):
            self.tail_surf = self.surfaces["tail_left"]
        elif tail_relation == pygame.Vector2(0, -1):
            self.tail_surf = self.surfaces["tail_down"]
        elif tail_relation == pygame.Vector2(0, 1):
            self.tail_surf = self.surfaces["tail_up"]

    def update_body(self):
        self.draw_data = []
        for index, part in enumerate(self.body):
            x = part.x * CELL_SIZE
            y = part.y * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if index == 0:
                self.draw_data.append((self.head_surf, rect))
            elif index == len(self.body) - 1:
                self.draw_data.append((self.tail_surf, rect))
            else:
                last_part = self.body[index + 1] - part
                next_part = self.body[index - 1] - part
                if last_part.x == next_part.x:
                    self.draw_data.append((self.surfaces["body_horizontal"], rect))
                elif last_part.y == next_part.y:
                    self.draw_data.append((self.surfaces["body_vertical"], rect))
                else:
                    if (
                        last_part.x == -1
                        and next_part.y == -1
                        or last_part.y == -1
                        and next_part.x == -1
                    ):
                        self.draw_data.append((self.surfaces["body_tl"], rect))
                    elif (
                        last_part.x == -1
                        and next_part.y == 1
                        or last_part.y == 1
                        and next_part.x == -1
                    ):
                        self.draw_data.append((self.surfaces["body_bl"], rect))
                    elif (
                        last_part.x == 1
                        and next_part.y == -1
                        or last_part.y == -1
                        and next_part.x == 1
                    ):
                        self.draw_data.append((self.surfaces["body_tr"], rect))
                    elif (
                        last_part.x == 1
                        and next_part.y == 1
                        or last_part.y == 1
                        and next_part.x == 1
                    ):
                        self.draw_data.append((self.surfaces["body_br"], rect))

    def draw(self):
        for surf, rect in self.draw_data:
            self.display_surface.blit(surf, rect)
