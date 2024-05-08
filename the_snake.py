from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS_SEQUENCE = [UP, DOWN, LEFT, RIGHT]

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10

TURNS = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT
}
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, содержащий общие атрибуты игровых объектов"""

    def __init__(self, position=GRID_CENTER,
                 body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Метод, определяющий отрисовку объектов на экране.
        Переопределяется в дочерних классах
        """


class Apple(GameObject):
    """Класс, описывающий яблоко"""

    def __init__(self, position=GRID_CENTER, body_color=APPLE_COLOR,
                 occupied_cells=None):
        self.occupied_cells = occupied_cells or []
        super().__init__(position, body_color)

    def randomize_position(self):
        """Генерирует рандомные координаты для появления яблока на поле"""
        while True:
            new_position = (randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE)
            if new_position not in self.occupied_cells:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на экране"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку"""

    def __init__(self, position=GRID_CENTER, positions=[GRID_CENTER],
                 body_color=SNAKE_COLOR,
                 length=1, direction=RIGHT, next_direction=None):
        super().__init__(position, body_color)
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.positions = positions
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбрасывает змейку в начальное положение"""
        self.length = 1
        self.positions.clear()
        self.positions.append(GRID_CENTER)
        self.direction = choice(DIRECTIONS_SEQUENCE)

    def get_head_position(self):
        """Возвращает положение головы змейки"""
        return self.positions[0]

    def move(self):
        """Меняет положение змейки"""
        old_head_x, old_head_y = self.get_head_position()
        new_head_position = ((old_head_x + self.direction[0] * GRID_SIZE)
                             % SCREEN_WIDTH,
                             (old_head_y + self.direction[1] * GRID_SIZE)
                             % SCREEN_HEIGHT)

        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop(-1)

    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last and self.last != self.get_head_position:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            game_object.next_direction = TURNS.get((event.key,
                                                    game_object.direction))


def main():
    """Главная функция"""
    pygame.init()
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)
    apple.randomize_position()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.positions.count(snake.get_head_position()) > 1:
            snake.reset()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
