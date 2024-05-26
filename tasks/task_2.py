import random


def clear_console():
    """Функция для очистки консоли"""
    print('\n' * 50)


def check_for_out_of_range(raw_coordinates: list[int]) -> bool:
    """Функция для проверки ввода координат на выход за пределы списка"""
    return len(list(filter(lambda x: 0 <= x < N, raw_coordinates))) == 2


def game_process(game_obj: 'GamePole') -> bool:
    """Функция контролирующая состояние игры"""
    status: bool = True
    while status:
        if game_obj.check_win():
            return True
        print('\n\nВведите клетку для хода.')
        step: str = input()
        try:
            coordinates: list = list(map(int, step.split(' ')))
        except ValueError:
            print('Координаты должны быть числами!')
            continue
        if check_for_out_of_range(coordinates):
            status = game_obj.make_step(*coordinates)
        else:
            print('Таких координат не существует!')
    return status


class Cell:
    def __init__(self, around_mines=0, mine=False):
        self.around_mines: int = around_mines
        self.mine: bool = mine
        self.fl_open: bool = False


class GamePole:
    def __init__(self, n, mines_count):
        self.n: int = n
        self.m: int = mines_count
        self.__pole = [[Cell() for _ in range(n)] for _ in range(n)]
        self.init()

    @property
    def pole(self) -> list[list[Cell]]:
        return self.__pole

    def get_around_mines_count(self, row: int, col: int) -> int:
        """Метод, который считает количество мин рядом для каждой ячейки"""
        counter: int = 0
        for i in range(max(0, row - 1), min(self.n, row + 2)):
            for j in range(max(0, col - 1), min(self.n, col + 2)):
                if self.pole[i][j].mine:
                    counter += 1
        return counter

    def check_win(self) -> bool:
        """Метод, который проверяет, является ли поле полностью разминированным"""
        if self.m == 0:
            return True

        open_cells: int = 0
        for row in range(self.n):
            for col in range(self.n):
                if self.pole[row][col].fl_open:
                    open_cells += 1
        return open_cells == (self.n ** 2 - self.m)

    def calculate_around_mines(self):
        """Метод, который определяет количество мин поблизости для каждой ячейки"""
        for row in range(self.n):
            for col in range(self.n):
                mines_count: int = self.get_around_mines_count(row, col)
                self.pole[row][col].around_mines = mines_count

    def init(self):
        """Метод, который расставляет мины по полю"""
        seen: list = []
        while len(seen) < self.m:
            row: int = random.randint(0, self.n - 1)
            col: int = random.randint(0, self.n - 1)
            if (row, col) not in seen:
                self.pole[row][col].mine = True
                seen.append((row, col))
        self.calculate_around_mines()

    def show(self, field: list[list[str]]):
        """Метод, который выводит текущее состояние поля"""
        print('\t' + ' '.join(map(str, list(range(self.n)))))
        print('\t' + '_ ' * self.n)
        for idx, item in enumerate(field):
            print(str(idx) + ' | ' + ' '.join(item))

    def update_fields(self):
        """Метод, который обновляет состояние поля"""
        open_field: list[list[str]] = [['' for _ in range(self.n)] for _ in range(self.n)]
        for row in range(self.n):
            for col in range(self.n):
                if self.pole[row][col].fl_open and self.pole[row][col].mine:
                    open_field[row][col] = '*'
                elif self.pole[row][col].fl_open and not self.pole[row][col].mine:
                    open_field[row][col] = str(self.pole[row][col].around_mines)
                elif not self.pole[row][col].fl_open:
                    open_field[row][col] = '#'
        self.show(open_field)

    def make_step(self, row: int, col: int) -> bool:
        """Метод, который позволяет игроку сделать шаг с проверкой на проигрыш"""
        if self.pole[row][col].mine:
            return False
        else:
            self.pole[row][col].fl_open = True
        clear_console()
        self.update_fields()
        return True


if __name__ == '__main__':
    N: int = 3
    MINES: int = 2

    game = GamePole(N, MINES)
    print("Вас привествует игра 'Сапёр'\n"
          "Для хода введите координаты клетки\n"
          "Например, 1 2 - 1 строка, 2 cтолбец\n\n")
    input("Если вы готовы, нажмите Enter...\n\n")

    game.update_fields()
    game_status = game_process(game)

    if game_status:
        print("\n\n\tПоздравляю, вы победили!")
    else:
        print("Вы взорвались..")
