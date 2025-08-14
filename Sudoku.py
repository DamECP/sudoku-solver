with open("sudoku_example.txt", "r") as example:
    sudoku_example = [line.strip() for line in example.readlines()]

all_spaces = []
squares, rows, columns = ({i: [] for i in range(1, 10)} for _ in range(3))


class Space:
    def __init__(self):
        self.row = None
        self.col = None
        self.possibilities = []
        self.square_row = None
        self.square_col = None
        self.square = None

    @property
    def value(self):
        if len(self.possibilities) == 1:
            return self.possibilities[0]
        return None

    def reduce_by_line(self, rows):
        if self.value is None:
            for value in rows[self.row]:
                if value in self.possibilities:
                    self.possibilities.remove(value)

    def reduce_by_column(self, columns):
        if self.value is None:
            for value in columns[self.col]:
                if value in self.possibilities:
                    self.possibilities.remove(value)

    def reduce_by_square(self, squares):
        if self.value is None:
            for value in squares[self.square]:
                if value in self.possibilities:
                    self.possibilities.remove(value)

    def reserved_spots(self, group):

        same = [
            space
            for space in all_spaces
            if getattr(space, group) == getattr(self, group) and not space.value
        ]

        comparable = [
            i for i in same if set(i.possibilities) <= set(self.possibilities)
        ]
        if self not in comparable:
            comparable.append(self)
        others = [i for i in same if set(i.possibilities) > set(self.possibilities)]

        if len(comparable) == len(self.possibilities):
            for item in others:
                item.possibilities = list(
                    set(item.possibilities) - set(self.possibilities)
                )

    def update(self, rows, columns, squares):
        if self.value:
            if self.value not in rows[self.row]:
                rows[self.row].append(self.value)
            if self.value not in columns[self.col]:
                columns[self.col].append(self.value)
            if self.value not in squares[self.square]:
                squares[self.square].append(self.value)

    def resolve(self, rows, columns, squares):

        self.reduce_by_line(rows)
        self.reduce_by_column(columns)
        self.reduce_by_square(squares)
        for group in ["row", "col", "square"]:
            self.reserved_spots(group)
        self.update(rows, columns, squares)


for i, row in enumerate(sudoku_example, 1):
    for j, char in enumerate(row, 1):

        s = Space()

        # from 1 to 9 each
        s.row, s.col = i, j

        # 3 square_rows corresponding to big squares
        # adder helps to build the square_col value
        if i in range(1, 4):
            s.square_row = 1
            adder = 0
        elif i in range(4, 7):
            s.square_row = 2
            adder = 3
        elif i in range(7, 10):
            s.square_row = 3
            adder = 6

        # 3 square_col corresponding to big squares
        if j in range(1, 4):
            s.square_col = 1
        elif j in range(4, 7):
            s.square_col = 2
        elif j in range(7, 10):
            s.square_col = 3

        # Builds the n° of the square the space belongs to
        s.square = s.square_col + adder

        if char == "x":
            s.possibilities = list(range(1, 10))

        # Builds all the possible lists
        else:
            # Only one solution => value is validated within the class
            s.possibilities.append(int(char))
            squares[s.square].append(int(char))
            rows[s.row].append(int(char))
            columns[s.col].append(int(char))

        all_spaces.append(s)


finished = False
n = 0
while not finished:
    for space in all_spaces:
        before = space.possibilities.copy()
        space.resolve(rows, columns, squares)
    n += 1
    if all(space.value is not None for space in all_spaces):
        finished = True
    if n > 20:
        break


def print_sudoku():
    for i in range(1, 10):  # pour chaque ligne
        if i in [4, 7]:  # ligne de séparation horizontale
            print("-" * 21)  # 9 cases * 2 (espaces) + 3 pour les séparateurs verticaux
        for j in range(1, 10):  # parcourir les colonnes
            space = next(s for s in all_spaces if s.row == i and s.col == j)
            if j in [4, 7]:  # séparation verticale
                print("|", end=" ")
            print(space.value if space.value else "x", end=" ")
        print()  # saut de ligne après chaque ligne
    print()
    print(f"Nombre de passes : {n}")


print_sudoku()
