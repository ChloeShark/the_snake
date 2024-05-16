import pygame
from gameparts.constants import TURNS


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
