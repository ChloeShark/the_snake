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


def get_occupied_cells(snake, apple, burger, rock):
    """Возвращает занятые ячейки на поле"""
    occupied_cells = []
    occupied_cells.extend(snake.positions)
    occupied_cells.append(apple.position)
    occupied_cells.append(burger.position)
    occupied_cells.append(rock.position)
    return occupied_cells


def fix_overlap(snake, apple, burger, rock):
    """Исправляет наложение объектов друг на друга"""
    while True:
        if get_occupied_cells(snake,
                              apple, burger, rock).count(apple.position) > 1:
            apple.occupied_cells = get_occupied_cells(snake,
                                                      apple, burger, rock)
            apple.randomize_position()
        elif get_occupied_cells(snake, apple,
                                burger, rock).count(burger.position) > 1:
            burger.occupied_cells = get_occupied_cells(snake,
                                                       apple, burger, rock)
            burger.randomize_position()
        elif get_occupied_cells(snake,
                                apple, burger, rock).count(rock.position) > 1:
            rock.occupied_cells = get_occupied_cells(snake,
                                                     apple, burger, rock)
            rock.randomize_position()
        else:
            break


def main():
    """Главная функция"""
    pygame.init()
    snake = Snake()
    apple = Apple()
    burger = JunkFood()
    rock = Rock()
    apple.randomize_position()
    burger.randomize_position()
    rock.randomize_position()
    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        fix_overlap(snake, apple, burger, rock)
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
        elif snake.get_head_position() == rock.position:
            snake.reset()
            rock.randomize_position()
        if snake.positions.count(snake.get_head_position()) > 1:
            snake.reset()
        apple.draw()
        burger.draw()
        rock.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
