from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS_SEQUENCE = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, содержащий общий атрибуты игровых объектов"""

    position = GRID_CENTER
    body_color = (0, 0, 0)

    def __init__(self, position=position, body_color=body_color):
        self.position = position
        self.color = body_color

    def draw(self):
        """
        Метод, определяющий отрисовку объектов на экране.
        Переопределяется в дочерних классах
        """
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко"""

    body_color = APPLE_COLOR

    @staticmethod
    def randomize_position():
        """Генерирует рандомные координаты для появления яблока на поле"""
        return (randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
                randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE)

    def __init__(self):
        self.position = Apple.randomize_position()
        self.color = Apple.body_color

    def draw(self):
        """Отрисовывает яблоко на экране"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку"""

    length = 1
    positions = [GRID_CENTER]
    direction = RIGHT
    next_direction = None
    body_color = SNAKE_COLOR

    def __init__(self):
        super().__init__(self.positions, self.body_color)
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
        screen.fill(BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает положение головы змейки"""
        return self.positions[0]

    def move(self):
        """Меняет положение змейки"""
        old_head_position = self.get_head_position()
        new_head_position = [old_head_position[0]
                             + self.direction[0] * GRID_SIZE,
                             old_head_position[1]
                             + self.direction[1] * GRID_SIZE]

        if new_head_position[0] > SCREEN_WIDTH - GRID_SIZE:
            new_head_position[0] = 0
        elif new_head_position[0] < 0:
            new_head_position[0] = SCREEN_WIDTH
        elif new_head_position[1] > SCREEN_HEIGHT - GRID_SIZE:
            new_head_position[1] = 0
        elif new_head_position[1] < 0:
            new_head_position[1] = SCREEN_HEIGHT

        new_head_position = tuple(new_head_position)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop(-1)
        # Проверка столкновений
        if self.positions.count(new_head_position) > 1:
            self.reset()

    # Метод draw класса Snake
    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last and self.last != self.positions[0]:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
