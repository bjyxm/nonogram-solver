import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
GRID_LINE_WIDTH = 1


class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.n_rows = len(rows)
        self.columns = columns
        self.n_columns = len(columns)
        self.array = ['□'] * self.n_rows * self.n_columns

        # for pygame rendering
        self.screen = None
        self.background = None
        self.left_margin = 0
        self.top_margin = 0

    def render_frame(self, cell_size=20, video_fps=10, padding=1):
        if self.screen is None:
            pygame.init()
            pygame.display.set_caption('nonogram Solver')

            max_row_count = max([len(x) for x in self.rows])
            max_column_count = max([len(x) for x in self.columns])
            self.left_margin = max_row_count * cell_size
            self.top_margin = max_column_count * cell_size

            width = self.n_columns * cell_size + (self.n_columns + 1) * GRID_LINE_WIDTH + self.left_margin
            height = self.n_rows * cell_size + (self.n_rows + 1) * GRID_LINE_WIDTH + self.top_margin

            self.screen = pygame.display.set_mode((width, height))
            self.background = pygame.Surface((width, height)).convert()
            self.background.fill(WHITE)

            for i in range(self.n_columns + 1):
                x = i * (cell_size + GRID_LINE_WIDTH) + self.left_margin
                pygame.draw.line(self.background, GRAY, (x, 0), (x, height))
            for i in range(self.n_rows + 1):
                y = i * (cell_size + GRID_LINE_WIDTH) + self.top_margin
                pygame.draw.line(self.background, GRAY, (0, y), (width, y))

            font = pygame.font.Font(None, int(cell_size * 1.35))
            for idx_x in range(len(self.columns)):
                x = idx_x * (cell_size + GRID_LINE_WIDTH) + self.left_margin
                y = self.top_margin - cell_size
                for idx_number in reversed(range(len(self.columns[idx_x]))):
                    number = self.columns[idx_x][idx_number]
                    surface_number = font.render(str(number), True, BLACK)
                    local_x = x + (cell_size - surface_number.get_width()) // 2
                    local_y = y + (cell_size - surface_number.get_height()) // 2
                    self.background.blit(surface_number, (local_x, local_y))
                    y -= cell_size

            for idx_y in range(len(self.rows)):
                x = self.left_margin - cell_size
                y = idx_y * (cell_size + GRID_LINE_WIDTH) + self.top_margin
                for idx_number in reversed(range(len(self.rows[idx_y]))):
                    number = self.rows[idx_y][idx_number]
                    surface_number = font.render(str(number), True, BLACK)
                    local_x = x + (cell_size - surface_number.get_width()) // 2
                    local_y = y + (cell_size - surface_number.get_height()) // 2
                    self.background.blit(surface_number, (local_x, local_y))
                    x -= cell_size

        clock = pygame.time.Clock()
        self.screen.blit(self.background, (0, 0))

        for i in range(len(self.array)):
            idx_y, idx_x = divmod(i, self.n_columns)
            x_1 = idx_x * (cell_size + GRID_LINE_WIDTH) + self.left_margin + GRID_LINE_WIDTH
            x_2 = x_1 + cell_size - 1
            y_1 = idx_y * (cell_size + GRID_LINE_WIDTH) + self.top_margin + GRID_LINE_WIDTH
            y_2 = y_1 + cell_size - 1
            x_1 += padding
            x_2 -= padding
            y_1 += padding
            y_2 -= padding
            if self.array[i] == '■':
                pygame.draw.polygon(self.screen, BLACK, [(x_1, y_1), (x_2, y_1), (x_2, y_2), (x_1, y_2)])
            elif self.array[i] == '×':
                pygame.draw.line(self.screen, RED, (x_1, y_1), (x_2, y_2), 2)
                pygame.draw.line(self.screen, RED, (x_2, y_1), (x_1, y_2), 2)

        pygame.display.update()
        clock.tick(video_fps)

    def render_grid(self, cell_size=20, video_fps=10, padding=1):
        if self.screen is None:
            pygame.init()
            pygame.display.set_caption('nonogram Solver')
            width = self.n_columns * cell_size + (self.n_columns - 1) * GRID_LINE_WIDTH
            height = self.n_rows * cell_size + (self.n_rows - 1) * GRID_LINE_WIDTH

            self.screen = pygame.display.set_mode((width, height))
            self.background = pygame.Surface((width, height)).convert()
            self.background.fill(WHITE)
            for idx_x in range(1, self.n_columns):
                x = idx_x * (cell_size + GRID_LINE_WIDTH) - 1
                pygame.draw.line(self.background, GRAY, (x, 0), (x, height))
            for idx_y in range(1, self.n_rows):
                y = idx_y * (cell_size + GRID_LINE_WIDTH) - 1
                pygame.draw.line(self.background, GRAY, (0, y), (width, y))

        clock = pygame.time.Clock()
        self.screen.blit(self.background, (0, 0))

        for i in range(len(self.array)):
            idx_y, idx_x = divmod(i, self.n_columns)
            x_1 = idx_x * (cell_size + GRID_LINE_WIDTH)
            x_2 = x_1 + cell_size - 1
            y_1 = idx_y * (cell_size + GRID_LINE_WIDTH)
            y_2 = y_1 + cell_size - 1
            x_1 += padding
            x_2 -= padding
            y_1 += padding
            y_2 -= padding
            if self.array[i] == '■':
                pygame.draw.polygon(self.screen, BLACK, [(x_1, y_1), (x_2, y_1), (x_2, y_2), (x_1, y_2)])
            elif self.array[i] == '×':
                pygame.draw.line(self.screen, RED, (x_1, y_1), (x_2, y_2), 2)
                pygame.draw.line(self.screen, RED, (x_2, y_1), (x_1, y_2), 2)

        pygame.display.update()
        clock.tick(video_fps)

    def render_simple(self, cell_size=20, video_fps=10):
        if self.screen is None:
            pygame.init()
            pygame.display.set_caption('nonogram Solver')
            width = self.n_columns * cell_size
            height = self.n_rows * cell_size

            self.screen = pygame.display.set_mode((width, height))
            self.background = pygame.Surface((width, height)).convert()
            self.background.fill(WHITE)

        clock = pygame.time.Clock()
        self.screen.blit(self.background, (0, 0))

        for i in range(len(self.array)):
            idx_y, idx_x = divmod(i, self.n_columns)
            y = idx_y * cell_size
            x = idx_x * cell_size
            if self.array[i] == '■':
                pygame.draw.polygon(self.screen, BLACK,
                                    [(x, y), (x + cell_size - 1, y), (x + cell_size - 1, y + cell_size - 1),
                                     (x, y + cell_size - 1)])
            elif self.array[i] == '×':
                pygame.draw.line(self.screen, RED, (x, y), (x + cell_size - 1, y + cell_size - 1), 2)
                pygame.draw.line(self.screen, RED, (x + cell_size - 1, y), (x, y + cell_size - 1), 2)
        pygame.display.update()
        clock.tick(video_fps)

    def get_row(self, n):
        return self.array[n * self.n_columns:(n + 1) * self.n_columns]

    def set_row(self, n, array):
        changed = False
        idx_start = n * self.n_columns
        for i in range(self.n_columns):
            if self.array[idx_start + i] != array[i]:
                changed = True
            self.array[idx_start + i] = array[i]
        return changed

    def get_column(self, n):
        column = list()
        for i in range(self.n_rows):
            value_of_each_row = self.array[i * self.n_columns + n]
            column.append(value_of_each_row)
        return column

    def set_column(self, n, array):
        changed = False
        for i in range(self.n_rows):
            if self.array[i * self.n_columns + n] != array[i]:
                changed = True
            self.array[i * self.n_columns + n] = array[i]
        return changed

    def set_cell(self, i, v):
        self.array[i] = v

    def is_complete(self):
        for r in range(self.n_rows):
            row = self.get_row(r)
            built = self.__build_numbers__(row)
            correct = self.rows[r]
            if built != correct:
                return False

        for c in range(self.n_columns):
            column = self.get_column(c)
            built = self.__build_numbers__(column)
            correct = self.columns[c]
            if built != correct:
                return False

        return self.array.count('□') == 0

    def locate_first_empty(self):
        for i in range(len(self.array)):
            if self.array[i] == '□':
                return i

    def is_valid(self):
        for r in range(self.n_rows):
            row = self.get_row(r)
            built = self.__build_numbers__(row)
            correct = self.rows[r]

            if max(built) > max(correct):
                return False
            elif sum(built) > sum(correct):
                return False
            elif len(built) > len(correct):
                return False
            elif row.count('□') == 0 and built != correct:
                return False

        for c in range(self.n_columns):
            column = self.get_column(c)
            built = self.__build_numbers__(column)
            correct = self.columns[c]

            if max(built) > max(correct):
                return False
            elif sum(built) > sum(correct):
                return False
            elif len(built) > len(correct):
                return False
            elif column.count('□') == 0 and built != correct:
                return False

        return True

    def is_valid_2(self):
        for r in range(self.n_rows):
            row = self.get_row(r)
            built = self.__build_numbers__(row)
            correct = self.rows[r]

            if len(built) > len(correct):
                return False

            for i in range(len(built)):
                if built[i] > correct[i]:
                    return False

            if row.count('□') == 0 and built != correct:
                return False

        for c in range(self.n_columns):
            column = self.get_column(c)
            built = self.__build_numbers__(column)
            correct = self.columns[c]

            if len(built) > len(correct):
                return False

            for i in range(len(built)):
                if built[i] > correct[i]:
                    return False

            if column.count('□') == 0 and built != correct:
                return False

        return True

    @staticmethod
    def __build_numbers__(cells):
        idx = 0
        numbers = [0]
        for cell in cells:
            if cell == '■':
                numbers[idx] += 1
            elif cell in '□×' and numbers[idx] > 0:
                numbers.append(0)
                idx += 1
        if numbers[-1] == 0 and len(numbers) > 1:
            numbers.pop()
        return numbers
