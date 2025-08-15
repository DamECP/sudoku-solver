from itertools import combinations


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

    def naked_singles(self):
        """Easiest sudoku method : reduce possibilities for each cell
        based on what is already valid within the row, col, square."""

        row_col_square = ["row", "col", "square"]

        progress = False

        for group in row_col_square:

            validated_cells = {
                i.value
                for i in all_spaces
                if getattr(i, group) == getattr(self, group) and i.value is not None
            }
            current_cells = [
                i
                for i in all_spaces
                if getattr(i, group) == getattr(self, group) and i.value is None
            ]

            for cell in current_cells:

                for value in validated_cells:
                    if value in cell.possibilities:
                        cell.possibilities.remove(value)
                        progress = True

        return progress

    def hidden_singles(self, group):

        progress = False

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
                before = len(item.possibilities)
                item.possibilities = list(
                    set(item.possibilities) - set(self.possibilities)
                )
                if len(item.possibilities) < before:
                    progress = True

        return progress

    def hidden_ns(self, group):

        progress = False

        for idx in range(1, 10):  # Will be used as an index for each row/col/square

            # list of unknowns spaces within a row/col/square
            block = [
                space
                for space in all_spaces
                if getattr(space, group) == idx and space.value is None
            ]

            # subset len to be tested
            for subset_len in range(2, 5):

                # all possible combinations of spaces depending on the subset length
                for space_group in combinations(block, subset_len):

                    # gather the possibilities as one specific set
                    # ex : {1, 4} + {2, 4} + {1, 2, 4} = {1, 2, 4}
                    all_combinations = set()
                    for space in space_group:
                        all_combinations.update(space.possibilities)

                    if len(all_combinations) == subset_len:

                        # gather the spaces that correspond to the subset
                        processed_spaces = [
                            space
                            for space in block
                            if any(
                                poss in all_combinations for poss in space.possibilities
                            )
                        ]

                        # ex : if 3 spaces share the values {1, 2, 4}
                        if set(processed_spaces) == set(space_group):

                            # limit the possibilities of that group to that set
                            for space in space_group:
                                space.possibilities = list(all_combinations)

                            # take this set out of the other spaces possibilities
                            for c in block:
                                if c not in space_group:
                                    new_possibilities = [
                                        p
                                        for p in c.possibilities
                                        if p not in all_combinations
                                    ]

                                    if len(new_possibilities) != len(c.possibilities):
                                        c.possibilities = new_possibilities
                                        progress = True

        return progress


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


def resolve_sudoku(max_passes=4):
    progress = True
    passes = 0
    while progress and passes < max_passes:
        progress = False
        passes += 1
        for group in ["row", "col", "square"]:
            for space in all_spaces:
                if space.naked_single():
                    progress = True
                if space.hidden_singles(group):
                    progress = True
                if space.hidden_ns(group):
                    progress = True
    if passes >= max_passes:
        print(
            f"⚠ Arrêt forcé après {max_passes} passes pour éviter une boucle infinie."
        )


resolve_sudoku()


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


print_sudoku()
