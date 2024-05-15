from random import choice, randint
import gameparts.constants as const
import pygame


class GameObject:
    """Базовый класс, содержащий общие атрибуты игровых объектов"""

    def __init__(self, position=const.GRID_CENTER,
                 body_color=const.BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Метод, определяющий отрисовку объектов на экране.
        Переопределяется в дочерних классах
        """


class Apple(GameObject):
    """Класс, описывающий яблоко"""

    def __init__(self, position=const.GRID_CENTER,
                 body_color=const.APPLE_COLOR,
                 occupied_cells=None):
        self.occupied_cells = occupied_cells or []
        super().__init__(position, body_color)

    def randomize_position(self):
        """Генерирует рандомные координаты для появления яблока на поле"""
        while True:
            new_position = (randint(1, const.GRID_WIDTH - 1)
                            * const.GRID_SIZE,
                            randint(1, const.GRID_HEIGHT - 1)
                            * const.GRID_SIZE)
            if new_position not in self.occupied_cells:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на экране"""
        rect = pygame.Rect(self.position, (const.GRID_SIZE, const.GRID_SIZE))
        pygame.draw.rect(const.screen, self.body_color, rect)
        pygame.draw.rect(const.screen, const.BORDER_COLOR, rect, 1)


class JunkFood(GameObject):
    """Класс, описывающий вредную еду"""

    def __init__(self, position=const.GRID_CENTER,
                 body_color=const.JUNKFOOD_COLOR,
                 occupied_cells=None):
        self.occupied_cells = occupied_cells or []
        super().__init__(position, body_color)

    def randomize_position(self):
        """Генерирует рандомные координаты для появления вредной еды на поле"""
        while True:
            new_position = (randint(1, const.GRID_WIDTH - 1)
                            * const.GRID_SIZE,
                            randint(1, const.GRID_HEIGHT - 1)
                            * const.GRID_SIZE)
            if new_position not in self.occupied_cells:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает вредную еду на экране"""
        rect = pygame.Rect(self.position, (const.GRID_SIZE, const.GRID_SIZE))
        pygame.draw.rect(const.screen, self.body_color, rect)
        pygame.draw.rect(const.screen, const.BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку"""

    def __init__(self, position=const.GRID_CENTER,
                 positions=[const.GRID_CENTER],
                 body_color=const.SNAKE_COLOR,
                 length=1, direction=const.RIGHT, next_direction=None):
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
        self.positions.append(const.GRID_CENTER)
        self.direction = choice(const.DIRECTIONS_SEQUENCE)

    def get_head_position(self):
        """Возвращает положение головы змейки"""
        return self.positions[0]

    def move(self):
        """Меняет положение змейки"""
        old_head_x, old_head_y = self.get_head_position()
        new_head_position = ((old_head_x + self.direction[0] * const.GRID_SIZE)
                             % const.SCREEN_WIDTH,
                             (old_head_y + self.direction[1] * const.GRID_SIZE)
                             % const.SCREEN_HEIGHT)

        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop(-1)

    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions:
            rect = (pygame.Rect(position, (const.GRID_SIZE, const.GRID_SIZE)))
            pygame.draw.rect(const.screen, self.body_color, rect)
            pygame.draw.rect(const.screen, const.BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.get_head_position(),
                                (const.GRID_SIZE, const.GRID_SIZE))
        pygame.draw.rect(const.screen, self.body_color, head_rect)
        pygame.draw.rect(const.screen, const.BORDER_COLOR, head_rect, 1)
        if self.last and self.last != self.get_head_position:
            last_rect = pygame.Rect(self.last, (const.GRID_SIZE,
                                                const.GRID_SIZE))
            pygame.draw.rect(const.screen, const.BOARD_BACKGROUND_COLOR,
                             last_rect)


class Rock(GameObject):
    """Описывает препядствие"""

    def __init__(self, position=const.GRID_CENTER,
                 body_color=const.ROCK_COLOR,
                 occupied_cells=None):
        super().__init__(position, body_color)
        self.occupied_cells = occupied_cells or []

    def randomize_position(self):
        """Генерирует рандомные координаты для появления препядствия на поле"""
        while True:
            new_position = (randint(1, const.GRID_WIDTH - 1)
                            * const.GRID_SIZE,
                            randint(1, const.GRID_HEIGHT - 1)
                            * const.GRID_SIZE)
            if new_position not in self.occupied_cells:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает препядствие на экране"""
        rect = pygame.Rect(self.position, (const.GRID_SIZE, const.GRID_SIZE))
        pygame.draw.rect(const.screen, self.body_color, rect)
        pygame.draw.rect(const.screen, const.BORDER_COLOR, rect, 1)
