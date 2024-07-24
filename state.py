import random

class ChocolateBoard:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.chocolates = [('circle', 'brown'), ('circle', 'pink'), ('circle', 'white'),
                            ('square', 'brown'), ('square', 'pink'), ('square', 'white'),
                            ('triangle', 'brown'), ('triangle', 'pink'), ('triangle', 'white')]
        self.constraints = {}

        # Generate random constraints
        for shape, color in self.chocolates:
            row, col = random.randint(0, 2), random.randint(0, 2)
            while (row, col) in self.constraints:
                row, col = random.randint(0, 2), random.randint(0, 2)
            constraint_type = random.choice(['shape', 'color'])
            if constraint_type == 'shape':
                self.constraints[(row, col)] = (shape, None)
            else:
                self.constraints[(row, col)] = (None, color)

        # Update board based on constraints
        for (row, col), (shape, color) in self.constraints.items():
            if shape:
                self.board[row][col] = shape[0]
            else:
                self.board[row][col] = color[0]

    def copy(self):
        new_board = ChocolateBoard()
        new_board.board = [row[:] for row in self.board]
        new_board.chocolates = self.chocolates.copy()
        new_board.constraints = self.constraints.copy()
        return new_board

    def print_board(self):
        for row in range(3):
            for col in range(3):
                print(f'[{self.board[row][col]}]', end='')
            print()

        print("\nConstraints:")
        for (row, col), (shape, color) in self.constraints.items():
            if shape:
                print(f"  - ({row}, {col}): {shape}")
            else:
                print(f"  - ({row}, {col}): {color}")

    def place_chocolate(self, chocolate, row, col):
        self.board[row][col] = chocolate

    def remove_chocolate(self, row, col):
        self.board[row][col] = ' '

    def set_constraint(self, row, col, shape, color):
        self.constraints[(row, col)] = (shape, color)

    def remove_constraint(self, row, col):
        if (row, col) in self.constraints:
            del self.constraints[(row, col)]

    def is_goal(self):
        for (row, col), (shape, color) in self.constraints.items():
            if self.board[row][col] != shape[0] + color[0]:
                return False
        return True

    def expand(self):
        possible_boards = []

        for chocolate in self.chocolates:
            for row in range(3):
                for col in range(3):
                    new_board = self.copy()
                    if new_board.board[row][col] == ' ' and (row, col) not in new_board.constraints.values():
                        new_board.place_chocolate(chocolate[0][0] + chocolate[1][0], row, col)
                        possible_boards.append(new_board)

        return possible_boards

    def hdistance(self):
        num_violated = 0
        for (row, col), (shape, color) in self.constraints.items():
            if self.board[row][col] != shape[0] + color[0]:
                num_violated += 1
        return num_violated



