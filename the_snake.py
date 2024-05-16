from gameparts.game_objects import Snake, Apple, JunkFood, Rock
from gameparts.constants import TURNS, BOARD_BACKGROUND_COLOR, screen, SPEED

import pygame


pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            game_object.next_direction = TURNS.get((event.key,
                                                    game_object.direction))


def get_occupied_cells(snake, *args):
    """Возвращает занятые ячейки на поле"""
    occupied_cells = []
    occupied_cells.extend(snake.positions)
    for arg in args:
        occupied_cells.append(arg.position)
    return occupied_cells


def fix_overlap(snake, *args):
    """Исправляет наложение объектов друг на друга"""
    for arg in args:
        while True:
            if get_occupied_cells(snake, *args).count(arg.position) > 1:
                arg.occupied_cells = get_occupied_cells(snake, *args)
                arg.randomize_position()
            else:
                break


def randomize_all_rocks(*args):
    """Рандомизирует положение всех камней на поле"""
    for arg in args:
        arg.randomize_position()


def draw_all_rocks(*args):
    """Рисует все камни на поле"""
    for arg in args:
        arg.draw()


def get_rocks_positions(*args):
    """Возвращает кортеж с текущими положениями камней"""
    rock_positions = []
    for arg in args:
        rock_positions.append(arg.position)
    return rock_positions


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
    randomize_all_rocks(*rocks)
    apple.randomize_position()
    burger.randomize_position()
    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        fix_overlap(snake, apple, burger, *rocks)
        handle_keys(snake)
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
        elif snake.get_head_position() in get_rocks_positions(*rocks):
            snake.reset()
            randomize_all_rocks(*rocks)
        if snake.positions.count(snake.get_head_position()) > 1:
            snake.reset()
        apple.draw()
        burger.draw()
        draw_all_rocks(rocks)
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
