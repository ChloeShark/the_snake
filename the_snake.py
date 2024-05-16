from gameparts.game_objects import Snake, Apple, JunkFood, Rock
from gameparts.constants import BOARD_BACKGROUND_COLOR, screen, SPEED
import gameparts.funcs as f

import pygame


pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


def main():
    """Главная функция"""
    pygame.init()
    snake = Snake()
    apple = Apple()
    burger = JunkFood()
    rock_1 = Rock()
    rock_2 = Rock()
    rock_3 = Rock()
    rocks = (rock_1, rock_2, rock_3)
    f.randomize_all_rocks(*rocks)
    apple.randomize_position()
    burger.randomize_position()
    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        f.fix_overlap(snake, apple, burger, *rocks)
        f.handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        elif snake.get_head_position() == burger.position:
            snake.length -= 1
            snake.positions.pop()
            burger.randomize_position()
            if snake.length < 1:
                snake.reset()
        elif snake.get_head_position() in f.get_rocks_positions(*rocks):
            snake.reset()
            f.randomize_all_rocks(*rocks)
        if snake.positions.count(snake.get_head_position()) > 1:
            snake.reset()
        apple.draw()
        burger.draw()
        f.draw_all_rocks(*rocks)
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
