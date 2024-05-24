import random


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
        counter: int = 0
        for i in range(max(0, row - 1), min(self.n, row + 2)):
            for j in range(max(0, col - 1), min(self.n, col + 2)):
                if self.pole[i][j].mine:
                    counter += 1
        return counter

    def init(self):
        seen: list = []
        while len(seen) < self.m:
            row: int = random.randint(0, self.n - 1)
            col: int = random.randint(0, self.n - 1)
            if (row, col) not in seen:
                self.pole[row][col].mine = True
                self.pole[row][col].fl_open = True
                seen.append((row, col))

        for row in range(self.n):
            for col in range(self.n):
                mines_count: int = self.get_around_mines_count(row, col)
                self.pole[row][col].around_mines = mines_count
                if mines_count > 0:
                    self.pole[row][col].fl_open = True

    def show(self):
        open_field: list[list[str]] = [['' for _ in range(self.n)] for _ in range(self.n)]
        for row in range(self.n):
            for col in range(self.n):
                if self.pole[row][col].mine:
                    open_field[row][col] = '*'
                elif self.pole[row][col].fl_open:
                    open_field[row][col] = str(self.pole[row][col].around_mines)
                elif not self.pole[row][col].fl_open:
                    open_field[row][col] = '#'

        for item in open_field:
            print(' '.join(item))


a = GamePole(10, 12)
a.show()
